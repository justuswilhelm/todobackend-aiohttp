from os import environ
from uuid import uuid4


class Task:

    db = {}

    @classmethod
    def create_object(cls, content):
        uuid = str(uuid4())
        HOST = environ['HOST']
        PORT = environ['PORT']
        obj = {
            'uuid': uuid,
            'completed': False,
            'url': 'http://{HOST}:{PORT}/{uuid}'.format(
                **locals())
        }
        obj.update(content)
        cls.set_object(uuid, obj)
        return obj

    @classmethod
    def all_objects(cls):
        return list(cls.db.values())

    @classmethod
    def delete_all_objects(cls):
        cls.db = {}

    @classmethod
    def get_object(cls, uuid):
        return cls.db[uuid]

    @classmethod
    def delete_object(cls, uuid):
        del cls.db[uuid]

    @classmethod
    def set_object(cls, uuid, value):
        cls.db[uuid] = value

    @classmethod
    def update_object(cls, uuid, value):
        obj = cls.db[uuid]
        obj.update(value)
        return obj
