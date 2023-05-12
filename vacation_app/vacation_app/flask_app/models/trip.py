from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
class Trip:
    db="vacation_schema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.duration = data['duration']
        self.departure_date = data['departure_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.traveler = None

#Read

#get all
    @classmethod
    def get_all_trips(cls):
        query="""
            SELECT * FROM trips;
        """
        results = connectToMySQL(cls.db).query_db(query)

        all_trips=[]

        for trip in results:
            all_trips.append(cls(trip))

        return all_trips



#get one by id
    @classmethod
    def get_one_trip(cls,data):
        query="""
            SELECT * FROM trips
            WHERE id = %(id)s;
        """

        results=connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    #get one with traveler
    @classmethod
    def get_one_with_user(cls,data):
        query="""
            SELECT * FROM trips
            JOIN users ON trips.user_id= users.id
            WHERE trips.id = %(id)s;
        """
        results=connectToMySQL(cls.db).query_db(query, data)
        one_trip= cls(results[0])
        user_data={
            'id':results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'age':results[0]['age'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at'],
        }
        one_user =user.User(user_data)
        one_trip.traveler = one_user
        return one_trip




#create
    @classmethod
    def save_trip(cls,data):
        query="""
            INSERT INTO trips
            (name, location, duration, departure_date, user_id)
            VALUES(%(name)s,%(location)s,%(duration)s,%(departure_date)s,%(user_id)s);
        """

        return connectToMySQL(cls.db).query_db(query,data)

#update
    @classmethod
    def update_trip(cls, data):
        query="""
            UPDATE trips
            SET name=%(name)s, location=%(location)s, duration=%(duration)s, departure_date=%(departure_date)s
            WHERE id= %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)




#delete

    @classmethod
    def delete_trip(cls, data):
        query="""
            DELETE FROM trips
            WHERE id = %(id)s;
        """

        return connectToMySQL(cls.db).query_db(query,data)



    @staticmethod
    def validate_trip(data):
        is_valid=True
        if len(data['name']) < 2:
            is_valid=False
            flash('Name must be at least 2 characters in length','Trips')
        if len(data['location']) == 0:
            is_valid=False
            flash('Location cannot be empty','Trips')
        if len(data['duration']) == 0:
            is_valid=False
            flash('Duration cannot be empty','Trips')
        if len(data['departure_date']) == 0:
            is_valid=False
            flash('Departure Date cannot be empty','Trips')
        return is_valid


