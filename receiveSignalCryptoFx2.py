
#filewatcher from 
#https://www.michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-directory

#ccxt demo taught in https://quantlabs.net/academy/python-algo-trading-infrastructure-with-crypto-currency/

#REMEMBER THAT SIGNALS ARE GENERATED FROM *KRAKEN* EXCHANGE SO PLACE ORDERS ON SAME EXCHANGE FOR OPTIMAL RESULTS

#see other comments at the bottom 
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import pandas as pd
import os
import threading

#https://github.com/ccxt/ccxt/issues/4972

class Functions:

    def placeOrderCrypto(pair,cl,side):

      #https://github.com/ccxt/ccxt/issues/4972

      #other order types like with margin 
      #https://github.com/ccxt/ccxt/blob/master/examples/py/margin-leverage-order-kraken.py
      #market order examples https://github.com/ccxt/ccxt/wiki/Manual

      # pair = "BTC/EUR"
      # ordertype = "stop-loss-limit"

      # #this positions size/amount could be changed dynamically based on various technical indicator, quantitative, or machine language capability

      # amount = 0.005 
      # price = cl
      # price2 = 0.99 * cl #could dynamically set stop loss 
      # params = {"trading_agreement": "agree", "validate": True, "price2": price2}

      # krk.create_order(pair, ordertype, "sell", amount, price, params=params)

      #note could apply stop loss in kraken https://github.com/ccxt/ccxt/issues/4972


        txt = pair+','+side+','+str(cl)+'\n'

        print(txt)

        f= open("cryptoOrders.log","a")
        f.write(txt)

    def placeOrderForex(pair,cl,side):
        #data source is from Oanda but strongly reccommend to trade with them as well 
        #to learn more about forex orders goto quantlabs.net store for Oanda Fx API workshop 
        txt = pair+','+side+','+str(cl)+'\n'

        print(txt)

        f= open("ordersForex.log","a")
        f.write(txt)

    def processForexSignal(emailBody):
        sigStr = str(emailBody)
        print(sigStr)
        print(type(sigStr))
        toks = sigStr.split(',')
        print(toks)
        sym = toks[0]
        sym = sym[5:] #remove ['<p>
        side = toks[1]
        print(sym+' '+side)
        cl = float(toks[2]) #closing price in signal email
        print(cl)
        print(type(cl))
        level618 = float(toks[5])
        level786 = float(toks[6])
        level1000Str = toks[7] #results in  "1.5827</p>\\r\\n\\r\\n']"
        toks = level1000Str.split('<')
        level1000 = float(toks[0])
        print(level618)
        print(level786)
        #write signal file to Metatrader 4 data folder for EA
        #C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\3212703ED955F10C7534BE8497B221F4\MQL4\Files
        val = sym+','+str(cl)+','+str(level618)+','+str(level786)+','+str(level1000)
        f= open("C:\\Users\\USER\\AppData\\Roaming\\MetaQuotes\\Terminal\\3212703ED955F10C7534BE8497B221F4\\MQL4\\Files\\signal.txt","a")
        f.write(val) 
        f.close()
        # print('sym '+sym)
        # print('side '+side)
        # print('close '+float(cl))
        placeOrderForex(sym,cl,side)

    @staticmethod
    def processSignal(fn):
        print('process file: '+fn)
        df = pd.read_csv(fn)

        #this above read pay generaet exceptions with blank dataframe df returned. this could be a 
        #conflict between outlook addin  generated with read_csv
        # Received modified event - C:\Users\USER\Documents\outlook test\signals_006.csv.
        # Received created event - C:\Users\USER\Documents\outlook test\signals_006.csv.
        # process file: C:\Users\USER\Documents\outlook test\signals_006.csv
        # Empty DataFrame
        # Columns: [From, Subject, Date, To, Body]
        # Index: []
        # []
        # <class 'str'>
        # exception data with wrong email body format of []
        # Received modified event - C:\Users\USER\Documents\outlook test\signals_006.csv.
        # Received created event - C:\Users\USER\Documents\outlook test\signals_007.csv.
        # process file: C:\Users\USER\Documents\outlook test\signals_007.csv

        #need to ensure we are dealing with a CRYPTO signal not FOREX
        typeStr = str(df['Subject'].values)
        print(df)
        if ('FX' in typeStr) == True:
          print('process FX signal')
          processForexSignal(df['Body'].values)
          os.remove(fn)
          return  

        #otherwise assume signal is crypto

        sigStr = str(df['Body'].values)
        print(sigStr)
        print(type(sigStr))
        toks = sigStr.split(',')

        try:
          sym = toks[0]
          sym = sym[5:] #remove ['<p>
          side = toks[1]
        except:
          print('exception data with wrong email body format of '+str(df['Body'].values))
          return

        print(sym+' '+side)
        cl = float(toks[2]) #closing price in signal email
        print(cl)
        print(type(cl))
        level618 = float(toks[5])
        level786 = float(toks[6])
        level1000Str = toks[7] #results in  "1.5827</p>\\r\\n\\r\\n']"
        toks = level1000Str.split('<')
        level1000 = float(toks[0])
        print(level618)
        print(level786)
        print(level1000)

        pair = sym.replace('USD','/USD')

        placeOrderCrypto(pair,cl,side)

        os.remove(fn)

    



class Watcher:
    DIRECTORY_TO_WATCH = "C:\\Users\\USER\\Documents\\outlook test"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        fn = Functions()

        if event.is_directory:
            return None

        elif event.event_type == 'created':
            #example output: Received modified event - C:\Users\USER\Documents\outlook test\sign
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            fn.processSignal(event.src_path)

        elif event.event_type == 'modified':
            #Received modified event - C:\Users\USER\Documents\outlook test\signals_022.csv.
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)


if __name__ == '__main__':
    #processSignal('C:\\Users\\USER\\Documents\\outlook test\\signals_022.csv')
    w = Watcher()
    w.run()


#you may run into this with challenges of multithreading  of hig level of incoming emails . This can also freeze the esecution  of this cript. 

# <class 'str'>                                                                                                                          
#  2019)</span><p>ENTRY_CRYPTO_MOM_ETCUSD ETCUSD                                                                                         
# Exception in thread Thread-1:                                                                                                          
# Traceback (most recent call last):                                                                                                     
#   File "C:\Users\USER\AppData\Local\Programs\Python\Python37\lib\threading.py", line 926, in _bootstrap_inner                          
#     self.run()                                                                                                                         
#   File "C:\Users\USER\AppData\Local\Programs\Python\Python37\lib\site-packages\watchdog\observers\api.py", line 199, in run            
#     self.dispatch_events(self.event_queue, self.timeout)                                                                               
#   File "C:\Users\USER\AppData\Local\Programs\Python\Python37\lib\site-packages\watchdog\observers\api.py", line 368, in dispatch_events
                                                                                                                                       
#     handler.dispatch(event)                                                                                                            
#   File "C:\Users\USER\AppData\Local\Programs\Python\Python37\lib\site-packages\watchdog\events.py", line 322, in dispatch              
#     self.on_any_event(event)                                                                                                           
#   File "receiveSignalCrypto.py", line 120, in on_any_event                                                                             
#     processSignal(event.src_path)                                                                                                      
#   File "receiveSignalCrypto.py", line 67, in processSignal                                                                             
#     cl = float(toks[3]) #closing price in signal email                                                                                 
# ValueError: could not convert string to float: 'Entry'   