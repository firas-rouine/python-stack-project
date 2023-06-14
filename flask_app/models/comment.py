from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class Comment:
    # CONSTRUCTOR - Make Defaults
    def __init__(self, data):
        self.id = data["id"]
        self.comment = data["comment"]
        self.user_id = data["user_id"]
        self.institution_id = data["institution_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.full_name = None

    # ========== CREATE new comment ============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO comments (comment,user_id, institution_id)
                    VALUES (%(comment)s,%(user_id)s,  %(institution_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    
    # ========= show favory by ID ============
    @classmethod
    def get_all_comments(cls, data):
        query  = """SELECT * FROM comments join users on comments.user_id = users.id
        WHERE institution_id = %(institution_id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        list = []
        if not results:
            return list
        for result in results:
            comment = cls(result)
            comment.full_name = result['first_name'] +" "+ result['last_name']
            list.append(comment)
        return list
