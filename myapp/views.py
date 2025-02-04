from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector as sql
from django.contrib import messages
from datetime import datetime

cnx = sql.connect(host='sql12.freesqldatabase.com', user='sql12761055', password='VfnMGSEFyj', database='sql12761055')
cur = cnx.cursor()

def func(request):
    return render(request, 'index.html')

def login(request):
    try:
        if request.method == "GET":
            return render(request, "login.html")
        if request.method == "POST":
            email1 = request.POST.get('email1')
            password1 = request.POST.get('password1')
            if email1 is not None:
                q = f"SELECT * FROM customers WHERE adhr='{email1}' AND password='{password1}';"
                cur.execute(q)
                print(email1, password1)
                result = cur.fetchall()
                if result:
                    adhr = result[0][1]  # Assuming 'adhr' is the third column in the 'customers' table
                    return redirect('profile', adhr=adhr)
                else:
                    messages.error(request, "Check details correctly")
                    return redirect('login')
    except Exception as e:
        return HttpResponse(e)

def create(request):
    try:
        if request.method == "GET":
            return render(request, 'create.html')
        if request.method == "POST":
            name = request.POST.get('name')
            adhr = request.POST.get('adhr')
            phone = request.POST.get('phone')
            age = request.POST.get('age')
            email2 = request.POST.get('email2')
            password2 = request.POST.get('password2')
            if email2 is not None:
                q=f"select * from customers where adhr='{adhr}';"
                cur.execute(q)
                l1=[]
                for i in cur:
                    l1.append(i)
                if(not l1):
                    q = f"INSERT INTO customers(name, adhr, phone, age, email, password,balance) VALUES('{name}', '{adhr}', '{phone}', '{age}', '{email2}', '{password2}','{5000}');"
                    cur.execute(q)
                    cnx.commit()
                    q=f"insert into transaction(adhr)values('{adhr}');"
                    cur.execute(q)
                    cnx.commit()
                    messages.success(request, "Created Successfully")
                    return redirect('profile', adhr=adhr)
                else:
                    messages.error(request,"User Already exists")
                    return redirect('create')
        return render(request, 'create.html')  # Ensure an HttpResponse is returned for all POST cases

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

def profile(request, adhr):
        q = f"SELECT * FROM customers WHERE adhr='{adhr}';"
        cur.execute(q)
        l = []
        for i in cur:
            l.append(i)
        q = f"SELECT * FROM transaction WHERE adhr='{adhr}';"
        cur.execute(q)
        l1 = []
        for i in cur:
            l1.append(i)
        print(l)
        l1 = [t for t in l1 if t[1] and t[1].strip()]
        l1.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'))
        l1.reverse()
        return render(request, 'profile.html', {'person': l, 'tr': l1})
def about(request,adhr):
    return render(request,'about.html',{'adhr':adhr})
def loan(request,adhr):
    return render(request,'loan.html',{'adhr':adhr})
def transfer(request,adhr):
    if(request.method=="GET"):
        return render(request,'transfer.html',{'adhr':adhr})
    q=f"select * from customers where adhr='{adhr}';"
    cur.execute(q)
    l=[]
    for i in cur:
        l.append(i)
    if(request.method=="POST"):
        name=request.POST.get('acc')
        amount=request.POST.get('amount')
        desc=request.POST.get('desc')
        s=str(datetime.today())
        q=f"select * from customers where adhr='{name}';"
        cur.execute(q)
        l1=[]
        for i in cur:
            l1.append(i)
        print(l1)
        if(not l1 or l[0][6] < amount):
            q = f"INSERT INTO transaction(adhr, date, description, amount, status) VALUES ('{adhr}', '{s[:19]}', '{desc}', '{amount}', 'Failed');"
            cur.execute(q)
            messages.error(request,"Transaction Failed")
        if(l1!=[] and l[0][6]>amount):
            trx=int(l[0][6])-int(amount)
            print(l1)
            q=f"update customers set balance='{trx}' where adhr='{adhr}';"
            cur.execute(q)
            q=f"INSERT INTO transaction(adhr, date, description, amount, status) VALUES ('{adhr}', '{s[:19]}', '{desc}', '{str('-'+amount)}', 'Success');"
            cur.execute(q)
            q=f"update customers set balance='{str(int(l1[0][6])+int(amount))}' where adhr='{name}';"
            cur.execute(q)
            q=f"INSERT INTO transaction(adhr, date, description, amount, status) VALUES ('{name}', '{s[:19]}', '{desc}', '{str('+'+amount)}', 'Recieved');"
            cur.execute(q)
            cnx.commit()
    return redirect('profile',adhr=adhr)
def hist(request,adhr):
    query = "SELECT date, description, amount, status FROM transaction WHERE adhr = %s;"
    with cnx.cursor() as cur:
        cur.execute(query, [adhr])
        transactions = cur.fetchall()
    transaction_list = [
        {"date": row[0], "description": row[1], "amount": row[2], "status": row[3]}
        for row in transactions
    ]
    transaction_list = [t for t in transaction_list if t['date'] and t['date'].strip()]
    transaction_list.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'))
    transaction_list.reverse()
    
    return render(request, 'hist.html', {'transactions': transaction_list})
def update(request,adhr):
    if(request.method=="GET"):
        q=f"select * from customers where adhr='{adhr}';"
        cur.execute(q)
        l=[]
        for i in cur:
            l.append(i)
        return render(request,'update.html',{'person':l})
    if(request.method=="POST"):
        name=request.POST.get('name')
        age=request.POST.get('age')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        q=f"update customers set name='{name}',phone='{phone}',age='{age}',email='{email}' where adhr='{adhr}';"
        cur.execute(q)
        cnx.commit()
    return redirect('profile',adhr=adhr)