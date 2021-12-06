from mymail import _smtp,_imap
import json
import encoding

""" sender=_smtp(True)
a=int(5000)
sender.send("kololololo".encode('utf-8'),"nrforadsbl@gmail.com")"""
reader=_imap("test",True)
mail_lst=reader.get_mails(3)

for mail in mail_lst:
    try:
        print (mail['body'].decode('utf-8'))
    except:
        print("unable to decode")


