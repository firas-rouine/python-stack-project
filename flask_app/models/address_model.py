from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Address:
    # CONSTRUCTOR - Make Defaults
    def __init__(self, data):
        self.id = data["id"]
        self.government = data["government"]
        self.city = data["city"]
        self.zipcode = data["zipcode"]
        self.street = data["street"]
        self.institution_id = data["institution_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ========== CREATE Institution ============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO addresses (government, city, zipcode, street, institution_id)
                    VALUES (%(government)s,  %(city)s, %(zipcode)s,%(street)s, %(institution_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)


    # =============== VALIDATIONS ================

    @staticmethod
    def validate(data):
        is_valid = True  # we assume this is true
        # Check the government
        if len(data['government']) < 3:
            flash("Government is Required !", "error_government")
            is_valid = False
        # Check the city
        if len(data['city']) < 2:
            flash("City is Required !", "error_city")
            is_valid = False
        # Check the diploma
        if len(data['zipcode']) < 2:
            flash("Zipcode is Required !", "error_zipcode")
            is_valid = False
        # Check the street
        if len(data['street']) < 2:
            flash("Street is Required !", "error_street")
            is_valid = False

        return is_valid
