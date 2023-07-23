#this will start operations
import subprocess

def start_recording(Folder, FileName):
    subprocess.Popen(["pwd"])
    subprocess.Popen(["python","./VideoCreator/video_recorder.py","-f",FileName, "-d", Folder, "&&"])
    return 

def start_processing(Folder, FileName, CharacterType):
    print(CharacterType)
    if CharacterType == "magistrade":
        subprocess.Popen(["python","./VideoCreator/magistrade.py","-f",FileName, "-d", Folder, "&&"])
    elif CharacterType == "messenger":
        subprocess.Popen(["python","./VideoCreator/messenger.py","-f",FileName, "-d", Folder, "&&"])

    return

def start_sending(Folder, FileName, IPDestination, FolderDestination):
    return