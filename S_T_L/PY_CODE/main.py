##add to gui whene pass entered close kb blocking prob PIPE

import threading
import multiprocessing
import time
from serv import serv
from tkinter import Button
import tkinter
from tkinter.constants import BOTTOM, CENTER, E, LEFT, RIGHT, S, TOP
from win32 import win32gui
from threading import Thread
from threading import Event
from log import log
from tkinter import Label,Entry,Tk,messagebox

import keyboard

 
class blocker(threading.Thread):
    def __init__(self,e:Event,debug=False, *args, **kwargs) -> None:
        super(blocker,self).__init__( *args, **kwargs)  
        Thread.setName(self,"kb_blocker")
        self.l=log(self.name,debug).get_logger()
        self.e1=e
        
        
    def run(self):
        self.block_kb()

    def block(self):
        self.e1.clear()

 
    
    def is_allowed(self)->bool:
        return self.e1.is_set()

    @staticmethod
    def on_event():
        return False
    

    def block_kb(self):
        keys=('alt','shift','ctrl','capslock',91,'tab','esc')
        while True:
            #blocks relevant keys of keyboard
            count=0
            while  not self.is_allowed():
                if count==0:
                    self.l.info("BLOCKING KEYBOARD")
                    count+=1
                keyboard.block_key(keys)
                win32gui.PumpWaitingMessages()
                if self.is_allowed():                                                                    
                    self.l.warning("DONE BLOCKING KEYBOARD")
                    
        
        

 
class Gui(multiprocessing.Process):
    def __init__(self,e:multiprocessing.Event,debug=False, *args, **kwargs) -> None: 
        super(Gui,self).__init__( *args, **kwargs)
        self.name="gui"
        self.e1=e
        self.l=log(self.name,debug).get_logger()
        
    
        
    def run(self):
        self.__start_gui()

    
    def __is_allowed(self)->bool:
        return self.e1.is_set()
    
    def __destroyer(self):
        while True:
            if self.__is_allowed():
                self.__quit()
                return
        
        
    def __nump_pad(self,root,t_var):
        #numpad creator
        np=tkinter.Label(root,bg="gray")
        np.pack(anchor=CENTER,padx=50,pady=75)
        Button(np,text="נקה",command=lambda:t_var.set("")).grid(row=3,column=4,padx=20,pady=20)
        n=1
        for i in range(0,3):
            for x in range (0,3):
               b=tkinter.Button(np,text=str(n),command=lambda n=n:(t_var.set(t_var.get()+str(n))))
               b.grid(row=i,column=x,padx=15,pady=15)
               n+=1
              
    def __start_gui(self):
        self.root=Tk()
        threading.Thread(target=self.__destroyer).start()
        self.root.attributes("-fullscreen",True)
        self.root.title("נועם הלוזר")
        #disables to alt+f4
        self.root.protocol("WM_DELETE_WINDOW", False)
        #disables maximize and minimize
        self.root.attributes('-toolwindow', True)
        l_top=Label(self.root,text="נגמר הזמןןןןןןןןן!!!!!!",fg="red",bg="black",font=('ariel',100))
        l_top.pack(side=TOP,anchor=CENTER)
        b_l=Label(self.root,padx=50,pady=20,bg="black",fg="red")
        b_l.pack(side=BOTTOM,anchor=CENTER)
        l_psw=Button(b_l,text="הכנס עכשיו ",bg="red",fg="black",command=lambda:self.__check_pass(e_psw))
        t_var=tkinter.StringVar()
        e_psw=Entry(b_l,bd=10,textvariable=t_var)
        e_psw.bind("<Button-1>",t_var.set(""))
        l_psw.pack(ipadx=10,ipady=25,anchor=CENTER,side=LEFT)
        e_psw.pack(ipadx=10,ipady=25,anchor=CENTER,side=RIGHT)
        self.__nump_pad(self.root,t_var)
        self.l.info("starting gui")
        self.root.mainloop()
        self.l.warning("gui stopped")
         


            
    def __quit(self):
        self.root.destroy()
        print("somthing")

    
               
    def __check_pass(self,entery):
        if (entery.get()=="12345"):
            self.l.info(" psw is correct")
            if( messagebox.askyesno("?מי המלך?","ניר המלך")):
                self.l.info("logged in seccesfully")
                self.e1.set()

        else:
            messagebox.showerror("סיסמא שגויה!!!","לא תמצא את הסיסמא")
            self.l.warning("wrong password has entered!")
           


    def fail_safe(self):
        #reserved for restarting the program while explicetly closed
        ...
    def ask_allow(self):
        ...

    


class Run:
    #init me once to start blocking and start server
    T=30
    def __init__(self) -> None:
         #blovking time secs
        self.l=log(__name__,True).get_logger()
        self.l.info("py side strted")
        self.t_e=threading.Event()
        self.p_e=multiprocessing.Event()
        self._serv=serv(self.t_e,self.p_e,True)
        self._serv.start()
        self.__block()
        self.__mainLoop()
        
    
    def __mainLoop(self):
        cur=False
        while True: 
            #if commanded to open and cur state is not open
            x=self.__is_allowed()
            if  x and x !=cur:
                self.l.info("allowing all")
                cur=True
                #if only one was allowed
                self.__allow()
                self.l.info("w8")
                

            
            elif x!=cur and not x:  
                cur=False
                self.l.info("blocking all")
                self.__block()
            
    def __is_allowed(self):
        return self.p_e.is_set() or self.t_e.is_set()   
    def __block(self):
        #setting events bool to False access
        self.p_e.clear()
        self.t_e.clear()
        #init blocking classes and starting them
        self._blocker=blocker(self.t_e,True)
        self._gui=Gui(self.p_e,True)
        #starts kb_blocking thread
        self._blocker.start()
        #stars gui in other process and its destroyer in other thread
        self._gui.start()
        
        

    def __allow(self):
        #the thread and proccess will close theme self via event condition
        self.p_e.set()
        self.t_e.set()

            
if __name__=="__main__":
   Run()
            
    
    
    
    

    
    
    
        