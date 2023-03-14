from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
class Recipe:
    db='recipes'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.description=data['description']
        self.instructions=data['instructions']
        self.date_cooked=data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id= data["user_id"]
        self.chef=None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name,under,description,instructions,date_cooked,created_at,updated_at,user_id) VALUES  (%(name)s,%(under)s,%(description)s,%(instructions)s,%(date_cooked)s,NOW(),NOW(),%(user_id)s);"
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def update(cls,data):
        query='UPDATE recipes SET name = %(name)s,under = %(under)s, description = %(description)s,instructions = %(instructions)s,date_cooked = %(date_cooked)s,updated_at=NOW() WHERE recipes.id=%(id)s;'
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def findIdr(cls,data):
        query="SELECT * FROM recipes WHERE id = %(id)s"
        result= connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return cls(result[0])

    @classmethod
    def findId(cls,data):
        query="SELECT * FROM recipes JOIN users ON user_id = users.id WHERE recipes.id = %(id)s"
        result= connectToMySQL(cls.db).query_db(query,data)
        recipe=cls(result[0])
        user_data={
            "id":result[0]['users.id'],
        'first_name':result[0]['first_name'],
        'last_name':result[0]['last_name'],
        'email':result[0]['email'],
        'password':"",
        'created_at':result[0]['users.created_at'],
        "updated_at":result[0]['users.updated_at']
            }
        recipe.chef = user.User(user_data)
        return recipe

    @classmethod
    def select_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON user_id = users.id;"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for recipe in results:
            this_recipe = cls(recipe)
            user_data={
            "id":recipe['users.id'],
        'first_name':recipe['first_name'],
        'last_name':recipe['last_name'],
        'email':recipe['email'],
        'password':"",
        'created_at':recipe['users.created_at'],
        "updated_at":recipe['users.updated_at']
            }
            this_recipe.chef = user.User(user_data)
            recipes.append(this_recipe)
        return recipes

    @staticmethod
    def validate_recipes(recipe):
        is_valid = True
        query = "SELECT * FROM recipes WHERE  = %(recipes)s;"
        results = connectToMySQL('recipes').query_db(query,recipe)
        if len(recipe['name']) < 1:
            flash("name must be 1 or more characters")
            is_valid=False
        if len(recipe['description']) < 3:
            flash("Description must be 3 or more characters")
            is_valid=False
        if len(recipe['instructions']) < 3:
            flash("Instruction must be 3 or more characters")
            is_valid=False
        if len(recipe['date_cooked']) < 1:
            flash("Date cooked  must be selected")
            is_valid=False
        
        return is_valid

    @staticmethod
    def validate_recipes_update(recipe):
        is_valid = True
        query = "SELECT * FROM recipes WHERE  = %(recipes)s;"
        results = connectToMySQL('recipes').query_db(query,recipe)
        if len(recipe['name']) < 1:
            flash("name must be 1 or more characters")
            is_valid=False
        if len(recipe['description']) < 3:
            flash("Description must be 3 or more characters")
            is_valid=False
        if len(recipe['instructions']) < 3:
            flash("Instruction must be 3 or more characters")
            is_valid=False
        if len(recipe['date_cooked']) < 1:
            flash("Date cooked  must be selected")
            is_valid=False
        
        return is_valid

    @classmethod
    def delete(cls,data):
        query="DELETE FROM recipes WHERE id = %(id)s"
        result= connectToMySQL(cls.db).query_db(query,data)