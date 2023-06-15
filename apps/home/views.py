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
from apps.home.models import Broker, user,strategy,TradingAccount,Input
from tinydb import TinyDB,Query
from json import dumps
from apps.home.Constants import BASE_URL
from apps.home.kite_init import kiteInit
from apps.home.itmBreakoutAlert import breakoutLogic
from apps.home.kite_trade import *
import datetime
import json
import time

from threading import Timer

Inputdb=TinyDB('Inputdb.json')
Brokerdb = TinyDB('Brokerdb.json')

# from_datetime =self.data.get("orb_range_start_time")
# x=from_datetime.replace("T"," ")+":00" 
# interval = "15minute"
# q = Query()
# interval = db.search(q.interval)
# ORB_candle_time = "30minute"
# high_window_size = db.search(q.high_window_size)
# low_window_size  = db.search(q.low_window_size)
# from_datetime =db.search(q.from_datetime)
# retracement=db.search(q.retracement)
# candle_HL_difference_points=db.search(q.candle_HL_difference_points)

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
    tradelogic = kiteInit()
    breakout_l = breakoutLogic()
    if request.method == 'POST':
        name=request.POST.get('name')
        pass1=request.POST.get('password')
        user=authenticate(request,username=name, password=pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('/homepage')
        else:
            return HttpResponse("incorrect")
        
    # tradelogic.getData()
    breakout_l.__init__()
    breakout_l.historicalData(request)
    tradelogic.dataAuth(request)
    # breakout_l.itmBreakoutAlert(request)
    # print(tradelogic.historicalData(request=request,from_datetime=from_datetime,interval=interval,
    #                                 to_datetime = datetime.datetime.now(), 
    #                                 instrument_token = 256265))
    # print(tradelogic.breakoutCandle(request=request,from_datetime=from_datetime,ORB_candle_time=ORB_candle_time))
    # tradelogic.moving_average_high(request=request,high_window_size=high_window_size)
    # tradelogic.moving_average_low(request=request,low_window_size=low_window_size)
    # tradelogic.top_range_breakout(request)
    return render(request, 'home/login.html')



def profile(request):
    return render(request,'home/profile.html')



#===============================================================================================user


def createUser(request):
    # db=TinyDB('db2.json')
    return render(request,'home/createUser.html')

def saveUser(request):
    # db=TinyDB('db2.json')
    user_name= request.POST.get("user_name")
    password = request.POST.get("password")
    contact_no= request.POST.get("contact_no")
    email= request.POST.get("email")
    status= request.POST.get("status")
    created_date=request.POST.get("created_date")
    # m=[{'user_name':user_name,'password':password,'contact_no':contact_no,'email':email,'status':status,'created_date':created_date}]
    # db.insert_multiple(m)
    b=user()
    b.user_name=user_name;
    b.email=email;
    b.contact_no=contact_no;
    b.user_password=password;
    b.status=status;
    b.created_date=created_date
    # b.created_date=datetime.datetime.now()
    b.save()
    return render(request,'home/createUser.html')



def showUser(request):
    # db=TinyDB('db2.json')
    # data = db.all()
    data = user.objects.all().values()
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


#========================================================================================================Strategy



def createStrategy(request):
    return render(request,'home/createStrategy.html')

def saveStrategy(request):
    strategy_name= request.POST.get("strategy_name")
    strategy_type = request.POST.get("strategy_type")
    status= request.POST.get("status")
    created_date=datetime.datetime.now()
    # m=[{'strategy_name':strategy_name,'strategy_type':strategy_type,'status':status,'created_date':created_date}]
    # db.insert_multiple(m)
    b=strategy()
    b.strategy_name=strategy_name;
    b.strategy_type=strategy_type;
    b.status=status;
    b.created_date = created_date
    # b.created_date=datetime.datetime.now()
    b.save()
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



#=========================================================================================================trading account

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


#=================================================================================================================input views
def createinput(request):
    return render(request , "home/input.html")
def saveinput(request):
    u = Input()
    orb_range_candle_time = request.POST.get("orb_range_candle_time")
    or_breakout_candle_time = request.POST.get("or_breakout_candle_time")
    orb_ma_h = request.POST.get("orb_ma_h")
    orb_ma_l = request.POST.get("orb_ma_l")
    orb_range_start_time = request.POST.get("orb_range_start_time")
    orb_retracement_time = request.POST.get("orb_retracement_time")
    hl_difference_points = request.POST.get("hl_difference_points")
    ttoken = request.POST.get("ttoken")
    moving_avg_rows = request.POST.get("moving_avg_rows")
    or_breakout_range_point_diff = request.POST.get("or_breakout_range_point_diff")
    data=Inputdb.all()
    if len(data)>0:
        for x in data:
            id=int(x.get("id"))+1
        data=[{"id":id,"orb_range_candle_time":orb_range_candle_time,"or_breakout_candle_time":or_breakout_candle_time,
               "orb_ma_h":orb_ma_h,"orb_ma_l":orb_ma_l,"orb_range_start_time":orb_range_start_time,
               "orb_retracement_time":orb_retracement_time,"hl_difference_points":hl_difference_points,"ttoken":ttoken,
               "moving_avg_rows":moving_avg_rows,"or_breakout_range_point_diff":or_breakout_range_point_diff}]
    else:
        data = [{"id":1,"orb_range_candle_time":orb_range_candle_time,"or_breakout_candle_time":or_breakout_candle_time,
                 "orb_ma_h":orb_ma_h,"orb_ma_l":orb_ma_l,"orb_range_start_time":orb_range_start_time,
                 "orb_retracement_time":orb_retracement_time,"hl_difference_points":hl_difference_points,"ttoken":ttoken,
                 "moving_avg_rows":moving_avg_rows,"or_breakout_range_point_diff":or_breakout_range_point_diff}]
    Inputdb.insert_multiple(data)
    return render(request , "home/input.html" , )

def showinput(request):
    q = Query()
    data = Inputdb.all()
    return render(request , 'home/showinput.html',{"data":data})

def updateinput(request,id):
    q = Query()
    data = Inputdb.search(q.id==id)
    data=data[0]
    return render(request,"home/updateinput.html",{"data":data})
def update_saveinput(request):
    u = Input()
    id = request.POST.get("id")
    orb_range_candle_time = request.POST.get("orb_range_candle_time")
    or_breakout_candle_time = request.POST.get("or_breakout_candle_time")
    orb_ma_h = request.POST.get("orb_ma_h")
    orb_ma_l = request.POST.get("orb_ma_l")
    orb_range_start_time = request.POST.get("orb_range_start_time")
    orb_retracement_time = request.POST.get("orb_retracement_time")
    hl_difference_points = request.POST.get("hl_difference_points")
    ttoken = request.POST.get("ttoken")
    moving_avg_rows = request.POST.get("moving_avg_rows")
    or_breakout_range_point_diff = request.POST.get("or_breakout_range_point_diff")
    data = {"orb_range_candle_time":orb_range_candle_time,"or_breakout_candle_time":or_breakout_candle_time,
            "orb_ma_h":orb_ma_h,"orb_ma_l":orb_ma_l,"orb_range_start_time":orb_range_start_time,
            "orb_retracement_time":orb_retracement_time,"hl_difference_points":hl_difference_points,"ttoken":ttoken,
            "moving_avg_rows":moving_avg_rows,"or_breakout_range_point_diff":or_breakout_range_point_diff}
    q = Query()
    Inputdb.update(data,q.id==int(id))
    return HttpResponseRedirect("/showinput")

def deleteinput(request,id):
    # Inputdb=TinyDB('Inputdb.json')
    b=Query()
    Inputdb.remove(b.id==id)
    # delete1 = Broker.objects.get(id=id)
    # delete1.delete()
    return HttpResponseRedirect("/showinput")

#==============================================================================================broker


def createBroker(request):
    return render(request,'home/createBroker.html')

def saveBroker(request):
    broker_name = request.POST.get("broker_name")
    broker_logo = request.POST.get("logo")
    created_date=request.POST.get("created_date")
    # b=Broker()
    # b.broker_name=broker_name
    # b.broker_logo=broker_logo
    # b.created_date=created_date
    brokers=Brokerdb.table("brokers")
    data={'broker_name':broker_name,'broker_logo':broker_logo,'created_date':created_date}
    brokers.insert(data)
    # b.save()
    return render(request,'home/createBroker.html')

def showBroker(request):
    q = Query()
    brokers=Brokerdb.table("brokers")
    # data = Broker.objects.all().values()
    data=brokers.all()
    return render(request,"home/showBroker.html",{"data": data})
def update_saveBroker(request):
    broker=Query()
    # u = Broker()
    id=request.POST.get("id")
    Brokerdb.search(broker.id==id)
    broker_name= request.POST.get("broker_name")
    broker_logo=request.POST.get("logo")
    updated_date=request.POST.get("updated_date")
    data={'broker_name':broker_name,'broker_logo':broker_logo,'updated_date':updated_date}
    Brokerdb.insert_multiple(data)
    # u.broker_name = broker_name
    # u.broker_logo = broker_logo
    # u.updated_date = updated_date
    # u.save()
    return HttpResponseRedirect("/showBroker")
def deleteBroker(request,id):
    broker=Query()
    Brokerdb.remove(broker.id==id)
    # delete1 = Broker.objects.get(id=id)
    # delete1.delete()
    return HttpResponseRedirect("/showBroker")

def updateBroker(request,id):
    broker=Query()
    # data=Broker.objects.get(id=id)
    data=Brokerdb.search(broker.id==id)
    return render(request,"home/updateBroker.html",{"data":data})


#=========================================================================================================================ORB

# def ticker(request):
#     calc(request)
#     return HttpResponse("avsd")
# def calc(request):
#     tradelogic = TradeLogic()
#     i=0
#     while True:
#         i=i+1
#         if i > 10:
#             break
#         tradelogic.top_range_breakout(request)
#         time.sleep(1)

