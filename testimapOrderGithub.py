#https://stackoverflow.com/questions/59513062/how-to-listen-for-incoming-emails-in-python-3
#Email sample
#Subject: CRYPTO SIGNAL 27-Aug-2020 (15:26:14.917409) BNBUSDT **ENTRY**
#Body: BNBUSDT pct 0.04622091158342035 clLast 22.2222 firstTrend 20.10063646650815 lastTrend 23.299105914444276 ENTRY

#notes that this files works in conjunction with the Quant Analytics service https://quantlabs.net/quantanalytics/
#your can learn more about building custom python trading bots for binance at https://quantlabs.net/python/

#typical output would be:
# ----- MESSAGE START -----

# From: support@quantlabs.net
# To: private328rjhd98hbv67@quantlabs.net, sales@quantlabs.net
# Date: None
# Subject: CRYPTO SIGNAL 27-Aug-2020 (15:30:02.494039) BNBUSDT **EXIT**


# 08/27/2020, 15:29:53 wavg 0.5567406767034248 BNBUSDT cl 22.2588 entry 22.2222 profit 0.036599999999999966 return 0.16442934929106673 EXIT
# ['08/27/2020,', '15:29:53', 'wavg', '0.5567406767034248', 'BNBUSDT', 'cl', '22.2588', 'entry', '22.2222', 'profit', '0.036599999999999966', 'return', '0.16442934929106673', 'EXIT']
# BNBUSDT
# 22.2588
# sell
# potential order BNBUSDT limit sell 0.1 22.2588 {'test': True}

# ----- MESSAGE END -----

import imaplib, email, getpass
from email import policy
import time
import ccxt

imap_host = 'imap.domain.net' #'imap.gmail.com'
imap_user = 'youremail@domain.com'
imap_pass = getpass.getpass()

#https://github.com/ccxt/ccxt/issues/2552

def orderBinance(symbol,side,amt,price):
    exchange = ccxt.binance({
        'apiKey': '*******',
        'secret': '*******',
        'enableRateLimit': True,
    })
 
    type = 'limit'  # or 'market'

    #side 'sell' or 'buy'
    #amount = 1.0
    #price = 0.060154  # or None

    # extra params and overrides if needed
    params = {
        'test': True,  # test if it's valid, but don't actually place it
    }

    print('potential order '+str(symbol)+' '+str(type)+' '+str(side)+' '+str(amt)+' '+str(cl)+' '+str(params))
    # order = exchange.create_order(symbol, type, side, amount, price, params)

    # print(order)



# init imap connection
# mail = imaplib.IMAP4_SSL(imap_host, 993)
# rc, resp = mail.login(imap_user, getpass.getpass())

# # select only unread messages from inbox
# mail.select('Inbox')
# status, data = mail.search(None, '(UNSEEN)')

# for each e-mail messages, print text content

while True:
    mail = imaplib.IMAP4_SSL(imap_host, 993)
    rc, resp = mail.login(imap_user, imap_pass) #getpass.getpass())

    print('**** Waiting for signals')

    # select only unread messages from inbox
    mail.select('Inbox')
    status, data = mail.search(None, '(UNSEEN)')

    for num in data[0].split():
        # get a single message and parse it by policy.SMTP (RFC compliant)
        status, data = mail.fetch(num, '(RFC822)')
        email_msg = data[0][1]
        email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)

        print("\n----- MESSAGE START -----\n")

        print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n" % ( \
            str(email_msg['From']), \
            str(email_msg['To']), \
            str(email_msg['Date']), \
            str(email_msg['Subject'] )))

        if email_msg['Subject'].find('CRYPTO SIGNAL') == -1:
            print('**** NOT CRYPTO SIGNAL')
            continue


        # print only message parts that contain text data
        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                for line in part.get_content().splitlines():
                    print(line)
                    toks = line.split(' ')
                    print(toks)
                    sym = toks[4]
                    cl = float(toks[6])
                    sid = toks[13]
                    
                    if sid == 'EXIT':
                        side = 'sell'
                    elif sid == 'ENTRY':
                        side = 'buy'

                    print(sym)
                    print(cl)
                    print(side)
                    orderBinance(sym,side,0.1,cl)

        print("\n----- MESSAGE END -----\n")

    time.sleep(5)