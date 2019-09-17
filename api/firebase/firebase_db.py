from firebase_admin import db


def write_filesName(name_file):
    db.reference("filesName").push(name_file)
    return 'write success.'


def funcCallBack(dataEvent):
    print(dataEvent.data != '')
    if dataEvent.data != '':
        data = dataEvent.data


# def
def realTimeDb():
    root = db.reference("filesName")
    root.listen(callback=funcCallBack)