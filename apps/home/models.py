from django.db import models

class Broker(models.Model):
    broker_name=models.CharField(max_length=250)
    broker_logo=models.CharField(max_length=250,default="",null=True) 
    # created_date=models.DateTimeField(null=True,default="")
    # updated_date=models.DateTimeField(null=True,default="")
        
class user(models.Model):
    user_name=models.CharField(max_length=250 ,blank=True ,null=True)
    email=models.CharField(max_length=250,default="",null=True) 
    contact_no=models.CharField(max_length=250)
    user_password=models.CharField(max_length=250)
    status=models.CharField(max_length=250, default="")
    created_date=models.DateTimeField(null=True,default="")
    updated_date=models.DateTimeField(null=True,default="")
        
class strategy(models.Model):
    strategy_name=models.CharField(max_length=250 ,blank=True ,null=True)
    strategy_type=models.CharField(max_length=250,default="",null=True) 
    status=models.CharField(max_length=250, default="")
    created_date=models.DateTimeField(null=True,default="")
    updated_date=models.DateTimeField(null=True,default="")
        
class TradingAccount(models.Model):
    UserID = models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    BrokerID = models.ForeignKey(Broker, on_delete=models.CASCADE, null=True)
    Zerodha_UserID = models.CharField(max_length=250,null=True,default="")
    Zerodha_Password = models.CharField(max_length=250,null=True,default="")
    Zerodha_TOTP_Key = models.CharField(max_length=250,null=True,default="")
    IIFL_Email_id = models.CharField(max_length=250,null=True,default="")
    IIFL_Contact_Number = models.CharField(max_length=250,null=True,default="")
    IIFL_App_Source = models.CharField(max_length=250,null=True,default="")
    IIFL_User_Key = models.CharField(max_length=250,null=True,default="")
    IIFL_User_id = models.CharField(max_length=250,null=True,default="")
    IIFL_Password = models.CharField(max_length=250,null=True,default="")
    IIFL_Encry_Key = models.CharField(max_length=250,null=True,default="")
    IIFL_OcpApimSubscription = models.CharField(max_length=250,null=True,default="")
    IIFL_My2Pin = models.CharField(max_length=250,null=True,default="")
    IIFL_ClientCode = models.CharField(max_length=250,null=True,default="")
    IIFL_cpass = models.CharField(max_length=250,null=True,default="")
    Kotak_Key = models.CharField(max_length=250,null=True,default="")
    Kotak_Secret = models.CharField(max_length=250,null=True,default="")
    TA_Status = models.CharField(max_length=250,null=True,default="")
    TA_Created_Date = models.CharField(max_length=250,null=True,default="")
    Created_By = models.CharField(max_length=250,null=True,default="")
    Updated_Date = models.CharField(max_length=250,null=True,default="")
    Updated_By = models.CharField(max_length=250,null=True,default="")


class Input(models.Model):
    orb_range_candle_time=models.CharField(max_length=50,null=True,default="")
    or_breakout_candle_time=models.CharField(max_length=50,null=True,default="")
    orb_ma_h=models.CharField(max_length=10,null=True,default="")
    orb_ma_l=models.CharField(max_length=100,null=True,default="")
    orb_range_start_time = models.DateTimeField(max_length=20,null=True,default="")
    orb_retracement_time = models.CharField(max_length=20,null=True,default="")
    hl_difference_points = models.CharField(max_length=20,null=True,default="")
    ttoken = models.CharField(max_length=20,null=True,default="")
    moving_avg_rows = models.CharField(max_length=20,null=True,default="")
    or_breakout_range_point_diff = models.CharField(max_length=20,null=True,default="")
