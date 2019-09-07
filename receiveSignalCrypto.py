
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

#https://github.com/ccxt/ccxt/issues/4972

def placeOrder(pair,cl,side):
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



def processSignal(fn):
	print('process file: '+fn)
	df = pd.read_csv(fn)

	#need to ensure we are dealing with a CRYPTO signal not FOREX
	typeStr = str(df['Subject'].values)
	
	if ('CRYPTO' in typeStr) == False:
		print('not Crypto signal')
		return	

	sigStr = str(df['Body'].values)
	print(sigStr)
	print(type(sigStr))
	toks = sigStr.split(',')
	sym = toks[1]
	side = toks[2]
	print(sym+' '+side)
	cl = float(toks[3]) #closing price in signal email
	print(cl)
	print(type(cl))
	level618 = float(toks[6])
	level786 = float(toks[7])
	level1000Str = toks[8] #results in  "1.5827</p>\\r\\n\\r\\n']"
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
        if event.is_directory:
            return None

        elif event.event_type == 'created':
        	#example output: Received modified event - C:\Users\USER\Documents\outlook test\sign
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            processSignal(event.src_path)

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