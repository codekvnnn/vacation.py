from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app.models import trip
class User:
    db = "vacation_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.age = data['age']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.vacations = []


    def full_name(self):
        return f"{self.first_name} {self.last_name}"
#create
    @classmethod
    def create_user(cls,data):
        query="""
            INSERT INTO users
            (first_name, last_name, age, email, password)
            VALUES(%(first_name)s, %(last_name)s, %(age)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

#read
#get all
    @classmethod
    def get_all_users(cls):
        query ="""
            SELECT * FROM users;
        """
        results = connectToMySQL(cls.db).query_db(query)

        all_users=[]

        for user in results:
            all_users.append(cls(user))

        return all_users



#get one

    @classmethod
    def get_one_user(cls, data):
        query="""
            SELECT * FROM users
            WHERE id = %(id)s;
        """

        results =connectToMySQL(cls.db).query_db(query,data)

        return cls(results[0])


    @classmethod
    def get_user_by_email(cls,data):
        query="""
            SELECT * FROM users
            WHERE email=%(email)s;
        """
        results= connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_user_with_trips(cls,data):
        query="""
            SELECT * FROM users
            LEFT JOIN trips ON users.id = trips.user_id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)

        one_user= cls(results[0])

        if len(results) >1: #alternative solution to the "None" problem in the html

            for row in results:
                # if row['trips.id'] == None:      ***#this is the way we did it in class***
                #     return one_user
                trip_data={
                    'id': row['trips.id'],
                    'name': row['name'],
                    'location': row['location'],
                    'duration': row['duration'],
                    'departure_date': row['departure_date'],
                    'user_id': row['user_id'],
                    'created_at': row['trips.created_at'],
                    'updated_at': row['trips.updated_at']
                }
                one_trip=trip.Trip(trip_data)
                one_user.vacations.append(one_trip)

        return one_user


#update


#delete


    @staticmethod
    def validate_user(data):
        is_valid=True
        user = User.get_user_by_email(data)
        if user:
            is_valid=False
            flash('user already exists', 'Users')
        if len(data['first_name']) <3:
            is_valid=False
            flash('First Name must be at least 3 characters', 'Users')
        if len(data['last_name']) <3:
            is_valid=False
            flash('Last Name must be at least 3 characters', 'Users')
        if len(data['age']) ==0:
            is_valid=False
            flash('Age cannot be left empty', 'Users')
        if len(data['email']) ==0:
            is_valid=False
            flash('Email cannot be left empty', 'Users')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid=False
            flash('Email must be in the proper format','Users')
        if len(data['password']) <8:
            is_valid=False
            flash('Password must be at least 8 characters', 'Users')
        # if data['password'] != data['confirm_password']:
        #     is_valid=False
        #     flash('Passwords do not match', 'Users')
        return is_valid
