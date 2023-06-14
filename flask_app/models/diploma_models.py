from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash


class Diploma:
    def __init__(self, data):
        self.diploma = data["diploma"]
        self.program_tittle = data["program_tittle"]
        self.description = data["description"]
        self.institution_id = data["institution_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    #=========================create diploma program=============
    @classmethod
    def create(cls,data):
        query="""
                INSERT INTO diplomas (diploma,program_tittle,description,institution_id)
                VALUE (%(diploma)s,%(program_tittle)s,%(description)s,%(institution_id)s)
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #=========================get all institution diplomas =============
    @classmethod
    def get_institution_diplomas(cls,data):
        query = """ 
                    SELECT * FROM diplomas WHERE institution_id =%(institution_id)s;
                """
        results = connectToMySQL(DATABASE).query_db(query,data)
        diplomas = []
        for row in results:
            diplomas.append(cls(row))
        return diplomas


    # =============== VALIDATIONS ================

    @staticmethod
    def validate(data):
            is_valid = True
        # Check the diploma
            if len(data['diploma1']) < 2:
                flash("Diploma is Required !", "error_diploma")
                is_valid = False
            # Check the program_tittle
            if len(data['program_tittle1']) < 2:
                flash("Program_tittle is Required !", "error_program_tittle")
                is_valid = False
            # Check the description
            if len(data['description1']) < 2:
                flash("Description is Required !", "error_description")
                is_valid = False

            return is_valid