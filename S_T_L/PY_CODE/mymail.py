
from email import *
from email.mime import * 
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
from io import FileIO
from log import log
import enum

    
class _smtp():
    global MAIL
    MAIL="nrforadsbl@gmail.com"
    global PASS
    PASS="Qeadzcwxs132"
    global TO
    TO="nrforadsbl@gmail.com"
    class err(enum.Enum):
        smtp_srv='somthing went wrong with ehlo msg'
        send="unabale to send message"
        connected="connected to smtp serv seccesfully!"
        auth="login smtp seccesfully"
    import smtplib
    def __init__(self,name,debug=False) -> None:
        self.l=log(name,debug).get_logger()

    def connect_smtp(self,_try=0)->smtplib.SMTP_SSL:
        import smtplib
        #opening smtp conn with google smtp serv on port 587 and waiting for AKW
        if (_try<30):
            try:
                conn=smtplib.SMTP_SSL("smtp.gmail.com",465)
                conn.ehlo()
                self.l.info(self.err.connected.value)
                _try+=1
            except :
                self.l.error("somthing went wrong with ehlo msg")
                self.l.info("trying again")
                self.__init__(_try+1)
            try:
                conn.login(MAIL,PASS)
                self.l.info(self.err.auth.value)
                return conn
            except smtplib.SMTPAuthenticationError as err:
                self.l.error(err)
                raise err
        else:
            raise self.err.smtp_srv
        
    def send_text(self,msg):
        conn=self.connect_smtp()
        try:
            conn.sendmail(from_addr=MAIL,to_addrs=TO,msg=msg)
            conn.quit()
            self.l.info("SECCESSFULLY SENT MAIL")
        except:
            self.l.error(self.err.send.value)

    def send_mime(self,f_name:str):
        import codecs
        #file must be opened  and given as 'rb' to method
        from email import encoders as en
        msg=MIMEMultipart()
        msg['To']=TO
        msg['From']=MAIL
        msg['Subject']="ip json"
        msg.set_charset('utf-8')
        msg.attach(MIMEText("json here",'plain'))
        mb=MIMEText('application','octet-stream')
        #add js as apyload
        try:
            mb.set_payload(codecs.open(f_name,'r','utf-8').read())
        except:
            self.l.warning("file error when trying to send mail")
        #encode the payload in mime base 
        mb.add_header('Content-Decomposition','attachment', filename=f_name)
        msg.attach(mb)
        
        self.send_text(msg.as_string())

    def  send_mime_BASE64(self,f_name:str):
        #file must be opened  and given as 'rb' to method
        from email import encoders as en
        msg=MIMEMultipart()
        msg['To']=TO
        msg['From']=MAIL
        msg['Subject']=f_name
        msg.set_charset('utf-8')
        msg.attach(MIMEText(f_name,'plain'))
        mb=MIMEText('application','octet-stream')
        #add js as apyload
        try:
            with open(f_name,'rb') as f:    
                mb.set_payload(f.read())
                en.encode_base64(mb)
        except:
            self.l.warning("file error when trying to send mail")
        #encode the payload in mime base 
        mb.add_header('Content-Decomposition','attachment', filename=f_name)
        msg.attach(mb)
        print(msg.as_string())
        self.send_text(msg.as_string())    

        

class _imap():
    class err(enum.Enum):
        imap_srv="somthing went wrong with imap connection establishing"
        wrong_pass="authantication error"
        connected="connected to imap serv seccesfully!"
        auth="login imap seccesfully"

    def __init__(self,name,debug=False) -> None:
        self.l=log(name,debug).get_logger()
    def conn_imap(self,_try=0)->imaplib.IMAP4_SSL:
        import imaplib
        if (_try<5):
            try:
                conn=imaplib.IMAP4_SSL("imap.gmail.com",993)
                self.l.info(self.err.connected.value)
                try:
                    conn.login(MAIL,PASS)
                    self.l.info(self.err.auth.value)
                    return conn
                except:
                    self.l.error(self.err.wrong_pass.value)
                _try+=1
            except :
                self.l.error(self.err.imap_srv.value)
                self.l.info("trying again")
                self.conn_imap(_try+1)
        else:
            raise self.err.imap_srv.value

    def get_mails(self,n_to_read):
        import email
        from email.header import decode_header
        mails_list=[]
        conn=self.conn_imap()
        status,email_num=conn.select('INBOX')
        email_num=int(email_num[0])
        for email_ID in range (email_num,email_num-n_to_read,-1):
            status,responses=conn.fetch(str(email_ID), "(RFC822)")
            for response in responses:
                if isinstance(response,tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    if(msg['Subject'] is  None):
                        msg['Subject']="no subject"
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if (isinstance(subject, bytes)and encoding is not None):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if (isinstance(From, bytes) and encoding is not None):
                        From = From.decode(encoding)

                    body=msg.get_payload(decode=True)
        
                    mails_list.append({"Subject":subject,"from":From,"body":body}) 
        return mails_list       
                    