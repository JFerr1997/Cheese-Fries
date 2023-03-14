from flask import Flask,render_template,request,session,redirect,flash
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt=Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data={
        'first_name':request.form["first_name"],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash,
        'confirm_password':request.form['confirm_password']
    }
    user_id=User.save(data)
    session['user_id']=user_id
    return redirect('/recipes')



@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email or Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email or Password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')












if __name__ == "__main__":
    app.run(debug=True)