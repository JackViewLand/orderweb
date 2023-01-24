from flask import Flask,redirect,render_template,request,session,url_for
from pymongo import MongoClient
import pymongo
app = Flask(__name__)
app.secret_key='JackViewLand Secret Key'

def get_database():
    CONNECTION_STRING=r'mongodb+srv://admin:admin@cluster0.x24cglf.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)
    return client['User_list']

@app.route("/index",methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])
def index():
    if 'name' in session:
        name=session['name']
        print(name)
        return render_template('index.html',name=name)
    return render_template('index.html')

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email=request.form['email']
        name=request.form['name']
        password = request.form['password']
        user_data={'email':email,'name':name,'password':password}
        try:
            dbname = get_database()
            collection= dbname["data"]
            result=collection.find_one({'email':email})
            if result is None:
                collection.insert_one(user_data)
                content='Success!'
            else:
                content='Email is already in use!'
            return render_template('signup.html',content=content)
        except:
            return render_template('signup.html',content='Please Try again!')
    return  render_template('signup.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method =='POST':
        email=request.form['email']
        password=request.form['password']
        dbname = get_database()
        collection= dbname["data"]
        result=collection.find_one({'email':email})
        if result is not None:
            if result['password'] == password:
                session['name']=result['name']
                return redirect(url_for('index'))
            else:
                content='Passwords do not match!'
                return render_template('login.html',content=content)
        else:
            content='No email found!'
            return render_template('login.html',content=content)
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('name',None)
    return redirect(url_for('index')) 

@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)