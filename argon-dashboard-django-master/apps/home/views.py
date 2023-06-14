# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import datetime,json
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from apps.home.models import Broker, user,strategy,TradingAccount
from tinydb import TinyDB,Query
from json import dumps
db=TinyDB('db.json')




def homepage(request):
    return render(request,'home/index.html')

def register(request):
    if request.method =='POST':
          username=request.POST.get('Username')
          email=request.POST.get('email')
          password=request.POST.get('password')
          cfm_pass=request.POST.get('cfm_pass')

          if password!=cfm_pass:
               messages.error(request, "Your password and confirm password are not same.")
               
          else:
             my_user=User.objects.create_user(username,email,password)
             my_user.save()
             return redirect('home/login')
        
    return render(request, 'accounts/register.html')



def login(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        pass1=request.POST.get('password')
        user=authenticate(request,username=name, password=pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('/homepage')
        else:
            return HttpResponse("incorrect")
    return render(request, 'home/login.html')



def profile(request):
    return render(request,'home/profile.html')


#=======================================================================================broker

def createBroker(request):
    return render(request,'home/createBroker.html')

def saveBroker(request):
    broker_name = request.POST.get("broker_name")
    broker_logo = request.POST.get("logo")
    created_date=request.POST.get("created_date")
    #b=Broker()
    #b.broker_name=broker_name;
    #b.broker_logo=broker_logo;
    #b.created_date=datetime.datetime.now()
    l=[{'broker_name':broker_name,'broker_logo':broker_logo,'created_date':created_date}]
    db.insert_multiple(l)
    return render(request,'home/createBroker.html')



def showBroker(request):
    data=db.all()
    return render(request, "home/showBroker.html", {"data": data})
def update_saveBroker(request):
    broker=Query()
    id=request.POST.get("id")
    db.search(broker.id==id)
    broker_name= request.POST.get("broker_name");
    broker_logo=request.POST.get("logo");
    updated_date=request.POST.get("updated_date");
    l=[{'broker_name':broker_name,'broker_logo':broker_logo,'updated_date':updated_date}]
    db.insert_multiple(l)
    # u.save()
    return HttpResponseRedirect("/showBroker")
def deleteBroker(request,id):
    broker=Query()
    db.remove(broker.id==id)
    #delete1 = Broker.objects.get(id=id)
    #delete1.delete()
    return HttpResponseRedirect("/showBroker")

def updateBroker(request,id):
    #broker=Query()
    data=Broker.objects.get(id=id)
    #cat=db.search(broker.id==id)
    return render(request,"home/updateBroker.html",{"data":data})

######3333333333=======================================================================================user


def createUser(request):
    db=TinyDB('db2.json')
    return render(request,'home/createUser.html')

def saveUser(request):
    db=TinyDB('db2.json')
    user_name= request.POST.get("user_name")
    password = request.POST.get("password")
    contact_no= request.POST.get("contact_no")
    email= request.POST.get("email")
    status= request.POST.get("status")
    created_date=request.POST.get("created_date")
    m=[{'user_name':user_name,'password':password,'contact_no':contact_no,'email':email,'status':status,'created_date':created_date}]
    db.insert_multiple(m)
    #b=user()
    #b.user_name=user_name;
    #b.email=email;
    #b.contact_no=contact_no;
    #b.user_password=password;
    #b.status=status;
    #b.created_date=datetime.datetime.now()
    #b.save()
    return render(request,'home/createUser.html')



def showUser(request):
    db=TinyDB('db2.json')
    data = db.all()
    return render(request, "home/showUser.html", {"data": data})

def update_saveUser(request):
    id=request.POST.get("id")
    u=user.objects.get(id=id)
    u.user_name= request.POST.get("user_name");
    u.email=request.POST.get("email");
    u.contact_no=request.POST.get("contact_no");
    u.user_password=request.POST.get("password");
    u.status=request.POST.get("status");
    u.updated_date=datetime.datetime.now()
    u.save()
    return HttpResponseRedirect("/showUser")
def deleteUser(request,id):
    delete1 = user.objects.get(id=id)
    delete1.delete()
    return HttpResponseRedirect("/showUser")

def updateUser(request,id):
    data=user.objects.get(id=id)
    return render(request,"home/updateUser.html",{"data":data})


######3333333333=======================================================================================Strategy



def createStrategy(request):
    return render(request,'home/createStrategy.html')

def saveStrategy(request):
    strategy_name= request.POST.get("strategy_name")
    strategy_type = request.POST.get("strategy_type")
    status= request.POST.get("status")
    created_date=datetime.datetime.now()
    m=[{'strategy_name':strategy_name,'strategy_type':strategy_type,'status':status,'created_date':created_date}]
    db.insert_multiple(m)
    #b=strategy()
    #b.strategy_name=strategy_name;
    #b.strategy_type=strategy_type;
    #b.status=status;
    #b.created_date=datetime.datetime.now()
    #b.save()
    return render(request,'home/createStrategy.html')



def showStrategy(request):
    data = strategy.objects.all().values()
    return render(request, "home/showStrategy.html", {"data": data})

def update_saveStrategy(request):
    id=request.POST.get("id")
    u=strategy.objects.get(id=id)
    u.strategy_name= request.POST.get("strategy_name");
    u.strategy_type=request.POST.get("strategy_type");
    u.status=request.POST.get("status");
    u.updated_date=datetime.datetime.now()
    u.save()
    return HttpResponseRedirect("/showStrategy")
def deleteStrategy(request,id):
    delete1 = strategy.objects.get(id=id)
    delete1.delete()
    return HttpResponseRedirect("/showStrategy")

def updateStrategy(request,id):
    data=strategy.objects.get(id=id)
    return render(request,"home/updateStrategy.html",{"data":data})





def createTradingAccount(request):
    user_data=user.objects.all().values()
    li=[]
    for x in user_data:
        li.append(x)
    broker_data=Broker.objects.all().values()
    return render(request, "home/createTradingAccount.html", {"data":{"user_data":li,"broker_data":broker_data}})

def saveTradingAccount(request):
    ta = TradingAccount()
    UserID = user.objects.get(id=request.POST.get("UserID"))
    BrokerID =Broker.objects.get(id=request.POST.get("BrokerID"))
    Zerodha_UserID = request.POST.get("Zerodha_UserID")
    Zerodha_Password = request.POST.get("Zerodha_Password")
    Zerodha_TOTP_Key = request.POST.get("Zerodha_TOTP_Key")
    IIFL_Email_id = request.POST.get("IIFL_Email_id")
    IIFL_Contact_Number = request.POST.get("IIFL_Contact_Number")
    IIFL_App_Source = request.POST.get("IIFL_App_Source")
    IIFL_User_Key = request.POST.get("IIFL_User_Key")
    IIFL_User_id = request.POST.get("IIFL_User_id")
    IIFL_Password = request.POST.get("IIFL_Password")
    IIFL_Encry_Key = request.POST.get("IIFL_Encry_Key")
    IIFL_OcpApimSubscription = request.POST.get("IIFL_OcpApimSubscription")
    IIFL_My2Pin = request.POST.get("IIFL_My2Pin")
    IIFL_ClientCode = request.POST.get("IIFL_ClientCode")
    IIFL_cpass = request.POST.get("IIFL_cpass")
    Kotak_Key = request.POST.get("Kotak_Key")
    Kotak_Secret = request.POST.get("Kotak_Secret")
    TA_Status = request.POST.get("TA_Status")
    
    Created_By = request.POST.get("Created_By")
    ta.UserID = UserID
    ta.BrokerID = BrokerID
    ta.Zerodha_UserID = Zerodha_UserID
    ta.Zerodha_Password = Zerodha_Password
    ta.Zerodha_TOTP_Key = Zerodha_TOTP_Key
    ta.IIFL_Email_id = IIFL_Email_id
    ta.IIFL_Contact_Number = IIFL_Contact_Number
    ta.IIFL_App_Source = IIFL_App_Source
    ta.IIFL_User_Key = IIFL_User_Key
    ta.IIFL_User_id = IIFL_User_id
    ta.IIFL_Password = IIFL_Password
    ta.IIFL_Encry_Key = IIFL_Encry_Key
    ta.IIFL_OcpApimSubscription = IIFL_OcpApimSubscription
    ta.IIFL_My2Pin = IIFL_My2Pin
    ta.IIFL_ClientCode = IIFL_ClientCode
    ta.IIFL_cpass = IIFL_cpass
    ta.Kotak_Key = Kotak_Key
    ta.Kotak_Secret = Kotak_Secret
    ta.TA_Status = TA_Status
    ta.TA_Created_Date = datetime.datetime.now()
    ta.Created_By = Created_By
   
    ta.save()
    return render(request,"home/createTradingAccount.html")



def showTradingAccount(request):
    data = TradingAccount.objects.all().values()
    return render(request, "home/showTradingAccount.html", {"data": data})

def update_saveTradingAccount(request):
    id=request.POST.get("id")
    ta=TradingAccount.objects.get(id=id)

    UserID = user.objects.get(id=request.POST.get("UserID"))
    BrokerID =Broker.objects.get(id=request.POST.get("BrokerID"))
    Zerodha_UserID = request.POST.get("Zerodha_UserID")
    Zerodha_Password = request.POST.get("Zerodha_Password")
    Zerodha_TOTP_Key = request.POST.get("Zerodha_TOTP_Key")
    IIFL_Email_id = request.POST.get("IIFL_Email_id")
    IIFL_Contact_Number = request.POST.get("IIFL_Contact_Number")
    IIFL_App_Source = request.POST.get("IIFL_App_Source")
    IIFL_User_Key = request.POST.get("IIFL_User_Key")
    IIFL_User_id = request.POST.get("IIFL_User_id")
    IIFL_Password = request.POST.get("IIFL_Password")
    IIFL_Encry_Key = request.POST.get("IIFL_Encry_Key")
    IIFL_OcpApimSubscription = request.POST.get("IIFL_OcpApimSubscription")
    IIFL_My2Pin = request.POST.get("IIFL_My2Pin")
    IIFL_ClientCode = request.POST.get("IIFL_ClientCode")
    IIFL_cpass = request.POST.get("IIFL_cpass")
    Kotak_Key = request.POST.get("Kotak_Key")
    Kotak_Secret = request.POST.get("Kotak_Secret")
    TA_Status = request.POST.get("TA_Status")
    
    Created_By = request.POST.get("Created_By")
    ta.UserID = UserID
    ta.BrokerID = BrokerID
    ta.Zerodha_UserID = Zerodha_UserID
    ta.Zerodha_Password = Zerodha_Password
    ta.Zerodha_TOTP_Key = Zerodha_TOTP_Key
    ta.IIFL_Email_id = IIFL_Email_id
    ta.IIFL_Contact_Number = IIFL_Contact_Number
    ta.IIFL_App_Source = IIFL_App_Source
    ta.IIFL_User_Key = IIFL_User_Key
    ta.IIFL_User_id = IIFL_User_id
    ta.IIFL_Password = IIFL_Password
    ta.IIFL_Encry_Key = IIFL_Encry_Key
    ta.IIFL_OcpApimSubscription = IIFL_OcpApimSubscription
    ta.IIFL_My2Pin = IIFL_My2Pin
    ta.IIFL_ClientCode = IIFL_ClientCode
    ta.IIFL_cpass = IIFL_cpass
    ta.Kotak_Key = Kotak_Key
    ta.Kotak_Secret = Kotak_Secret
    ta.TA_Status = TA_Status
    ta.Created_By = Created_By
    ta.Updated_Date=datetime.datetime.now()
    ta.save()
    return HttpResponseRedirect("/showTradingAccount")

def deleteTradingAccount(request,id):
    delete1 = TradingAccount.objects.get(id=id)
    delete1.delete()
    return HttpResponseRedirect("/showTradingAccount")

def updateTradingAccount(request,id):
    user_data=user.objects.all().values()
    li=[]
    for x in user_data:
        li.append(x)
    broker_data=Broker.objects.all().values()
    data1=TradingAccount.objects.get(id=id)
    return render(request,"home/updateTradingAccount.html",{"data1":data1,"data":{"user_data":li,"broker_data":broker_data}})