from flask import Flask,render_template,request,session,redirect
from flask_app import app
from flask_app.models import recipe,user

@app.route('/recipes')
def success():
    data = {
        'id':session['user_id']
    }
    return render_template('recipe_list.html',recipes=recipe.Recipe.select_recipes(),user = user.User.get_by_id(data))

@app.route('/create')
def create():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create.html')

@app.route('/add_recipe', methods=['POST'])
def validate():
    if not recipe.Recipe.validate_recipes(request.form):
        return redirect('/create')
    user_id=session['user_id']
    data={
        'name':request.form['name'],
        'under':request.form['under'],
        'description':request.form['description'],
        'instructions':request.form['instructions'],
        'date_cooked':request.form['date_cooked'],
        'user_id':user_id
    }
    recipe.Recipe.save(data)
    print(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('show_recipe.html',recipes=recipe.Recipe.findId({'id':id}))

@app.route('/recipes/edit/<int:id>',methods=["POST"])
def update(id):
    update_data={
        "name":request.form["name"],
        "under":request.form["under"],
        "description":request.form['description'],
        'instructions':request.form['instructions'],
        "date_cooked":request.form['date_cooked'],
        "id":id
    }
    if not recipe.Recipe.validate_recipes_update(update_data):
        return redirect(f'/recipes/edit/{id}')
    recipe.Recipe.update(update_data)
    return redirect('/recipes')

@app.route('/recipes/edit/<int:id>')
def display(id):
    return render_template ('edit.html',recipe=recipe.Recipe.findIdr({'id':id}))

@app.route('/delete/<int:id>')
def delete(id):
    recipe.Recipe.delete({'id':id})
    return redirect('/recipes')