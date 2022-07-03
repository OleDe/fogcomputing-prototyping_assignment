import pymongo, sys

class cldb:
    def __init__(self):
        self.hostname = 'localhost'
        self.port = 27017
        self.username = 'cl'
        self.password = 'cl123'
        self.db_name = 'cl_db'
        self.collection_name = 'sensor_data'
        self.client = pymongo.MongoClient(self.hostname,
                                            self.port,
                                            username=self.username,
                                            password=self.password)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        self.collection.create_index([('time', pymongo.ASCENDING)],
                                    unique=True)
    
    def insert(self, air_pressure, air_temperature, time):
        """
        Insert a document in sensor_data collection.
        """
        try:
            self.collection.insert_one({'air_pressure': air_pressure,
                            'ait_temperature': air_temperature,
                            'time': time})
        except pymongo.errors.DuplicateKeyError:
            print('cldb.insert: Document already exists!', file=sys.stderr)
    
    def get_data_latter_than(self, time):
        """
        Returns data that was created after time.
        """
        return self.collection.find({'time' : { '$gt':  time }}).sort('time')

    def erase_data_starting_from(self, time):

        """
        Erases data that is older than or equal time.
        """
        return self.collection.delete_many({'time' : { '$lte':  time }})


if __name__ == '__main__':
    db = cldb()
    db.insert(1013.25, 25, 12345)
    db.insert(1014.25, 26, 12346)
    db.insert(1015.25, 27, 12347)
    print(list(db.get_data_newer_than(12346)))
    db.erase_old_data_starting_from(12346)
