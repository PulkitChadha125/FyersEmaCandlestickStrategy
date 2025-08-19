import pandas as pd
import datetime  # full module
import polars as pl
import polars_talib as plta
import json
# from datetime import datetime, timedelta
import time
import traceback
import sys
from FyresIntegration import *

def normalize_time_to_timeframe(current_time, timeframe_minutes):
    """
    Normalize time to the specified timeframe interval.
    
    Args:
        current_time: datetime object (current time)
        timeframe_minutes: int (timeframe in minutes, e.g., 5 for 5-minute intervals)
    
    Returns:
        datetime: normalized time rounded down to the nearest timeframe interval
    """
    # Calculate how many complete timeframe intervals have passed
    intervals_passed = current_time.minute // timeframe_minutes
    
    # Calculate the normalized minute (round down to nearest timeframe)
    normalized_minute = intervals_passed * timeframe_minutes
    
    # Create normalized time (set seconds and microseconds to 0)
    normalized_time = current_time.replace(
        minute=normalized_minute, 
        second=0, 
        microsecond=0
    )
    
    return normalized_time

def calculate_stop_loss_time(timeframe_minutes):
    """
    Calculate stop loss time by normalizing current time to timeframe and adding the timeframe.
    
    Args:
        timeframe_minutes: int (timeframe in minutes from FyersTf)
    
    Returns:
        datetime: stop loss time (normalized current time + timeframe)
    """
    current_time = datetime.now()
    
    # Normalize to the specified timeframe
    normalized_time = normalize_time_to_timeframe(current_time, timeframe_minutes)
    
    # Add the timeframe to get the stop loss time
    stop_loss_time = normalized_time + timedelta(minutes=timeframe_minutes)
    
    return stop_loss_time



def get_api_credentials_Fyers():
    credentials_dict_fyers = {}
    try:
        df = pd.read_csv('FyersCredentials.csv')
        for index, row in df.iterrows():
            title = row['Title']
            value = row['Value']
            credentials_dict_fyers[title] = value
    except pd.errors.EmptyDataError:
        print("The CSV FyersCredentials.csv file is empty or has no data.")
    except FileNotFoundError:
        print("The CSV FyersCredentials.csv file was not found.")
    except Exception as e:
        print("An error occurred while reading the CSV FyersCredentials.csv file:", str(e))
    return credentials_dict_fyers

#get equity symbols
def get_equity_symbols():
    url = "https://public.fyers.in/sym_details/NSE_CM_sym_master.json"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame.from_dict(data, orient='index')
    return df



def delete_file_contents(file_name):
    try:
        # Open the file in write mode, which truncates it (deletes contents)
        with open(file_name, 'w') as file:
            file.truncate(0)
        print(f"Contents of {file_name} have been deleted.")
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

          

def write_to_order_logs(message):
    with open('OrderLog.txt', 'a') as file:  # Open the file in append mode
        file.write(message + '\n')

def get_user_settings():
    global result_dict, instrument_id_list, Equity_instrument_id_list, Future_instrument_id_list, FyerSymbolList
    from datetime import datetime
    import pandas as pd

    delete_file_contents("OrderLog.txt")

    try:
        csv_path = 'TradeSettings.csv'
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()

        result_dict = {}
        
        FyerSymbolList = []

        for index, row in df.iterrows():
            symbol = row['Symbol']
            # expiry = row['EXPIERY']  # Format: 29-05-2025

            # Convert expiry to API format: DDMonYYYY (e.g., 29May2025)
    #         expiry_api_format = datetime.strptime(expiry, "%d-%m-%Y").strftime("%d%b%Y")
    #         expiry_date = datetime.strptime(expiry, "%d-%m-%Y")
    #         try:
    # # Parse '26-06-2025' → datetime object
    #             expiry_date = datetime.strptime(expiry, '%d-%m-%Y')
    # # Format as '25JUN'
    #             new_date_string = expiry_date.strftime('%y%b').upper()
    #             fyers_fut_symbol = f"NSE:{symbol}{new_date_string}FUT"
            # except ValueError as e:
            #     print(f"[ERROR] Failed to parse expiry for symbol {symbol}: {expiry}. Error: {e}")
            #     fyers_fut_symbol = None

            symbol_dict = {
                "Symbol": symbol, "unique_key": f"{symbol}_",
                # "Expiry": expiry,
                "Quantity": int(row['Quantity']),# Add tick size to symbol dictionary
   
                "MA1": int(row['MA1']),
                "StartTime": datetime.strptime(row["StartTime"], "%H:%M:%S").time(),
                "StopTime": datetime.strptime(row["Stoptime"], "%H:%M:%S").time(),
                "ma1Val": None, "last_run_time": None,
                "ActualDiff": None, "Trade": None, "TargetExecuted": False,
                "EQltp": None, "Futltp": None, "buytargetvalue": None,"buystop":None,"sellstop":None,
                "selltargetvalue": None,"firstclose":None,"secondclose":None,
                "firsthigh":None,"firstlow":None,"secondhigh":None,"secondlow":None,
                "last_high": None, "last_low": None, "SquareOffExecuted": False,
                "Series": None, "Candletimestamp": None,
                "FyersTf": row['FyersTf'],
                "FyresSymbol": f"NSE:{symbol}-EQ",
                "FyresLtp": None,"StopLossExecuted":False,"RiskAmount":row['RiskAmount'],
                "FyersFutLtp": None,"FutAsk": None,"FutBid": None,"StopLossTime":datetime.now(),
            
            }

            result_dict[symbol_dict["unique_key"]] = symbol_dict

            

            FyerSymbolList.append(symbol_dict["FyresSymbol"])
           


        print("result_dict: ", result_dict)
        print("-" * 50)
       

    except Exception as e:
        print("Error happened in fetching symbol", str(e))



def UpdateData():
    global result_dict

    for symbol, ltp in shared_data.items(): 
        for key, value in result_dict.items():
            if value.get('FyresSymbol') == symbol:
                value['FyresLtp'] = float(ltp)
                print(f"[EQ] Updated {symbol} with LTP: {ltp}")
                break  # Optional: skip if you assume each symbol is unique
           



def main_strategy():
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=10)

        start_time_str = start_date.strftime("%b %d %Y 090000")
        end_time_str = end_date.strftime("%b %d %Y 153000")

        now = datetime.now()
        now_time = now.time()
        UpdateData()
        time.sleep(1)
        fetch_start = time.time()
        for unique_key, params in result_dict.items():
            # initialize loop-specific variables to avoid UnboundLocalError
            symbol_name = params["Symbol"]
            print("symbol_name: ",symbol_name,"time: ",now_time)
            if not (params["StartTime"] <= now_time <= params["StopTime"]):
                continue
            

            if params.get("last_run_time") is None or datetime.now() >= params["last_run_time"]:
                try:
                    symbol_name = params["Symbol"]
                    fohlc_data=fetchOHLC(symbol=params["FyresSymbol"],tf=params["FyersTf"])
                    # last_candle_fyres = fohlc_data.iloc[-1]
                    Candletimestamp = pd.to_datetime(fohlc_data['date'].iloc[-1])
                    # second_last_candle_fyres = fohlc_data.iloc[-2]
                except Exception as e:
                    print(f"Error fetching OHLC data for {symbol_name}: {str(e)}")
                    traceback.print_exc()
                    continue 


                fohlc_data = fohlc_data.astype({
                    col: "float64" if fohlc_data[col].dtype.name.startswith("Float") else
                        "int64" if fohlc_data[col].dtype.name.startswith("Int") else
                        fohlc_data[col].dtype
                    for col in fohlc_data.columns
                })
                pl_df = pl.from_pandas(fohlc_data)
                    # Calculate EMA using values from settings (MA1 and MA2)
                pl_df = pl_df.with_columns([
                        pl.col("close").ta.ema(int(params["MA1"])).alias(f"ema_{params['MA1']}"),
                    ])
                
                    # Save last EMA values into result_dict
                #     "firstclose":None,"secondclose":None,
                # "firsthigh":None,"firstlow":None,"secondhigh":None,"secondlow":None,

                params["firstclose"] = pl_df.select("close")[-2, 0]
                params["firstopen"] = pl_df.select("open")[-2, 0]
                params["firsthigh"] = pl_df.select("high")[-2, 0]
                params["firstlow"] = pl_df.select("low")[-2, 0]
                params["secondclose"] = pl_df.select("close")[-3, 0]
                params["secondopen"] = pl_df.select("open")[-3, 0]
                params["secondhigh"] = pl_df.select("high")[-3, 0]
                params["secondlow"] = pl_df.select("low")[-3, 0]

                params["ma1Val"] = pl_df.select(f"ema_{params['MA1']}")[-2, 0]
                params["ma2Val"] = pl_df.select(f"ema_{params['MA1']}")[-3, 0]
                
                 

                    # Show first few rows
                fetch_end = time.time()
                fetch_duration = fetch_end - fetch_start
                Candletimestamp = pd.to_datetime(fohlc_data['date'].iloc[-1]).replace(tzinfo=None)
                params["Candletimestamp"] = Candletimestamp
                params["last_run_time"] = Candletimestamp + timedelta(minutes=params["FyersTf"])
                params["last_run_time"] = params["last_run_time"].replace(tzinfo=None)

                # print fetch timing and last close right after fetch
                print(f"Symbol: {symbol_name}, Next run time: {params['last_run_time']}, Total Time taken by api to fetch data: {fetch_duration:.2f} seconds")

                
            # divider line
            print("=== First Candle ===")
            print(f"First Close: {params['firstclose']}")
            print(f"First Open: {params['firstopen']}")
            print(f"First High: {params['firsthigh']}")
            print(f"First Low: {params['firstlow']}")

            print("\n=== Second Candle ===")
            print(f"Second Close: {params['secondclose']}")
            print(f"Second Open: {params['secondopen']}")
            print(f"Second High: {params['secondhigh']}")
            print(f"Second Low: {params['secondlow']}")

            print("\n=== EMA Values ===")
            print(f"EMA (MA1) Value at -2: {params['ma1Val']}")
            print(f"EMA (MA1) Value at -3: {params['ma2Val']}")

            print("-" * 50)
            print("Trade: ",params["Trade"])
            print("TargetExecuted: ",params["TargetExecuted"])
            print("StopLossExecuted: ",params["StopLossExecuted"])
            print("Buy Target: ",params["buytargetvalue"])
            print("Buy Stop: ",params["buystop"])
            print("Sell Target: ",params["selltargetvalue"])
            print("Sell Stop: ",params["sellstop"])
            print("FyresLtp: ",params["FyresLtp"])

            
               
            if datetime.now() >= params['StopLossTime']and params["Trade"] is None and  params["firstclose"] >params["ma1Val"] and params["secondclose"] > params["ma2Val"] and params["firstclose"] > params["firstopen"] and params["secondclose"] > params["secondopen"] and params["FyresLtp"]>=params["firsthigh"]:
                print(f"Buy Signal for {symbol_name}")
                params["Trade"] = "BUY"
                params["TargetExecuted"] = False
                params["StopLossExecuted"] = False
                params["buystop"]=min(params["firstlow"],params["secondlow"])
                FyresLtp=params["FyresLtp"]
                params["buytargetvalue"]=FyresLtp-params["buystop"]
                params["buytargetvalue"]=FyresLtp+params["buytargetvalue"]
                lotsize= params["RiskAmount"]/(FyresLtp-params["buystop"])
                place_order(symbol=params["FyresSymbol"],quantity=params["Quantity"],type=1,side=1,price=params["FyresLtp"])
                print("Buy Signal for ",symbol_name," at ",FyresLtp," with stop loss ",params["buystop"]," and target ",params["buytargetvalue"])
                write_to_order_logs(f"{datetime.now()} Buy Signal for {symbol_name} at {FyresLtp} with stop loss {params['buystop']} and target {params['buytargetvalue']}, risk based qty: {lotsize}")
            
            if datetime.now() >= params['StopLossTime'] and params["Trade"] is None and params["firstclose"] <params["ma1Val"] and params["secondclose"] < params["ma2Val"]  and params["firstclose"] < params["firstopen"] and params["secondclose"] < params["secondopen"] and params["FyresLtp"]<=params["firstlow"]:
                print(f"Sell Signal for {symbol_name}")
                params["Trade"] = "SELL"
                params["TargetExecuted"] = False
                params["StopLossExecuted"] = False
                params["sellstop"]=max(params["firsthigh"],params["secondhigh"])
                FyresLtp=params["FyresLtp"]
                params["selltargetvalue"]=params["sellstop"]-FyresLtp
                params["selltargetvalue"]=FyresLtp-params["selltargetvalue"]
                lotsize= params["RiskAmount"]/(params["sellstop"]-FyresLtp)
                place_order(symbol=params["FyresSymbol"],quantity=params["Quantity"],type=1,side=-1,price=params["FyresLtp"])
                print("Sell Signal for ",symbol_name," at ",FyresLtp," with stop loss ",params["sellstop"]," and target ",params["selltargetvalue"])
                write_to_order_logs(f"{datetime.now()} Sell Signal for {symbol_name} at {FyresLtp} with stop loss {params['sellstop']} and target {params['selltargetvalue']}, risk based qty: {lotsize}")
            

            # buy target 

            if params["Trade"] == "BUY" and params["TargetExecuted"] == False:
                if params["FyresLtp"]>=params["buytargetvalue"] and params["buytargetvalue"]>0:
                    print(f"Buy Target Executed for {symbol_name}")
                    params["TargetExecuted"] = True
                    params["buytargetvalue"]=0
                    params["buystop"]=0
                    params["Trade"] = "NOMORETRADE"
                    place_order(symbol=params["FyresSymbol"],quantity=params["Quantity"],type=1,side=-1,price=params["FyresLtp"])
                    print("Buy Target Executed for ",symbol_name," at ",params["FyresLtp"]," with stop loss ",params["sellstop"]," and target ",params["selltargetvalue"])
                    write_to_order_logs(f"{datetime.now()} Buy Target Executed for {symbol_name} at {params['FyresLtp']} with stop loss {params['buystop']} and target {params['buytargetvalue']}")
# buy stoploss
            if params["Trade"] == "BUY" and params["StopLossExecuted"] == False:
                if params["FyresLtp"]<=params["buystop"] and params["buystop"]>0:
                    print(f"Buy Stop Loss Executed for {symbol_name}")
                    params["StopLossExecuted"] = True
                    params["buystop"]=0
                    params["buytargetvalue"]=0
                    params["StopLossTime"] = calculate_stop_loss_time(params["FyersTf"])
                    params["StopLossTime"] = params["StopLossTime"].replace(tzinfo=None)                    
                    params["Trade"] = None
                    place_order(symbol=params["FyresSymbol"],quantity=params["Quantity"],type=1,side=-1,price=params["FyresLtp"])
                    print("Buy Stop Loss Executed for ",symbol_name," at ",params["FyresLtp"]," with stop loss ",params["sellstop"]," and target ",params["selltargetvalue"])
                    write_to_order_logs(f"{datetime.now()} Buy Stop Loss Executed for {symbol_name} at {params['FyresLtp']} with stop loss {params['buystop']} and target {params['buytargetvalue']},StopLossTime: {params['StopLossTime']}")

            # sell target
            if params["Trade"] == "SELL" and params["TargetExecuted"] == False:
                if params["FyresLtp"]<=params["selltargetvalue"] and params["selltargetvalue"]>0:
                    print(f"Sell Target Executed for {symbol_name}")
             
                    params["TargetExecuted"] = True
                    params["selltargetvalue"]=0
                    params["sellstop"]=0
                    params["Trade"] = "NOMORETRADE"
                    place_order(symbol=params["FyresSymbol"],quantity=params["Quantity"],type=1,side=1,price=params["FyresLtp"])
                    print("Sell Target Executed for ",symbol_name," at ",params["FyresLtp"]," with stop loss ",params["sellstop"]," and target ",params["selltargetvalue"])
                    write_to_order_logs(f"{datetime.now()} Sell Target Executed for {symbol_name} at {params['FyresLtp']} with stop loss {params['sellstop']} and target {params['selltargetvalue']}")
            
            # sell stoploss
            if params["Trade"] == "SELL" and params["StopLossExecuted"] == False:
                if params["FyresLtp"]>=params["sellstop"] and params["sellstop"]>0:
                    print(f"Sell Stop Loss Executed for {symbol_name}")
                    params["StopLossExecuted"] = True
                    params["sellstop"]=0
                    params["selltargetvalue"]=0
                    params["Trade"] = None
                    params["StopLossTime"] = calculate_stop_loss_time(params["FyersTf"])
                    params["StopLossTime"] = params["StopLossTime"].replace(tzinfo=None)

                    place_order(symbol=params["FyresSymbol"],quantity=params["Quantity"],type=1,side=1,price=params["FyresLtp"])
                    print("Sell Stop Loss Executed for ",symbol_name," at ",params["FyresLtp"]," with stop loss ",params["sellstop"]," and target ",params["selltargetvalue"])
                    write_to_order_logs(f"{datetime.now()} Sell Stop Loss Executed for {symbol_name} at {params['FyresLtp']} with stop loss {params['sellstop']} and target {params['selltargetvalue']},StopLossTime: {params['StopLossTime']}")

    except Exception as e:
        print("Error in main strategy:", str(e))
        traceback.print_exc()

if __name__ == "__main__":
    # # Initialize settings and credentials
    #   # <-- Add this line
    credentials_dict_fyers = get_api_credentials_Fyers()
    redirect_uri = credentials_dict_fyers.get('redirect_uri')
    client_id = credentials_dict_fyers.get('client_id')
    secret_key = credentials_dict_fyers.get('secret_key')
    grant_type = credentials_dict_fyers.get('grant_type')
    response_type = credentials_dict_fyers.get('response_type')
    state = credentials_dict_fyers.get('state')
    TOTP_KEY = credentials_dict_fyers.get('totpkey')
    FY_ID = credentials_dict_fyers.get('FY_ID')
    PIN = credentials_dict_fyers.get('PIN')
        # Automated login and initialization steps
    automated_login(client_id=client_id, redirect_uri=redirect_uri, secret_key=secret_key, FY_ID=FY_ID,
                                        PIN=PIN, TOTP_KEY=TOTP_KEY)
    get_user_settings()


        # Initialize Market Data API
    fyres_websocket(FyerSymbolList)
    time.sleep(5)
    while True:
            now =   datetime.now()   
            print(f"\nStarting main strategy at {datetime.now()}")
            main_strategy()
            time.sleep(2)
    
