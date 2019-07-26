#https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
# Python code to illustrate Sending mail with attachments 
# from your Gmail account  
  
# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   
fromaddr = "from@domain.com"
toaddr = "to@yahoo.com"
   
# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
# storing the senders email address   
msg['From'] = 'Santa Claus'
  
# storing the receivers email address  
msg['To'] = 'Password'
  
# storing the subject  
msg['Subject'] = "Alert ENTRY Alert BNBETH"
  
# string to store the body of the mail 
body = "qty,0,Htp,0.8957200000000001,Hsl,0.8788422999999999,Stp,0.8867970999999999,Ssl,0.8969299999999999"
  
# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 
  
# open the file to be sent  
filename = "readme.txt"
attachment = open("/Users/quantlabsnet/DOCS/Documents/python/email/readme.txt", "rb") 
  
# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
p.set_payload((attachment).read()) 
  
# encode into base64 
encoders.encode_base64(p) 
   
p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
msg.attach(p) 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login(fromaddr, "Password") 
  
# Converts the Multipart msg into a string 
text = msg.as_string() 
  
# sending the mail 
s.sendmail(fromaddr, toaddr, text) 
  
# terminating the session 
s.quit() 
