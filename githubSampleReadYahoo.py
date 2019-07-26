#https://gist.github.com/nickoala/569a9d191d088d82a5ef5c03c0690a02
import time
from itertools import chain
import email
import imaplib

#note for yahoo, enable less secure apps with https://login.yahoo.com/account/security Under Yahoo settings
#Allow apps that use less secure sign in
#Some non-Yahoo apps and devices use less secure sign-in technology, which could leave your account vulnerable. You can turn off access (which we recommend) or choose to use them despite the risks.

#Due to inbox Yahoo security, you may need to train the service to know your sending email is not spam!
#ensure to whitelist the sender email so it does not end up in the spambox http://onlinegroups.net/blog/2014/02/25/how-to-whitelist-an-email-address/

imap_ssl_host = 'imap.mail.yahoo.com' #'imap.gmail.com'  # imap.mail.yahoo.com
imap_ssl_port = 993
username = 'email@domain.com'
password = 'yourpassword'

# Restrict mail search. Be very specific.
# Machine should be very selective to receive messages.
criteria = {
    'FROM':    'support@quantlabs.net' #,
    # 'SUBJECT': 'signal',
    # 'BODY':    'signal is this',
}
# criteria = {
#     'FROM':    'PRIVILEGED EMAIL ADDRESS',
#     'SUBJECT': 'SPECIAL SUBJECT LINE',
#     'BODY':    'SECRET SIGNATURE',
#}
uid_max = 0


def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))
    # Produce search string in IMAP format:
    #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)


def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()


server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
server.login(username, password)
server.select('INBOX') 
result, data = server.uid('search', None, search_string(uid_max, criteria))

uids = [int(s) for s in data[0].split()]
if uids:
    uid_max = max(uids)
    # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

server.logout()


# Keep checking messages ...
# I don't like using IDLE because Yahoo does not support it.
while 1:
    # Have to login/logout each time because that's the only way to get fresh results.

    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(username, password)
    server.select('INBOX')

    result, data = server.uid('search', None, search_string(uid_max, criteria))

    uids = [int(s) for s in data[0].split()]
    for uid in uids:
        # Have to check again because Gmail sometimes does not obey UID criterion.
        if uid > uid_max:
            result, data = server.uid('fetch', uid, '(RFC822)')  # fetch entire message
            msg = email.message_from_string(data[0][1])
            
            uid_max = uid
        
            text = get_first_text_block(msg)
            print 'New message :::::::::::::::::::::'
            print text

    server.logout()
    print('check email....')
    time.sleep(1)
