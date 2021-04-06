from classes.Registration import Registration
from flask import Flask, render_template, redirect, request, jsonify, send_file, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import sys
import numpy as np
import json
from flask_qrcode import QRcode
import os
import cv2
import pyqrcode
from werkzeug.utils import secure_filename
from flask import send_from_directory

# import qrtools
from PIL import Image
from pyzbar.pyzbar import decode

sys.path.insert(0, sys.path[0]+'\\classes')

UPLOAD_FOLDER = "/home/muhammad/Desktop/Working Areas/flask-save-food/static/uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
qrcode = QRcode(app)
app.secret_key = "app"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


class store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    group = db.Column(db.String(20), nullable=False)

    def __init__(self, name, username, password, group):
        self.name = name
        self.username = username
        self.password = password
        self.group = group


class charity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    group = db.Column(db.String(20), nullable=False)

    def __init__(self, name, username, password, group):
        self.name = name
        self.username = username
        self.password = password
        self.group = group

class fooditem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    itemName = db.Column(db.String(120), nullable=False)
    expDay = db.Column(db.Integer, nullable=False)
    expMonth = db.Column(db.Integer, nullable=False)
    expYear = db.Column(db.Integer, nullable=False)
    qx = db.Column(db.Integer, nullable=False)


    def __init__(self, username, itemName, expDay, expMonth, expYear, qx):
        self.username = username
        self.itemName = itemName
        self.expDay = expDay
        self.expMonth = expMonth
        self.expYear = expYear
        self.qx = qx

@app.route('/')
def index():
    reg = Registration()
    return render_template("Home.html")


@app.route('/login')
def login():
    reg = Registration()
    return render_template("login.html")


@app.route('/signup')
def signup():
    reg = Registration()
    return render_template("signup.html")

# ---------------------------------

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))
            return redirect(url_for('display', filename=filename))

    return render_template("checkout.html")


# ---------------------------------

# ---------------------------------------------

@app.route('/uploader/display/<filename>')
def display(filename):

    result = decode(Image.open('static/uploads/'+filename))
    data = result[0].data.decode()
    list_of_data = [] #[{id, qx}, {id, qx}, ...]
    for item in data.split(',')[:-1]:
        ids = item.split('|')[0] #it's a simple id
        qx = item.split('|')[1]
        list_of_data.append({"id": ids, "qx": qx})

    new_data = [] # [{all of properties which are given below}, ...]
    for obj in list_of_data:
        item = fooditem.query.filter_by(id=obj['id']).first()
        new_data.append({"id":item.id,"username":item.username,"itemName":item.itemName,"expDay":item.expDay,"expMonth":item.expMonth,"expYear":item.expYear,"qx":obj['qx']})

    print(new_data)
    #properties
    # id 
    # username
    # itemName
    # expDay
    # expMonth
    # expYear
    # qx
    return render_template("display.html", data=new_data)



# ---------------------------------------------



@app.route('/create/<name>/<username>/<password>/<cpass>/<group>')
def create(name, username, password, cpass, group):
    if group == "Store":
        isFound = store.query.filter_by(username=username).first()
        if isFound == None:
            print("ok")
            _store = store(name, username, password, group)
            db.session.add(_store)
            db.session.commit()
            return render_template("store-added.html")
        else:
            return render_template("user-exists.html")
    elif group == "Charity" :
        isFound = charity.query.filter_by(username=username).first()
        if isFound == None:
            _charity = charity(name, username, password, group)
            db.session.add(_charity)
            db.session.commit()
            return render_template("charity-added.html")
        else:
            return render_template("user-exists.html")


@app.route('/login/<username>/<password>/<group>')
def getLoginStore(username, password, group):
    if group == "Store":
        isFound = store.query.filter_by(username=username).first()
        if isFound != None:
            if password == isFound.password : 
                items = {}
                items = fooditem.query.filter_by(username=username).all()
                return render_template("item-list-store.html", usrname=isFound.username, items=items)
            else : return render_template("pass-not-match.html")
        else: return render_template("user-not-found.html")
    elif group == "Charity":
        isFound = charity.query.filter_by(username=username).first()
        if isFound != None:
            if password == isFound.password : 
                items = {}
                items = fooditem.query.filter_by().all()
                return render_template("item-list-charity.html", usrname=isFound.username, items=items)
            else : return render_template("pass-not-match.html")
        else: return render_template("user-not-found.html")
   
       

@app.route('/item/<username>')
def item(username):
    return render_template("add-item-store.html", usrname=username)


@app.route('/list/item/<username>')
def listitem(username):
    items = {}
    items = fooditem.query.filter_by(username=username).all()
    return render_template("item-list-store.html", usrname=username, items=items)


@app.route('/add/item/<username>/<itemName>/<expDay>/<expMonth>/<expYear>/<qx>')
def additem(username, itemName, expDay, expMonth, expYear, qx):
    _item = fooditem(username, itemName, expDay, expMonth, expYear, qx)
    db.session.add(_item)
    db.session.commit()
    return redirect("http://127.0.0.1:5000/list/item/"+username)


@app.route('/show/cart/<data>')
def goToCart(data) :
    # print('inside of cart -----------------------------',type(data))
    datas=json.loads(data)
    code = ''
    print(datas)
    for obj in datas:
        # print(obj)
        string = "{}|{},".format(obj['id'], obj['qx'])
        code+=string
    qr = pyqrcode.create(code) #saving data in qr code
    qr.png('static/images/qrcode.png', scale=8) #saving qrcode image
    return render_template("cart.html", data=json.loads(data), jsons=data)

@app.route('/qr/<data>')
def genrateQR(data):
    items = json.loads(data) #[{id, qx},...]
    code = ''
    for obj in items:
        # print(obj)
        string = "{}|{},".format(obj['id'], obj['qx'])
        code+=string
    qr = pyqrcode.create(code) #saving data in qr code
    qr.png('static/images/qrcode.png', scale=8) #saving qrcode image

    return render_template('qrcode.html')

@app.route('/download')
def download():
    img = cv2.imread('static/images/qrcode.png', 1)
    path = get_download_path()
    cv2.imwrite(os.path.join(path , 'qrcode.png'),img)
    cv2.waitKey(0)
    # return redirect('http://127.0.0.1:5000/qr/downloaded')
    return ("nothing")

    
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


