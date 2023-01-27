from flask import Flask,redirect,render_template,request,session,url_for,jsonify
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
app = Flask(__name__)
app.secret_key='JackViewLand Secret Key'

def get_database():
    CONNECTION_STRING=r'mongodb+srv://admin:admin@cluster0.x24cglf.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)
    return client['restaurant_reservation']

@app.route("/index",methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])
def index():
    if 'name' in session:
        name=session['name']
        print(name)
        return render_template('index.html',name=name)
    return render_template('index.html')

@app.route('/user')
def user():
    try:
        name=session['name']
        print(name)
        dbname = get_database()
        collection= dbname["events"]
        calendar = list(collection.find({'title':{'$regex':f'{name}.*'}}))
        if len(calendar) != 0:
            for c in calendar:
                del c['_id'],c['end_event']
                return render_template('booking.html',name=name,calendar=calendar)
        else:
            return "<a href='/'>無訂位資料!</a>"
    except:
            return index()

@app.route('/user/cancel/<id>')
def cancel(id):
    dbname = get_database()
    collection= dbname["events"]
    collection.delete_one({'id':id})
    return "<script>alert('cancel the reservation');window.location.replace('/user');</script>"

@app.route('/reserve')
def reserve():
    persons=request.args.get('persons')
    date=request.args.get('date')
    date=date.split('/')
    day,month,year=date
    time=request.args.get('time')
    t = time.split(' ')[0].split(':')
    if 'PM' in time:
        hour,mins=t
        hour=int(hour)+12
        start_time=f'{hour}:{mins}:00'
        end_time=f'{hour+2}:{mins}:00'
    else:
        hour,mins=t
        start_time=f'{hour}:{mins}:00'
        end_time=f'{hour+2}:{mins}:00'
    start=f'{year}-{month}-{day} {start_time}'
    end=f'{year}-{month}-{day} {end_time}'
    if 'name' in session:
        name=session['name']
        title=f'{name} {persons}位'
    data=[title,start,end]
    print(data)

    dbname = get_database()
    collection= dbname["events"]
    data={'title':title,'start_event':start,'end_event':end,'id':str(title)+str(ObjectId())}
    collection.insert_one(data)  
    return "<script>alert('Success');window.location.replace('/');</script>"
    

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email=request.form['email']
        name=request.form['name']
        password = request.form['password']
        user_data={'email':email,'name':name,'password':password}
        try:
            dbname = get_database()
            collection= dbname["user"]
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
        collection= dbname["user"]
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

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method =='POST':
        account=request.form['email']
        password=request.form['password']
        dbname = get_database()
        collection= dbname["user"]
        result=collection.find_one({'account':account})
        if result is not None:
            if result['password'] == password:
                session['admin']=1
                return admin_calendar()
            else:
                content='Passwords do not match!'
                return 'error'
    if request.method=='GET':
        if 'admin' in session:
            return admin_calendar()
    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin',None)
    return redirect(url_for('admin')) 

def admin_calendar():
    dbname = get_database()
    collection= dbname["events"]
    calendar = list(collection.find({}))
    return render_template('calendar.html', calendar = calendar)

@app.route("/admin/insert",methods=["POST","GET"])
def insert():
    if request.method == 'POST':
        dbname = get_database()
        collection= dbname["events"]
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        print(title)     
        print(start)
        data={'title':title,'start_event':start,'end_event':end,'id':str(title)+str(ObjectId())}
        collection.insert_one(data)  
        msg = 'success' 
    return jsonify(msg)

@app.route("/admin/update",methods=["POST","GET"])
def update():
    if request.method == 'POST':
        dbname = get_database()
        collection= dbname["events"]
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        id = request.form['id']
        print(title)     
        print(start)
        collection.update_one({'id':id},{'$set':{'title':title,'start_event':start,'end_event':end}})  
        msg = 'success' 
    return jsonify(msg)

@app.route("/admin/ajax_delete",methods=["POST","GET"])
def ajax_delete():
    if request.method == 'POST':
        dbname = get_database()
        collection= dbname["events"]
        getid = request.form['id']
        collection.delete_one({'id':getid})
        msg ='Record deleted successfully' 
    return jsonify(msg)        

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)