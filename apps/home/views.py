# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import datetime, json
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
from django.conf import settings
from django.contrib.auth import login as auth_login

# from apps.home.models import Broker, user,strategy,TradingAccount,Input
from tinydb import TinyDB, Query
from json import dumps
from apps.home.Constants import BASE_URL
from apps.home.kite_init import kiteInit
from apps.home.itmBreakoutAlert import breakoutLogic
from apps.home.kite_trade import *
import datetime
import json
import time
from django.core.files.storage import FileSystemStorage
from threading import Timer

Inputdb = TinyDB("Inputdb.json")
inputs = Inputdb.table("inputs")

Brokerdb = TinyDB("Brokerdb.json")
brokers = Brokerdb.table("brokers")

Userdb = TinyDB("Userdb.json")

StrategyDb = TinyDB("StrategyDb.json")

Trading_AccountDb = TinyDB("Trading_AccountDb.json")

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
    return render(request, "home/index.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("Username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cfm_pass = request.POST.get("cfm_pass")

        if password != cfm_pass:
            messages.error(request, "Your password and confirm password are not same.")

        else:
            my_user = User.objects.create_user(username, email, password)
            my_user.save()
            return redirect("home/login")
    return render(request, "accounts/register.html")


def login(request):
    tradelogic = kiteInit()
    breakout_l = breakoutLogic()
    if request.method == "POST":
        name = request.POST.get("name")
        pass1 = request.POST.get("password")
        user = authenticate(request, username=name, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect("/homepage")
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
    return render(request, "home/login.html")


def profile(request):
    return render(request, "home/profile.html")


# =================================================================================================================input views
def createinput(request):
    return render(request, "home/input.html")


def saveinput(request):
    strategy_name = request.POST.get("strategy_name")
    strategy_id = request.POST.get("strategy_id")
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
    data = inputs.all()
    if len(data) > 0:
        for x in data:
            id = int(x.get("id")) + 1
        data = [
            {
                "id": id,
                "strategy_name":strategy_name,
                "strategy_id":strategy_id,
                "orb_range_candle_time": orb_range_candle_time,
                "or_breakout_candle_time": or_breakout_candle_time,
                "orb_ma_h": orb_ma_h,
                "orb_ma_l": orb_ma_l,
                "orb_range_start_time": orb_range_start_time,
                "orb_retracement_time": orb_retracement_time,
                "hl_difference_points": hl_difference_points,
                "ttoken": ttoken,
                "moving_avg_rows": moving_avg_rows,
                "or_breakout_range_point_diff": or_breakout_range_point_diff,
            }
        ]
    else:
        data = [
            {
                "id": 1,
                "strategy_name":strategy_name,
                "strategy_id":strategy_id,
                "orb_range_candle_time": orb_range_candle_time,
                "or_breakout_candle_time": or_breakout_candle_time,
                "orb_ma_h": orb_ma_h,
                "orb_ma_l": orb_ma_l,
                "orb_range_start_time": orb_range_start_time,
                "orb_retracement_time": orb_retracement_time,
                "hl_difference_points": hl_difference_points,
                "ttoken": ttoken,
                "moving_avg_rows": moving_avg_rows,
                "or_breakout_range_point_diff": or_breakout_range_point_diff,
            }
        ]
    inputs.insert_multiple(data)
    return render(
        request,
        "home/input.html",
    )


def showinput(request):
    q = Query()
    data = inputs.all()
    return render(request, "home/showinput.html", {"data": data})


def updateinput(request, id):
    q = Query()
    data = inputs.search(q.id == id)
    data = data[0]
    return render(request, "home/updateinput.html", {"data": data})


def update_saveinput(request):
    id = request.POST.get("id")
    strategy_name = request.POST.get("strategy_name")
    strategy_id = request.POST.get("strategy_id")
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
    data = {
        "strategy_name":strategy_name,
        "strategy_id":strategy_id,
        "orb_range_candle_time": orb_range_candle_time,
        "or_breakout_candle_time": or_breakout_candle_time,
        "orb_ma_h": orb_ma_h,
        "orb_ma_l": orb_ma_l,
        "orb_range_start_time": orb_range_start_time,
        "orb_retracement_time": orb_retracement_time,
        "hl_difference_points": hl_difference_points,
        "ttoken": ttoken,
        "moving_avg_rows": moving_avg_rows,
        "or_breakout_range_point_diff": or_breakout_range_point_diff,
    }
    q = Query()
    inputs.update(data, q.id == int(id))
    return HttpResponseRedirect("/showinput")


def deleteinput(request, id):
    # Inputdb=TinyDB('Inputdb.json')
    b = Query()
    inputs.remove(b.id == id)
    # delete1 = Broker.objects.get(id=id)
    # delete1.delete()
    return HttpResponseRedirect("/showinput")


#===========================================================================================================broker
def showBroker(request):
    data = brokers.all()
    print(data[0]["broker_name"])
    print(settings.MEDIA_ROOT)
    return render(request, "home/showBroker.html", {"data": data, "settings":settings})


def createBroker(request):
    if request.method == "POST":
        broker_name = request.POST["broker_name"]
        created_date = request.POST["created_date"]
        broker_logo = request.FILES["broker_logo"]
        fs = FileSystemStorage()
        filename = fs.save(broker_logo.name, broker_logo)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)

        brokers.insert(
            {
                "broker_name": broker_name,
                "broker_logo": uploaded_file_url,
                "created_date": created_date,
            }
        )
        return redirect("/showBroker")
    return render(request, "home/createBroker.html")


def updateBroker(request, id):
    data = brokers.get(doc_id=id)
    if request.method == "POST":
        broker_name = request.POST["broker_name"]
        created_date = request.POST["created_date"]
        broker_logo = request.FILES["broker_logo"]
        fs = FileSystemStorage()
        filename = fs.save(broker_logo.name, broker_logo)  
        uploaded_file_url = fs.url(filename)
        brokers.update(
            {
                "id": id,
                "broker_name": broker_name,
                "broker_logo": uploaded_file_url,
                "created_date": created_date,
            },
            doc_ids=[id],
        )
        return redirect("/showBroker")
    return render(request, "home/updateBroker.html", {"data": data})


def deleteBroker(request, id):
    brokers.remove(doc_ids=[id])
    return redirect("/showBroker")

#=================================================================================================================user

users = Userdb.table("users")
def createUser(request):
    if request.method == "POST":
        user_name = request.POST["user_name"]
        password = request.POST["password"]
        contact_no = request.POST["contact_no"]
        email = request.POST["email"]
        status = request.POST["status"]
        created_date = request.POST["created_date"]
        users.insert(
            {
                "user_name": user_name,
                "password": password,
                "contact_no": contact_no,
                "email": email,
                "status": status,
                "created_date": created_date,
            }
        )
        return redirect("/showUser")    
    return render(request, "home/createUser.html")


def showUser(request):
    data = users.all()
    return render(request, "home/showUser.html", {"data": data})

def updateUser(request, id):
    data = users.get(doc_id=id)
    if request.method == "POST":
        user_name = request.POST["user_name"]
        password = request.POST["password"]
        contact_no = request.POST["contact_no"]
        email = request.POST["email"]
        status = request.POST["status"]
        updated_date = request.POST["updated_date"]
        users.update(
            {
                "id": id,
                "user_name": user_name,
                "password": password,
                "contact_no": contact_no,
                "email": email,
                "status": status,
                "updated_date": updated_date,
            },
            doc_ids=[id],
        )
        return redirect("/showUser")
    return render(request, "home/updateUser.html", {"data": data})

def deleteUser(request, id):
    users.remove(doc_ids=[id])
    return redirect("/showUser")



#================================================================================================strategies
strategies = StrategyDb.table("strategies")

def createStrategy(request):
    if request.method == "POST":
        strategy_name = request.POST["strategy_name"]
        strategy_type = request.POST["strategy_type"]
        status = request.POST["status"]

        strategies.insert(
            {
                "strategy_name": strategy_name,
                "strategy_type": strategy_type,
                "status": status,
            }
        )
        return redirect("/showStrategy")
    return render(request, "home/createStrategy.html")


def showStrategy(request):
    data = strategies.all()
    return render(request, "home/showStrategy.html", {"data": data})


def deleteStrategy(request, id):
    strategies.remove(doc_ids=[id])
    return redirect("/showStrategy")


def updateStrategy(request, id):
    data = strategies.get(doc_id=id)
    if request.method == "POST":
        strategy_name = request.POST["strategy_name"]
        strategy_type = request.POST["strategy_type"]
        status = request.POST["status"]

        strategies.update(
            {
                "id": id,
                "strategy_name": strategy_name,
                "strategy_type": strategy_type,
                "status": status,
            },
            doc_ids=[id],
        )
        return redirect("/showStrategy")
    return render(request, "home/updateStrategy.html", {"data": data})


#===========================================================================================================trading Acoount

tradingAc = Trading_AccountDb.table("tradingAc")


def createTradingAccount(request):
    if request.method == "POST":
        UserID = request.POST["UserID"]
        BrokerID = request.POST["BrokerID"]
        Zerodha_UserID = request.POST["Zerodha_UserID"]
        Zerodha_Password = request.POST["Zerodha_Password"]
        Zerodha_TOTP_Key = request.POST["Zerodha_TOTP_Key"]
        IIFL_Email_id = request.POST["IIFL_Email_id"]
        IIFL_Contact_Number = request.POST["IIFL_Contact_Number"]
        IIFL_App_Source = request.POST["IIFL_App_Source"]
        IIFL_User_Key = request.POST["IIFL_User_Key"]
        IIFL_User_id = request.POST["IIFL_User_id"]
        IIFL_Password = request.POST["IIFL_Password"]
        IIFL_Encry_Key = request.POST["IIFL_Encry_Key"]
        IIFL_OcpApimSubscription = request.POST["IIFL_OcpApimSubscription"]
        IIFL_My2Pin = request.POST["IIFL_My2Pin"]
        IIFL_ClientCode = request.POST["IIFL_ClientCode"]
        IIFL_cpass = request.POST["IIFL_cpass"]
        Kotak_Key = request.POST["Kotak_Key"]
        Kotak_Secret = request.POST["Kotak_Secret"]
        TA_Status = request.POST["TA_Status"]

        tradingAc.insert(
            {
                "UserID": UserID,
                "BrokerID": BrokerID,
                "Zerodha_UserID": Zerodha_UserID,
                "Zerodha_Password": Zerodha_Password,
                "Zerodha_TOTP_Key": Zerodha_TOTP_Key,
                "IIFL_Email_id": IIFL_Email_id,
                "IIFL_Contact_Number": IIFL_Contact_Number,
                "IIFL_App_Source": IIFL_App_Source,
                "IIFL_User_Key": IIFL_User_Key,
                "IIFL_User_id": IIFL_User_id,
                "IIFL_Password": IIFL_Password,
                "IIFL_Encry_Key": IIFL_Encry_Key,
                "IIFL_OcpApimSubscription": IIFL_OcpApimSubscription,
                "IIFL_My2Pin": IIFL_My2Pin,
                "IIFL_ClientCode": IIFL_ClientCode,
                "IIFL_cpass": IIFL_cpass,
                "Kotak_Key":Kotak_Key,
                "Kotak_Secret":Kotak_Secret,
                "TA_Status": TA_Status,
            }
        )
        return redirect("/showTradingAccount")
    return render(request, "home/createTradingAccount.html")


def showTradingAccount(request):
    data = tradingAc.all()
    return render(request, "home/showTradingAccount.html", {"data": data})


def deleteTradingAccount(request, id):
    tradingAc.remove(doc_ids=[id])
    return redirect("/showTradingAccount")

def updateTradingAccount(request, id):
    data = tradingAc.get(doc_id=id)
    if request.method == "POST":
        UserID = request.POST["UserID"]
        BrokerID = request.POST["BrokerID"]
        Zerodha_UserID = request.POST["Zerodha_UserID"]
        Zerodha_Password = request.POST["Zerodha_Password"]
        Zerodha_TOTP_Key = request.POST["Zerodha_TOTP_Key"]
        IIFL_Email_id = request.POST["IIFL_Email_id"]
        IIFL_Contact_Number = request.POST["IIFL_Contact_Number"]
        IIFL_App_Source = request.POST["IIFL_App_Source"]
        IIFL_User_Key = request.POST["IIFL_User_Key"]
        IIFL_User_id = request.POST["IIFL_User_id"]
        IIFL_Password = request.POST["IIFL_Password"]
        IIFL_Encry_Key = request.POST["IIFL_Encry_Key"]
        IIFL_OcpApimSubscription = request.POST["IIFL_OcpApimSubscription"]
        IIFL_My2Pin = request.POST["IIFL_My2Pin"]
        IIFL_ClientCode = request.POST["IIFL_ClientCode"]
        IIFL_cpass = request.POST["IIFL_cpass"]
        TA_Status = request.POST["TA_Status"]

        tradingAc.update(
            {
                "id": id,
                "UserID": UserID,
                "BrokerID": BrokerID,
                "Zerodha_UserID": Zerodha_UserID,
                "Zerodha_Password": Zerodha_Password,
                "Zerodha_TOTP_Key": Zerodha_TOTP_Key,
                "IIFL_Email_id": IIFL_Email_id,
                "IIFL_Contact_Number": IIFL_Contact_Number,
                "IIFL_App_Source": IIFL_App_Source,
                "IIFL_User_Key": IIFL_User_Key,
                "IIFL_User_id": IIFL_User_id,
                "IIFL_Password": IIFL_Password,
                "IIFL_Encry_Key": IIFL_Encry_Key,
                "IIFL_OcpApimSubscription": IIFL_OcpApimSubscription,
                "IIFL_My2Pin": IIFL_My2Pin,
                "IIFL_ClientCode": IIFL_ClientCode,
                "IIFL_cpass": IIFL_cpass,
                "TA_Status": TA_Status,
            },
            doc_ids=[id],
        )
        return redirect("/showTradingAccount")
    return render(request, "home/updateTradingAccount.html", {"data": data})
