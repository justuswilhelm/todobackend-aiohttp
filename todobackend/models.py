class Task:

    db = {}

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
        cls.db[uuid].update(value)
