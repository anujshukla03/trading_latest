# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('homepage/', views.homepage, name='homepage'),
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),


######3333333333=======================================================================================broker

    path('createBroker/', views.createBroker, name='createBroker'),
    path('saveBroker/', views.saveBroker, name='saveBroker'),
    path('showBroker/',views.showBroker, name='showBroker'),
    path('deleteBroker/<int:id>',views.deleteBroker,name='deleteBroker'),
    path('update_saveBroker/',views.update_saveBroker,name='update_saveBroker'),
    path('updateBroker/<int:id>',views.updateBroker,name='updateBroker'),
    
######3333333333=======================================================================================user
 
     path('createUser/', views.createUser, name='createUser'),
    path('saveUser/', views.saveUser, name='saveUser'),
    path('showUser/',views.showUser, name='showUser'),
    path('deleteUser/<int:id>',views.deleteUser,name='deleteUser'),
    path('update_saveUser/',views.update_saveUser,name='update_saveUser'),
    path('updateUser/<int:id>',views.updateUser,name='updateUser'),


######3333333333=======================================================================================strategy
 
     path('createStrategy/', views.createStrategy, name='createStrategy'),
    path('saveStrategy/', views.saveStrategy, name='saveStrategy'),
    path('showStrategy/',views.showStrategy, name='showStrategy'),
    path('deleteStrategy/<int:id>',views.deleteStrategy,name='deleteStrategy'),
    path('update_saveStrategy/',views.update_saveStrategy,name='update_saveStrategy'),
    path('updateStrategy/<int:id>',views.updateStrategy,name='updateStrategy'),


#=====================================================================================================trading account

    path('createTradingAccount/',views.createTradingAccount, name='createTradingAccount'),
    path('saveTradingAccount/',views.saveTradingAccount, name='saveTradingAccount'),
    path('showTradingAccount/',views.showTradingAccount, name='showTradingAccount'),
    path('update_saveTradingAccount/',views.update_saveTradingAccount, name='update_saveTradingAccount'),
    path('deleteTradingAccount/<int:id>',views.deleteTradingAccount, name='deleteTradingAccount'),
    path('updateTradingAccount/<int:id>',views.updateTradingAccount, name='updateTradingAccount'),
]
