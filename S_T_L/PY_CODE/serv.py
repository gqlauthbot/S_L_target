import socket
import os
from mymail import _smtp
import threading
from log import log

class ip_enum():
    IP="IP"
    L_IP="L_IP"
    P_IP="P_IP"
    MY_P_IP="YourFuckingIPAddress"
    PORT="PORT"
    MAIL="MAIL"

class serv(threading.Thread,ip_enum):
    HEADER=1024
    FORMAT='utf-8'
    
    def __init__(self,t_e,p_e,debug=False) -> None:
        #init eventers for gui and kb blocker
        self.t_e=t_e
        self.p_e=p_e
        #starting server in a thread starts with run method
        super(serv,self).__init__()
        threading.Thread.setName(self,"server")
        self.l=log(self.name,debug).get_logger()
        ip_i,flag=self.get_ip()
        self.client_dict={}
        self.addr=(ip_i[self.IP][self.L_IP],ip_i[self.PORT])
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
           
    def run(self):
        self.s_s(self.addr)
    
    def __allow_access(self,bool):
        if bool:
            self.t_e.set()
            self.p_e.set()
           
        else:
            self.p_e.clear()
            self.t_e.clear()
            
        
    def get_ip(self):
        #retutns dict of  ip info and a flag if the ip has changed or didnt existed in file
        import json
        global F_NAME
        F_NAME="IP_INFO.json"
        flag=False
        def get_L_ip() ->dict:
            from socket import gethostname,gethostbyname
            ip= gethostbyname(gethostname())
            return (ip)           
        
        def get_P_ip() ->dict:
            #retutns dict of public ip info 
            from requests import get
            try:
                return(get("https://myip.wtf/json").json())
            except:
                self.l.warning("COULDNT ACCESS THE WEBSITE, CHECK CONNECTION! from: get_P_IP")
                return False
            

        cur_ip_i={self.IP:{self.L_IP:get_L_ip(),self.P_IP:{self.MY_P_IP:get_P_ip()}},self.PORT:64435}
        #if file not exists
        if not(os.path.isfile(F_NAME)):
            self.l.warn("FILE NOT EXISTS from:P_IP")
            self.l.info("CREATING FILE")
            with open(F_NAME,'w') as f:
                json.dump(cur_ip_i,f,indent=4)
        #if there was respnse       
        elif(cur_ip_i[self.IP][self.P_IP]):
            #updating json file if needed
            with open(F_NAME,'r') as f:
                pre_ip_i=json.load(f)
                # if prev p_ip wasnt None and there is diffrence
                if (pre_ip_i[self.IP][self.L_IP]!=cur_ip_i[self.IP][self.L_IP] or
                pre_ip_i[self.IP][self.P_IP][self.MY_P_IP]!=cur_ip_i[self.IP][self.P_IP][self.MY_P_IP]):
                    f.close()
                    with open(F_NAME,'w') as nf:
                        self.l.info("IP has changed updating IP_INFO")
                        flag=True
                        json.dump(cur_ip_i,nf,indent=4)
                #check only L_IP
                elif(cur_ip_i["IP"]["L_IP"]!=pre_ip_i["IP"]["L_IP"]):
                    with open(F_NAME,'w') as nf:
                        self.l.info("IP has changed updating IP_INFO")
                        flag=True
                        json.dump(cur_ip_i,nf,indent=4)
        self.send_ip_mail()
        return (cur_ip_i,flag)
    
    def send_ip_mail(self):
        #sends the json file to smtp class to be senttt
        sender=_smtp("sender",True)
        sender.send_mime_BASE64(F_NAME)
            
    def s_s(self,addr):
        self.s.bind(addr)
        self.l.info("server is binded")
        self.s.listen()
        self.l.info("server is listining")
        while True:
            self.l.info(f"server is accepting at{addr}")
            conn,addr=self.s.accept()
            self.client_dict[addr]=[conn]
            threading.Thread(target=self.handel_conn,args=(conn,addr)).start()
            self.l.info(f"new client has connected \n amount of clients is{self.client_dict.__len__()}")
        
    def handel_conn(self,conn:socket.socket,addr):
        while True:
             self.l.info("handeling client")
             msg=conn.recv(self.HEADER).decode(self.FORMAT)
             self.l.info(f"recived : {msg} \n from address {addr}\n")
             if msg=="allow":
                 self.__allow_access(True)
             if msg=="block":
                 self.__allow_access(False)
                 
                 
             self.send_msg(msg,conn)
                
    def send_msg(self,msg,conn):
        #encode the message
        en_msg=str(msg).encode(self.FORMAT)    
        conn.send(en_msg)
