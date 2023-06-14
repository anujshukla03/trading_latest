import pandas as pd
import numpy as np
import datetime
from typing import Optional, Tuple
import time
from datetime import datetime
from apps.home.kite_init import kiteInit
import math


class breakoutLogic():

    def __init__(self) -> None:
        self.kite = kiteInit()
        self.orb_range_candle_time = int(self.kite.getdata("orb_range_candle_time"))
        self.or_breakout_candle_time = int(self.kite.getdata("or_breakout_candle_time"))
        self.orb_ma_h = self.kite.getdata("orb_ma_h")
        self.orb_ma_l = self.kite.getdata("orb_ma_l")
        self.orb_range_start_time1 = str(self.kite.getdata("orb_range_start_time")+":00")
        self.orb_range_start_time = datetime.strptime(self.orb_range_start_time1, '%H:%M:%S').time()
        self.orb_retracement_time = self.kite.getdata("orb_retracement_time")
        self.hl_difference_points = self.kite.getdata("hl_difference_points")
        self.ttoken = self.kite.getdata("ttoken")
        self.moving_avg_rows = int(self.kite.getdata("moving_avg_rows"))
        self.or_breakout_range_point_diff = self.kite.getdata("or_breakout_range_point_diff")
    def historicalData(self,request):
        print(type(self.orb_range_start_time))
        # print(self.kite.historicalData(request, self.orb_range_start_time, self.orb_range_candle_time,self.ttoken, to_datetime= datetime.datetime.now()))
    def itmBreakoutAlert(self, request):
        ### Establish your KITE connection here and be ready to call kite.historical_data.
        # kite = Kite()
        # args = self.kite.input_params
        ### calculate number of days required for candle and add 5 day buffer.

        past_days_required = math.ceil(self.or_breakout_candle_time*self.moving_avg_rows/375)


        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        few_days_ago = today - datetime.timedelta(days=past_days_required+5)

        reliance_token = 91234
        df = self.kite.historicalData(request, few_days_ago, 'day', yesterday, reliance_token)
        last_trading_day = df.iloc[-1]['date'].date()

        last_few_trading_day_df = pd.DataFrame(self.kite.historical_data(request, few_days_ago,
                                                                    'minute', last_trading_day, self.ttoken))
        
        start_time = datetime.time(9, 15)
        end_time = datetime.time(15, 30)


        # Different States
        orb_range_checked = False

        while True:
            if start_time >= current_time():
                break

        # Check for Activator only in Trading Hours
        if start_time <= current_time() <= end_time:

            # waiting time is the time to wait till starttime + candle time has passed to get atleast one candle.
            waiting_time = add_mins_to_time(self.orb_range_start_time, self.orb_range_candle_time)

            while True:
                if current_time() > waiting_time:
                    break

            if current_time() >= waiting_time and orb_range_checked is False:

                orb_range_checked = True

                curr_day_df = pd.DataFrame(self.kite.historical_data(request, today, 'minute', 
                                                                     today, self.ttoken, oi=1))
                
                curr_day_after_start_time_df = curr_day_df[curr_day_df['date'].dt.time > self.orb_range_start_time]

                curr_day_after_start_time_df = resample_df(curr_day_after_start_time_df.copy(),
                                                            x_minutes = self.orb_range_candle_time)
                
                orb_first_candle = curr_day_after_start_time_df.head(1)
            
                top_range = orb_first_candle.loc[0, 'high']
                
                bottom_range = orb_first_candle.loc[0, 'low']
                
                hl_difference = top_range - bottom_range
                
                if hl_difference < self.hl_difference_points:
                    
                    return True, 'Range'
            
                    # itm_buy_sell_strategy()
                        
                else:
                    
                    while current_time() < end_time:
                        curr_day_df = pd.DataFrame(self.kite.historical_data(request, today, 'minute', today, self.ttoken))

                        or_breakout_df = resample_df(curr_day_df.copy(), self.or_breakout_candle_time)

                        or_breakout_df = pd.concat(last_few_trading_day_df, or_breakout_df)

                        or_breakout_df['ma_h'] = or_breakout_df['high'].rolling(window=self.moving_avg_rows).mean()
                        or_breakout_df['ma_l'] = or_breakout_df['low'].rolling(window=self.moving_avg_rows).mean()

                        or_breakout_df = or_breakout_df[or_breakout_df['date'] >= today]

                        top_activator_flag = self.test_top_range(request, or_breakout_df.copy(), top_range)

                        if top_activator_flag:
                            return True, 'top_range_breakout'
                        
                        bottom_activator_flag = self.test_bottom_range(request, or_breakout_df.copy(), bottom_range)

                        if bottom_activator_flag:
                            return True, 'bottom_range_breakout'

        return False


    def test_top_range(self, request, df, top_range):

        return False

        today = datetime.date.today()
        


        row = df.iloc[-1]  

        i = df.index[-1]

        c1 = df.loc[i-1, 'close'] or row['close'] > row['open']
        c2 = df.loc[i-1, 'close'] > row['ma_h'] and top_range
        c3 = row['close'] > row['ma_h'] and top_range
        c4 = row['ma_h'] > top_range
        
        if c1 and c2 and c3 and c4:
            
            c5 = row['close'] - top_range < self.or_breakout_range_point_diff
            
            if c5:
                return True
            
            else:
                end_of_retracement = current_time() + datetime.timedelta(minutes= self.orb_retracement_time)

                while current_time() <= end_of_retracement:
                    
                    time.sleep(60)

                    curr_day_df = pd.DataFrame(self.kite.historical_data(request, today, 'minute', today,  self.ttoken))

                    curr_day_df = resample_df(curr_day_df.copy(), self.or_breakout_candle_time)

                    pass 

                    # if breakout_in_retracement:
                    #     return True

        else:
            time.sleep(60)
        
        return False
            

    # def test_bottom_range(self, request, df, top_range):     
        return False



def resample_df(df: pd.DataFrame, x_minutes : Optional[int] = 15) -> pd.DataFrame:
    
    df.set_index('date', inplace=True)
    x_minutes = str(x_minutes) + 'T'
    resampled_df = df.resample(x_minutes, origin = 'start').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    })
    resampled_df.reset_index(inplace=True, drop=True)

    return resampled_df


def add_mins_to_time(time: datetime.time, mins: int) -> datetime.time:

    mins = datetime.timedelta(minutes=mins)
    current_date = datetime.datetime.now().date()
    start_datetime = datetime.datetime.combine(current_date, time)
    result = start_datetime + mins

    return result.time()


def current_time() -> datetime.time:
    curr_time = datetime.datetime.now().time()
    return curr_time


def itm_buy_sell_strategy():
    pass


    
