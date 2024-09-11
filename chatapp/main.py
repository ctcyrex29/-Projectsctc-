import socket
import time
import threading
from tkinter import *

root=Tk()
root.geometry("300x500")
root.config(bg="black")

def func():
    t=threading.Thread(target=recv)
    t.start()

def recv():
    listensocket=socket.socket()
    port=3050
    maxconnection=99
    ip=socket.gethostname()
    print(ip)

    listensocket.bind(('', port))
    listensocket.listen(maxconnection)
    (clientsocket, address)=listensocket.accept()
    
    while True:
        sendmessage=clientsocket.recv(1024).decode()
        if not sendmessage=="":
            time.sleep(5)
            lstbox.insert(0,"Client: "+sendmessage)

xr=0
def sendmsg():
    global s
    if xr==0:
        xr=socket.socket()
        hostname='desktop-uj3qcrs'
        port=4050
        xr.connect((hostname, port))
        msg=messagebox.get()
        lstbox.insert(0,"You : "+msg)
        xr.send(msg.encode())
        xr=xr+1
    
    else:
        msg=messagebox.get()
        lstbox.insert(0,"You : "+msg)
        s.send(msg.encode())

def threadsendmsg():
    th=threading.Thread(target=sendmsg)
    th.start()

button=Button(root, command=func,borderwidth=2)
button.place(x=90,y=10)

message=StringVar()
messagebox=Entry(root,textvariable=message,font=('calibre',14,'normal'), border=2,width=32)
messagebox.place(x=10,y=444)

sendmessagebutton=Button(root, command=threadsendmsg,borderwidth=0)
sendmessagebutton.place(x=200,y=440)

lstbox=Listbox(root,height=20,width=45)
lstbox.place(x=15,y=80)





    
