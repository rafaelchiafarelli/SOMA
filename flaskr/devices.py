from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('devices', __name__)

@bp.route('/device_list')
def index():
    db = get_db()
    devices = db.execute(
        'SELECT *'
        ' FROM device p'
    ).fetchall()
    return render_template('devices/device_list.html', devices=devices)

@bp.route('/device_register', methods=('POST',))
def create():
    if request.method == 'POST':
        content = request.json

        if "type" not in content:
            return jsonify({"Error":"dev_type not present"})
        if "IP"  not in content:
            return jsonify({"Error":"dev_IP not present"})
        if "PORT" not in content:
            return jsonify({"Error":"dev_PORT not present"})
        if "character" not in content:
            return jsonify({"Error":"character not present"})
        if "endpoints" not in content:
            return jsonify({"Error":"endpoints not present"})
        if "animations" not in content:
            return jsonify({"Error":"animations not present"})

        dev_type = content["type"]
        dev_IP = content["IP"]
        dev_PORT = content["PORT"]
        dev_character = content["character"]
        endpoints = content["endpoints"]
        endp ="{}".format(endpoints) 
        animations = content["animations"]
        anim = "{}".format(animations)
        

        db = get_db()
        db.execute(
            'INSERT or REPLACE INTO device (dev_type, dev_IP, dev_PORT, dev_character, endpoints, animations)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (dev_type, dev_IP,dev_PORT,dev_character,endp,anim)
        )
        db.commit()
        return "{}"

    return "{}"

