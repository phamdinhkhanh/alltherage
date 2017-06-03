import mongoengine
# mongodb://<dbuser>:<dbpassword>@ds155080.mlab.com:55080/shiptest
host = "ds157971.mlab.com"
port = 57971
db_name = "akana"
username = "khanh"
password = "khanh"

def connect():
    mongoengine.connect(db_name, host=host, port=port, username=username, password=password)


def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())