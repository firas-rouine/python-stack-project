from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app,DATABASE,IMAGES_PATH
from flask import flash
from flask import render_template,request, redirect, session,flash,url_for

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Institution:
    # CONSTRUCTOR - Make Defaults
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.email = data["email"]
        self.phone = data["phone"]
        self.fax = data["fax"]
        self.diploma = data["diploma"]
        self.program_tittle = data["program_tittle"]
        self.description = data["description"]
        self.creator_id = data["creator_id"]
        self.created_at = data["created_ad"]
        self.updated_at = data["updated_at"]
        self.image = None

    # ========== CREATE Institution ============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO institutions (name, email, phone, fax, diploma,program_tittle, description, creator_id)
                    VALUES (%(name)s,  %(email)s, %(phone)s,%(fax)s, %(diploma)s, %(program_tittle)s, %(description)s, %(creator_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    #=========================get user by id creator =======================
    @classmethod
    def get_by_id_creator(cls,id):
        query="SELECT * FROM institutions join users on users.id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,id)
        # print("slect inst 🐱‍🐉🐱‍🐉🐱‍🐉============================",result)
        if len(result) <1:
            return False
        return result[0]
    
    
    #=========================get all creator =======================
    @classmethod
    def get_all_institutions(cls):
        query = """
            select * from institutions; 
        """
        results = connectToMySQL(DATABASE).query_db(query)
        # print(results)
        institutions = []
        for row in results:
            institution=cls(row)
            institution.image = cls.get_image({'institution_id':institution.id})
            institutions.append(institution)
        return institutions
    
    @classmethod
    def get_image(cls,data):
        query = """
        SELECT * FROM images where institution_id = %(institution_id)s order by created_at limit 1;
        """
        result  = connectToMySQL(DATABASE).query_db(query,data)
        if result:
            # print("👌"*20,result[0]['name_image'],"👌"*20)
            return IMAGES_PATH+result[0]['name_image']
        return None
    # =============== VALIDATIONS ================

    @staticmethod
    def validate(data):
        is_valid = True  # we assume this is true
        # Check the name
        if len(data['name']) < 3:
            flash("Name is Required !", "error_name")
            is_valid = False
        # Check the phone
        if len(data['phone']) < 2:
            flash("Phone is Required !", "error_phone")
            is_valid = False
        # Check the diploma
        if len(data['diploma']) < 2:
            flash("Diploma is Required !", "error_diploma")
            is_valid = False
        # Check the program_tittle
        if len(data['program_tittle']) < 2:
            flash("Program_tittle is Required !", "error_program_tittle")
            is_valid = False
        # Check the description
        if len(data['description']) < 2:
            flash("Description is Required !", "error_description")
            is_valid = False
        # Check the email
        if len(data["email"]) < 1:
            is_valid = False
            flash("Email is Required !", "error_email")
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "error_email")
            is_valid = False

        return is_valid
    @staticmethod
    def validate_institution_image(data):
        if len(data) == 1 :
            data.pop()
            img='img_institution.png'
            data.append({'name_image' : img})
            print('null is true 888888888888888888888888888888')
            return data
        else:
            return data