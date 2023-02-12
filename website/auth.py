from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import current_user
import mysql.connector
import json
import random
import smtplib


auth = Blueprint('auth', __name__)

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="finman"
    )

my_cursor = mydb.cursor()

email = 0
name = 0
number = 0
passw = 0
pin = 0
balance = 0
@auth.route('/', methods=['GET', 'POST'])
def start():
    return render_template("home.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method=="POST" :
     emailornum = request.form.get('emailornum')
     password = request.form.get('password')
     my_cursor.execute("select email,mno,password,pin,name from login")
     my_data = my_cursor.fetchall()
     msc = 0
     record = 0
     for i in my_data:
         if emailornum in i:
             msc+=1
             record = i
             break
         else:
             continue
     if msc == 0 :
         flash('Invalid Email or Username', category='error')

     else:
         if password != record[2] :
             flash('Incorrect password', category='error')

         else :
            print(record)
            global email
            global number
            global pin
            global passw
            global name
            email = emailornum
            passw =password
            pin = record[3]
            name = record[4]
            number = record[1]
            return redirect(url_for('auth.home2'))

  return render_template("login.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method=="POST":
    emai = request.form.get('email')
    numbe = request.form.get('number')
    password = request.form.get('password')
    nam = request.form.get('name')
    pi = request.form.get('pin')
    print(nam)
    temp = []
    if not str(numbe).isdigit() or len(numbe) != 10:
        flash("Invalid mobile number entered... ",category="error")
    else:
      my_cursor.execute("select email,mno from login")
      data = my_cursor.fetchall()
      for i in data:
         for j in i :
             temp.append(j)

      if emai in temp  :
          flash("Email already exists...",category="error")

      elif numbe in temp :
           flash("Mobile Number already exists...",category="error")

      else :
            if not pi.isdigit() or len(pi)!=4:
               flash("Invalid pin (pin can only be 4 digits long)",category="error")
            else :
                my_cursor.execute("insert into login values('{}','{}','{}','{}','{}','{}')".format(emai,numbe,password,pi,nam,"no"))
                mydb.commit()
                e=emai
                p= pi
                n= nam
                nu = numbe
                global email
                global passw
                global  name
                global pin
                global number
                email = e
                passw = password
                pin = p
                name = n
                number = nu
                flash("Signup successful", category="success")
                return redirect(url_for("auth.home2"))


  return render_template("signup.html", user=current_user)


@auth.route('/home2', methods=['GET', 'POST'])
def home2():
    global number
    print(number)
    my_cursor.execute("Select kyc from login where mno='{}'".format(number))
    gg=my_cursor.fetchall()
    print(gg)
    kyc = gg[0][0]
    if kyc != 'done':
        flash("you are not eligible to access our services as your kyc hasn't been completed kindly complete your Kyc to continue", category="Error")
        return redirect(url_for("auth.kycbookc"))
    else :
        my_cursor.execute("show tables")
        t=my_cursor.fetchall()
        upiid="fim"+number
        for i in t:
            if upiid in i:
                pass
            else :
                my_cursor.execute("create table IF NOT EXISTS {} (date datetime,transid varchar(255),transac varchar (255), balance varchar (255))".format(upiid))
                mydb.commit()


    return render_template("home2.html", user=current_user)


@auth.route('/kycbookc', methods=['GET', 'POST'])
def kycbookc():
    return render_template("kycbookc.html", user=current_user)

@auth.route('/kycbook', methods=['GET', 'POST'])
def kycbook():
 if request.method=="POST":
  global number
  if number != 0:
    global email
    global name
    address = request.form.get('address')
    landmark = request.form.get('landmark')
    my_cursor.execute("select mno from kycbooking")
    ff=my_cursor.fetchall()
    h = 0
    for i in ff:
        if number in i:
            h+=1
    if h == 0:
          flash("You have already made a request kindly be patient",category="error")
          return redirect(url_for("auth.logout"))
    else :
        my_cursor.execute("insert into kycbooking values('{}','{}','{}','{}','{}')".format(email, number,name,address,landmark))
        mydb.commit()
    return render_template("kycbook.html", user=current_user)
  else :
      flash("kindly login first",category="Error")



@auth.route('/crypto', methods=['GET', 'POST'])
def crypto():

    return render_template("crypto.html", user=current_user)


@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    global number
    global email
    global name
    global balance

    upiid = "fim" + number
    my_cursor.execute("select * from {} ".format(upiid))
    gg=my_cursor.fetchall()
    file = [email,name,balance,number,gg]
    return render_template("profile.html", user=current_user,data=file)


@auth.route('/sendmoney', methods=['GET', 'POST'])
def sendmoney():
 if request.method =='POST':
     global name
     namec=name
     upiid = request.form.get('landmark')
     name = request.form.get('landmark')
     amount = request.form.get('landmark')
     pin = request.form.get('pin ')
     my_cursor.execute("show tables;")
     tables=my_cursor.fetchall()
     counter=0
     for i in tables:
       if upiid in i:
           counter+=1
     if counter!=0 :
         global number
         upiidc="fin"+str(number)
         my_cursor.execute("select balance from balance where upiid='{}'".format(upiidc))
         if int(balance)>int(amount):
             my_cursor.execute("select pin from login where number='{}'".format(number))
             d=my_cursor.fetchall()
             if pin == d[0][0]:
                 my_cursor.execute("select name from login where number='{}'".format(upiid[3:]))
                 d=my_cursor.fetchall()
                 if name == d[0][0]:
                     nb=str(int(balance)-int(amount))
                     my_cursor .execute("update table balance set balance = '{}' where number={}".format(nb,number))
                     mydb.commit()
                     my_cursor.execute("insert into {} values ('{}','{}','{}','{}')".format(upiidc,now,rnd,"You sent"+str(amount)+"$ to"+name,balance))
                     mydb.commit()
                     my_cursor.execute("insert into {} values ('{}','{}','{}','{}')".format(upiid,now,rnd,"You recieved"+str(amount)+"$ from"+namec,balance))
                     mydb.commit()
                     flash("Money Sent successfully", category="success")
                 else :
                     flash("Name doesn't match", category="Error")
             else :
                 flash("Incorrect pin ", category="Error")
         else :
          flash("Insufficient Balance",category="Error")

 return render_template("sendmoney.html",user=current_user)
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
   global email
   global pin
   global number
   global passw
   global balance
   global name
   email = 0
   pin = 0
   number = 0
   passw = 0
   balance = 0
   name = 0
   return redirect(url_for("auth.login"))

@auth.route('/passbook', methods=['GET', 'POST'])
def passbook():
    global number
    global email
    global name
    global balance

    upiid = "fim" + str(number)
    my_cursor.execute("select * from {} ".format(upiid))
    gg = my_cursor.fetchall()
    return render_template("passbook.html",user=current_user,data=gg)