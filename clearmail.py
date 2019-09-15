#https://stackoverflow.com/questions/3180891/imap-deleting-messages
import imaplib
box = imaplib.IMAP4_SSL('mail.quantlabs.net', 993)
box.login("email","password")
box.select('Inbox')
typ, data = box.search(None, 'ALL')
for num in data[0].split():
   box.store(num, '+FLAGS', '\\Deleted')
box.expunge()
box.close()
box.logout()