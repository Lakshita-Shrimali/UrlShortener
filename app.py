import string
import random

from flask import Flask, render_template, request, redirect, session, make_response, send_file, jsonify
from mysql.connector import connect
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='shrimalilakshita28@gmail.com',
    MAIL_PASSWORD='hmnhzokefijlxgbb'
)
app.secret_key='ghjhjhq/213763fbf'

mail=Mail(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<url>')
def dynamicUrl(url):
    connection = connect(host="localhost", database="student", user="root", password="password")
    cur = connection.cursor()
    query1 = "select * from urlinfo where encryptedUrl='{}'".format(url)
    cur.execute(query1)
    orignalurl = cur.fetchone()
    if orignalurl==None:
        return render_template('index.html')
    else:
        print(orignalurl[1])
        return redirect(orignalurl[1])


@app.route('/urlshortner')
def urlshortner():
    # letter='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    url = request.args.get('link')
    custom = request.args.get('customurl')
    username=request.args.get('username')
    print(custom)
    print("planettech")
    connection = connect(host="localhost", database="student", user="root", password="password")
    cur = connection.cursor()
    encryptedurl=''
    if custom=='':
        while True:
            encryptedurl=createEncrytedUrl()
            query1="select * from urlinfo where encryptedUrl='{}'".format(encryptedurl)
            cur.execute(query1)
            xyz=cur.fetchone()
            if xyz==None:
                break
        print(encryptedurl)
        #id = session['userid']
        if 'userid' in session:
            #id=session['userid']
            query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active,created_by) values('{}','{}',1,'{}')".format(url, encryptedurl,username)
        else:
            query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active) values('{}','{}',1)".format(url,encryptedurl)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        finalencryptedurl = 'sd.in/' + encryptedurl
    else:
        query1 = "select * from urlinfo where encryptedUrl='{}'".format(custom)
        cur.execute(query1)
        xyz = cur.fetchone()
        #id = session['userid']
        if xyz==None:
            if 'userid' in session:
                #id = session['userid']
                query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active,created_by) values('{}','{}',1,'{}')".format(url,custom,username)
            else:
                query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active) values('{}','{}',1)".format(url, custom, 1)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            finalencryptedurl = 'sd.in/' + custom
        else:
            #return "url already exist"
            return redirect('/home')
    if 'userid' in session:
        return redirect('/home')
    else:
        return render_template('index.html',finalencryptedurl=finalencryptedurl,url=url)

def createEncrytedUrl():
    letter = string.ascii_letters + string.digits
    encryptedurl = ''
    for i in range(6):
        encryptedurl = encryptedurl + ''.join(random.choice(letter))
    print(encryptedurl)
    return encryptedurl

@app.route('/signup')
def signup():
    return render_template('SignUp.html')
@app.route('/why_shrinker')
def why_shrinker():
    return render_template('why.html')

@app.route('/features')
def features():
    return render_template('Feature.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checkLoginIn')
def checkLogIn():
    email=request.args.get('email')
    password=request.args.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="password")
    cur = connection.cursor()
    query1 = "select * from userdetails where emailId='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz == None:
        return render_template('Login.html', xyz='you are not registered')
    else:
        if password == xyz[2]:
            session['email']=email
            session['userid']=xyz[1]
            #return render_template('UserHome.html')
            return redirect('/urlshortener')
        else:
            return render_template('Login.html', xyz='your password is not correct')


@app.route('/register',methods=['post'])
def register():
    email=request.form.get('email')
    username=request.form.get('uname')
    password=request.form.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="password")
    cur = connection.cursor()
    query1 = "select * from userdetails where emailId='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    if xyz==None:
        #file=request.files['file']
        #print(type(file))
        #file.save('F:/files/'+file.filename)
        query = "insert into userdetails(emailId,userName,password,is_Active,created_Date) values('{}','{}','{}',1,now())".format(email, username, password)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return 'you are successfully registered'
        return render_template("login.html")

    else:
        return 'already registered'
@app.route('/google')
def google():
    path='F:/files/as.jpg'
    return send_file(path,mimetype='image/jpg',as_attachment=True)

@app.route('/home')
def home():
    if 'userid' in session:
        email=session['email']
        username=session['userid']
        print(id)
        connection = connect(host="localhost", database="student", user="root", password="password")
        cur = connection.cursor()
        query1 = "select * from urlinfo where created_by='{}'".format(username)
        cur.execute(query1)
        data=cur.fetchall()
        print(data)
        return render_template('updateUrl.html',data=data)
    return render_template('login.html')




@app.route('/deleteUrl',methods=['post'])
def deleteUrl():
    if 'userid' in session:
        custom = request.form.get('encryptedUrl')
        connection = connect(host="localhost", database="student", user="root", password="password")
        cur = connection.cursor()
        query1 = "delete from urlinfo where encryptedUrl={}".format(custom)
        cur.execute(query1)
        connection.commit()
        return redirect('/home')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/askemail')
def askemail():
    return render_template('askemail.html')

@app.route('/forgetpassword')
def forgetpassword():
    print("hi")
    email = request.args.get('email')
    randomnumber = ''
    letter = string.digits
    for i in range(6):
        random.choice(letter)
        randomnumber =randomnumber + ''.join(random.choice(letter))
    body ='Your forget password OTP is'+ randomnumber
    msg1 = Message( subject = 'Forget Password Email', sender = 'shrimalilakshita28@gmail.com', recipients=[email], body= body)
    msg1.cc = ['it2024067@mlvti.ac.in']
    mail.send(msg1)
    connection = connect(host='localhost', database='student', user='root', password='Lak@shita28')
    cur = connection.cursor()
    query1 = "update userdetails set otp='{}' where emailId= '{}'".format(randomnumber,email)
    cur.execute(query1)
    connection.commit()
    return render_template('updatepassword.html',email = email)

@app.route('/xyzlogin',methods=['post'])
def testapi():
    abc=request.get_json()
    print(abc)
    list=[]
    da={}
    connection = connect(host="localhost", database="student", user="root", password="password")
    cur = connection.cursor()
    query = "select * from urlinfo"
    cur.execute(query)
    data = cur.fetchall()
    for i in data:
        da["name"]=i[0]
        da["email"]=i[1]
        list.append(da)
    return jsonify(list)
@app.route('/updatepassword')
def updatepassword():
    email = request.form.get('email')
    otp = request.form.get('otp')
    password = request.form.get('password')
    connection = connect(host='localhost', database='student', user='root', password='password')
    cur1 = connection.cursor()
    #cur = connection.cursor()
    query1 = "select * from userdetails where emailId= '{}'".format(email)
    data = cur1.execute(query1)

    print(data)
    if data == None:
        return render_template('login.html', error="email is not correct")
    else:
        if (otp == data[0]):
            print("hello from if otpdatabse")
            query2 = "update userdetails set password='{}' where emailId= '{}'".format(password, email)
            cur1.execute(query2)
            connection.commit()
        else:
            return render_template('updatepassword.html',error="otp does not matched")
    return render_template('updateUrl.html')
if __name__ == "__main__":
    app.run()

