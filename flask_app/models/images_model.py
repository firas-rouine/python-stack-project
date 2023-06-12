
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app,DATABASE,IMAGES_PATH
from flask import flash
from flask import render_template,request, redirect, session,flash,url_for


class Image:
    def __init__(self, data):
        self.id = data["id"]
        self.name = IMAGES_PATH+data["name_image"]
        self.institution_id = data["institution_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    #=================create images for institutions ===============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO images (institution_id,name_image)
                    VALUES (%(institution_id)s,%(name_image)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    # #=================get all images for institutions ===============
    # @classmethod
    # def get_images_institution(cls,data):
    #     query = """ 
    #                 SELECT * FROM images WHERE images.institution_id =%(institution_id)s;
    #             """
    #     results = connectToMySQL(DATABASE).query_db(query,data)
    #     images = []
    #     for row in results:

    #         images.append(cls(row))
    #     return images