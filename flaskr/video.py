#this app will integrate the video for the characters

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import uuid
from flaskr.auth import login_required
from flaskr.db import get_db
from .video_operations import start_recording, start_processing, start_sending
import os.path

VideoState = [
    "begin",
    "recording",
    "recorded",
    "processing",
    "processed",
    "sending",
    "sent"
]

bp = Blueprint('video', __name__)

@bp.route('/list_video', methods=('GET', 'POST'))
def index():
    error = None    
    if request.method == 'POST':
        folder = request.form['folder']
        file_name = None

        if folder is None:
            error = "Must have a folder"
        else:
            video_to_update = get_post(folder)

        if video_to_update is None:
            error = "File name not found. Not a valid folder"
        else:
            if video_to_update["cur_state"] == VideoState[0]: #begin
                cur_state = VideoState[1]
                db = get_db()
                db.execute(
                    'UPDATE videos SET cur_state = ?'
                    ' WHERE file_name = ?',
                    (cur_state, video_to_update["file_name"])
                    )
                db.commit()
                start_recording(video_to_update['folder'], video_to_update['file_name'])
            elif video_to_update["cur_state"] == VideoState[1]: #recording
                error = "Can not change status while it is being recorded"
            elif video_to_update["cur_state"] == VideoState[2]: #recorded
                cur_state = VideoState[3]
                db = get_db()
                db.execute(
                    'UPDATE videos SET cur_state = ?'
                    ' WHERE file_name = ?',
                    (cur_state, video_to_update["file_name"])
                    )
                db.commit()                
                start_processing(video_to_update["folder"], video_to_update["file_name"], video_to_update['character_type'])
            elif video_to_update["cur_state"] == VideoState[3]: #processing
                error = "Can not send while it is being processd"
            elif video_to_update["cur_state"] == VideoState[4]: #processed
                cur_state = VideoState[5]
                db = get_db()
                db.execute(
                    'UPDATE videos SET cur_state = ?'
                    ' WHERE file_name = ?',
                    (cur_state, video_to_update["file_name"])
                    )
                db.commit()       
            elif video_to_update["cur_state"] == VideoState[5]: #sending
                error = "Still sending"
            elif video_to_update["cur_state"] == VideoState[6]: #processed
                error = "File Sended. Nothing to do"

    if error is not None:
        flash(error)

    db = get_db()
    videos = db.execute(
        'SELECT *'
        ' FROM videos'
    ).fetchall()
    return render_template('video/index.html', videos=videos, VideoState=VideoState)

@bp.route('/create_video', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        folder = request.form['folder']
        IP_dest = request.form['dest_ip']
        Folder_dest = request.form['dest_folder']
        dest_user = request.form['dest_user']
        dest_password = request.form['dest_password']
        character_type = request.form['character_type']
        error = None
        if os.path.isdir(folder) == False:
            os.mkdir(folder)
        else:
            db = get_db()
            remove = get_post(folder)
            if remove is not None:
                db.execute('DELETE FROM videos WHERE folder = ?', (folder,))
                db.commit()            
        if not folder or not IP_dest or not Folder_dest or not dest_user or not dest_password or not character_type:
            error = 'all parameters are required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur_state = VideoState[0]
            file_name = "{}.avi".format(uuid.uuid4())
            db.execute(
                'INSERT INTO videos (folder, file_name, cur_state, dest_ip, dest_folder, dest_user, dest_password, character_type)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (folder, file_name, cur_state, IP_dest, Folder_dest,dest_user, dest_password, character_type )
            )
            db.commit()
            return redirect(url_for('video.index'))

    return render_template('video/create.html')


def get_post(folder):
    file_ = get_db().execute(
        'SELECT *'
        ' FROM videos'
        ' WHERE folder = ?',
        (folder,)
    ).fetchone()
    return file_


@bp.route('/update_video', methods=["POST"])
def update():
    data = request.json
    folder = data.get('Folder')
    filename = data.get('FileName')
    cur_state = data.get('cur_state')
    if folder is None or filename is None or cur_state is None:
        return {'error':'all parameters are required'}
    file_ = get_db().execute(
        'SELECT *'
        ' FROM videos'
        ' WHERE folder = ?',
        (folder,)
    ).fetchone()    
    if file_ is not None:
        db = get_db()
        db.execute(
            'UPDATE videos SET cur_state = ?'
            ' WHERE file_name = ?',
            (cur_state, filename)
            )
        db.commit()
    else:
        print("error file not found")
        return {'error':'file not found in DataBase'}
    return {'result':"OK"}

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
