from tkinter import *
from tkinter import messagebox as mb
import wcwidth as ww
from socket import *
import threading as td
import os
def mainclose():
    if gotten:
        sock.sendall(b'system')
        sock.recv(1024)
        sock.sendall(b'quit')
        sock.recv(1024)
    win.destroy()
def background():
    csock.sendall(username.encode())
    csock.recv(1024)
    csock.sendall(b'ok')
    while True:
        cmd=csock.recv(1024).decode()
        csock.sendall(b'ok')
        if cmd=='add':
            friend=csock.recv(1024).decode()
            csock.sendall(b'ok')
            f=open(mr+username+'/'+friend+'.txt','w')
            f.close()
            states[friend]=lb.size()
            lb.insert(END,friend)
        elif cmd=='msg':
            usnm=csock.recv(1024).decode()
            csock.sendall(b'ok')
            msg=csock.recv(1024).decode()
            csock.sendall(b'ok')
            print(usnm+' '+msg)
            NewMsg(1,msg,usnm)
def ADDR():
    import requests
    from bs4 import BeautifulSoup
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    rp=requests.get('https://blog.csdn.net/Oscar_Myh_39/article/details/135032913?spm=1001.2014.3001.5501',headers=header)
    rp=BeautifulSoup(rp.text,'html.parser')
    div=rp.find('div',{'id':'content_views','class':'htmledit_views'})
    p=div.find('p')
    dic=p.text.split(':')
    print(dic)
    return dic
def closed():
    pass
def cut(strs:str,width:int)->list:
    sum=0
    k=0
    strlist=[]
    for i in range(len(strs)):
        s=ww.wcwidth(strs[i])
        if s!=-1:
            sum+=s
        if sum>width:
            strlist.append(strs[k:i])
            k=i
            sum=s
    if sum>0:
        strlist.append(strs[k:len(strs)])
    return strlist
def length(strs:str)->int:
    sum=0
    for ch in strs:
        s=ww.wcwidth(ch)
        if s!=-1:
            sum+=s
    return sum
def GetUser()->None:
    global vis
    global cansend
    k=lb.curselection()
    if len(k)>0:
        cansend=True
        msg.config(background='pink')
        user.set(lb.get(int(k[0])))
        if user.get()!=vis:
            vis=user.get()
            f=open((mr+username+'/'+vis+'.txt'),'r')
            Msgs=f.readlines()
            msg.config(state='normal')
            msg.delete(0.0,END)
            msg.config(state='disabled')
            i=0
            while i<len(Msgs):
                if Msgs[i][:len(Msgs[i])-2]==username:
                    NewMsg(2,Msgs[i+1])
                    i+=2
                elif Msgs[i]=='\n':
                    i+=1
                    pass
                else:
                    NewMsg(1,Msgs[i+1])
                    i+=2
            f.close()
            lb.itemconfig(states[vis],background='white')
    win.after(50,GetUser)
def error()->None:
    mb.showwarning('Syntax Error!','语法错误!使用help命令获取帮助。')
def isdigit(num:str)->bool:
    try:
        int(num)
        return True
    except:
        return False
def NewMsg(mode:int,Msg:str=None,usnm:str=None)->None:
    if not cansend and Msg==None:
            e.delete(0,END)
            e.icursor(0)
            return
    if user.get()=='system' and Msg==None:
        message=e.get()
        NewMsg(2,message)
        cmd=message.split(' ')
        if cmd[0]=='list':
            if len(cmd)>2:
                error()
            else:
                if cmd[1]=='rqmt':
                    sock.sendall(b'system')
                    sock.recv(1024)
                    sock.sendall(b'rqmt')
                    size=int(sock.recv(1024).decode())
                    sock.sendall(b'ok')
                    if size==0:
                        NewMsg(1,'None')
                    else:
                        global rqnm
                        rqnm=[]
                        for i in range(size):
                            rqmt=sock.recv(1024).decode()
                            rqnm.append(rqmt)
                            NewMsg(1,rqmt)
                            sock.sendall(b'ok')
                        sock.recv(1024)
                        NewMsg(1,'Enter in the number of requirement which you want to accept:')
                        NewMsg(1,'For example,you can enter in \"1\" to accept the first requirement or \"2\" to accpet the second requirement.')
                        NewMsg(1,'If you don\'t want to accept the anyone or you want to quit,you can enter in \"-1\".')
                        NewMsg(1,'Please enter in your decision:')
                        global number
                        number=size
                else:
                    error()
        elif len(cmd)==1 and isdigit(cmd[0]):
            ipt=int(cmd[0])
            if number!=None:
                if 0<ipt and ipt<=number:
                    sock.sendall(b'system')
                    sock.recv(1024)
                    sock.sendall(b'accept')
                    sock.recv(1024)
                    if ipt==-1:
                        sock.sendall(b'None')
                    else:
                        sock.sendall(rqnm[ipt-1].encode())
                    sock.recv(1024)
                    NewMsg(1,'Finish it successfully.')
                    number=None
                    rqnm=None
                elif ipt==-1:
                    number=None
                    rqnm=None
    else:
        msg.config(state='normal')
        if Msg==None:
            message=e.get()
        else:
            message=Msg
        e.delete(0,END)
        e.icursor(0)
        if message=="":
            return
        if message[len(message)-1]=='\n':
            message=message[:len(message)-1]
        if mode==1:
            if usnm!=None:
                f=open((mr+username+'/'+usnm+'.txt'),'a')
                f.write((usnm+':\n'))
                f.write((message+'\n'))
                f.close()
                f=open((mr+username+'/'+usnm+'_lst.txt'),'w')
                f.write((usnm+':\n'))
                f.write((message+'\n'))
                f.close()
                print(usnm+' '+user.get())
                if usnm!=user.get():
                    lb.itemconfig(states[usnm],background='pink')
                else:
                    msg.insert(END,user.get()+':\n')
                    msg.insert(END,'\n'.join(cut(message,20))+'\n','white')
            else:
                msg.insert(END,user.get()+':\n')
                msg.insert(END,'\n'.join(cut(message,20))+'\n','white')
        elif mode==2:
            msg.insert(END,'                                             Me:\n')
            if length(message)>20:
                k=cut(message,20)
                for i in range(len(k)):
                    k[i]='                            '+k[i]
                msg.insert(END,'\n'.join(k)+'\n','green')
            else:
                k=""
                for i in range(48-length(message)):
                    k+=' '
                msg.insert(END,k+message+'\n','green')
            if Msg==None:
                sock.sendall(user.get().encode())
                sock.recv(1024)
                sock.sendall(message.encode())
                sock.recv(1024)
                f=open((mr+username+'/'+user.get()+'.txt'),'a')
                f.write((username+':\n'))
                f.write((message+'\n'))
                f.close()
                f=open((mr+username+'/'+user.get()+'_lst.txt'),'w')
                f.write((username+':\n'))
                f.write((message+'\n'))
                f.close()
    msg.see(END)
    msg.config(state='disabled')
def recvfile(sock:socket,route:str)->None:
    size=int(sock.recv(1024).decode())
    sock.sendall(b'ok')
    f=open(route,'w')
    for i in range(int(size/1024)):
        f.write(sock.recv(1024).decode())
    f.write(sock.recv(size%1024).decode())
    f.close()
    sock.sendall(b'ok')
def User()->None:
    if not os.path.exists(mr):
        os.makedirs(mr)
    ret=sock.recv(1024).decode()
    sock.sendall(b'ok')
    while ret!='@end':
        print(ret+':')
        sock.recv(1024)
        if ret=='system':
            sock.sendall(b'neither')
        else:
            route=mr+username+'/'+ret
            if not os.path.exists(route+'_lst.txt') or not os.path.exists(route+'.txt'):
                sock.sendall(b'both')
                recvfile(sock,route+'_lst.txt')
                recvfile(sock,route+'.txt')
            else:
                sock.sendall(b'check')
                svlst=sock.recv(65536).decode()
                f=open(route+'_lst.txt','r')
                cllst=f.read()
                f.close()
                if svlst!=cllst:
                    sock.sendall(b'both')
                    recvfile(sock,route+'_lst.txt')
                    recvfile(sock,route+'.txt')
                else:
                    sock.sendall(b'neither')
        states[ret]=lb.size()
        lb.insert(END,ret)
        ret=sock.recv(1024).decode()
        sock.sendall(b'ok')
    sock.recv(1024)
def check(root:Toplevel,un:StringVar,pw:StringVar)->None:
    sock.sendall(un.get().encode())
    ret=sock.recv(1024).decode()
    if ret=='notfound':
        print('here')
        page=Toplevel(win)
        page.attributes('-topmost',True)
        page.title('Registration')
        page.geometry('400x200')
        page.protocol('WM_DELETE_WINDOW',closed)
        l1=Label(page,text='您似乎没有注册',fg='green',font=('楷体'))
        l1.pack()
        l2=Label(page,text='请输入需注册的用户名:',fg='green',font=('楷体'))
        l2.pack()
        usname=StringVar()
        psword=StringVar()
        e1=Entry(page,textvariable=usname,font=('楷体'))
        e1.pack(fill='x')
        l3=Label(page,text='请输入需注册的密码:',fg='green',font=('楷体'))
        l3.pack()
        e2=Entry(page,textvariable=psword,font=('楷体'),show='*')
        e2.pack(fill='x')
        def register(pages:Toplevel,usnm:StringVar,pswd:StringVar)->None:
            sock.sendall(usnm.get().encode())
            sock.recv(1024)
            sock.sendall(pswd.get().encode())
            sock.recv(1024)
            sock.sendall(b'ok')
            ret=sock.recv(1024).decode()
            print(ret)
            if ret=='used':
                mb.showwarning('注册失败','用户已被注册!')
                pages.attributes('-topmost',True)
            else:
                global username 
                username=usnm.get()
                os.makedirs(mr+username+'/')
                f=open(mr+username+'/system.txt','w')
                f.close()
                pages.destroy()
                root.destroy()
                dic=ADDR()
                csock.connect((dic[1][2:],int(dic[2])))
                GetUser()
                User()
                t=td.Thread(target=background,daemon=True)
                t.start()
        reg=Button(page,command=lambda:register(page,usname,psword),text='注册',font=('楷体'),fg='green')
        reg.pack()
        page.bind('<Return>',lambda func:reg.invoke())
        page.mainloop()
    elif ret==pw.get():
        sock.sendall(b'true')
        sock.recv(1024)
        global username
        username=un.get()
        root.destroy()
        dic=ADDR()
        csock.connect((dic[1][2:],int(dic[2])))
        GetUser()
        User()
        t=td.Thread(target=background,daemon=True)
        t.start()
    else:
        sock.sendall(b'false')
        sock.recv(1024)
        mb.showwarning('登录失败','用户名或密码错误!')
        root.attributes('-topmost',True)
        pw.set('')
def login()->None:
    page=Toplevel(win)
    page.protocol('WM_DELETE_WINDOW',closed)
    page.geometry('300x150')
    page.attributes('-topmost',True)
    page.iconbitmap('D:/Test/Communication.ico')
    page.title('Login')
    un=StringVar()
    pw=StringVar()
    l1=Label(page,text='用户名:',font=('楷体'),foreground='green')
    l1.pack()
    u=Entry(page,textvariable=un,font=('楷体'))
    u.pack(fill='x')
    l2=Label(page,text='密码:',font=('楷体'),foreground='green')
    l2.pack()
    p=Entry(page,textvariable=pw,show='*',font=('楷体'))
    p.pack(fill='x')
    log=Button(page,command=lambda:check(page,un,pw),text='登录',font=('楷体'))
    log.pack()
    page.bind('<Return>',lambda func:log.invoke())
    page.mainloop()
def GetAddr()->None:
    dic=ADDR()
    page=Toplevel(win)
    page.protocol('WM_DELETE_WINDOW',closed)
    page.geometry('300x200')
    page.title('GetAddr')
    page.iconbitmap('D:/Test/Console.ico')
    page.attributes('-topmost',True)
    l=Label(page,text='请输入服务器IPv4地址:',font=('楷体'),fg='green')
    l.pack()
    addr=StringVar()
    ee=Entry(page,textvariable=addr,font=('楷体'))
    addr.set(dic[1][2:])
    ee.pack()
    ees=Scrollbar(page,orient='horizontal')
    ee.config(xscrollcommand=ees.set)
    ees.config(command=ee.xview)
    ees.pack(fill='x')
    l1=Label(page,text='服务器IPv4地址端口:',font=('楷体'),fg='green')
    l1.pack()
    post=StringVar()
    ep=Entry(page,textvariable=post,font=('楷体'))
    post.set(dic[2])
    ep.pack()
    def quit()->None:
        try:
            page.attributes('-topmost',True)
            sock.connect((addr.get(),int(post.get())))
            sock.settimeout(None)
            sock.sendall(b'None')
            sock.recv(1024)
            t=td.Thread(target=login,daemon=False)
            t.start()
            page.destroy()
            global gotten
            gotten=True
        except:
            mb.showwarning('Error','Can\'t connect to the server!(IPv4 Error)')
            page.attributes('-topmost',True)
    bt=Button(page,text='确定',command=quit,font=('楷体'),fg='green')
    bt.pack()
    page.bind('<Return>',lambda func:bt.invoke())
    page.mainloop()
def AddUser()->None:
    if username==None:
        return
    global cansend
    cansend=False
    page=Toplevel(win)
    page.title('Add Friend')
    page.geometry('400x280')
    page.attributes('-topmost',True)
    def auclose():
        global cansend
        cansend=True
        page.destroy()
    page.protocol('WM_DELETE_WINDOW',auclose)
    f1=Frame(page)
    f1.grid(row=0,column=0,columnspan=3)
    uls=Scrollbar(f1)
    uls.pack(fill='y',side='right')
    ul=Listbox(f1,yscrollcommand=uls.set,height=10,width=35,font=('楷体'))
    ul.pack()
    uls.config(command=ul.yview)
    sock.sendall(b'system')
    sock.recv(1024)
    sock.sendall(b'user')
    ret=sock.recv(1024).decode()
    sock.sendall(b'ok')
    dic=[]
    sdic={}
    while ret!='@end':
        if ret.lower()!=username.lower():
            dic.append(ret)
        ret=sock.recv(1024).decode()
        sock.sendall(b'ok')
    sock.recv(1024)
    dic.sort(key=lambda x:x.encode('gbk'))
    for d in dic:
        ul.insert(END,d)
    ld=''
    def dfs(ndic:dict,i:int,s:str,ins:dict)->dict:
        if i==len(s)-1:
            ndic[s[i]]=ins
            return ndic
        ndic[s[i]]=dfs(ndic[s[i]],i+1,s,ins)
        return ndic
    for i in range(len(dic)):
        d=dic[i]
        ndic={'value':i}
        f=True
        for j in range(len(d)-2,-1,-1):
            if j<len(ld):
                if d[j]==ld[j]:
                    ff=True
                    for k in range(j,-1,-1):
                        if d[k]!=ld[k]:
                            ff=False
                    if ff:
                        sdic=dfs(sdic,0,d[:j+2],ndic)
                        f=False
                        break
            ndic={'value':i,d[j+1]:ndic}
        if f:
            sdic[d[0]]=ndic
        ld=d
    def updating():
        global update
        global isuser
        if update:
            try:
                ndic=sdic
                s=ues.get()
                for i in range(len(s)):
                    ndic=ndic[s[i]]
                    if i==len(s)-1:
                        ul.selection_clear(0,END)
                        ul.see(ndic['value'])
                        ul.select_set(ndic['value'])
                        isuser=True
            except:
                ul.select_clear(0,END)
                isuser=False
        page.after(50,updating)
    ues=StringVar()
    ue=Entry(page,textvariable=ues,width=30,font=('楷体'))
    ue.grid(row=1,column=0)
    def bqkcmd():
        global update
        if not update:
            ue.config(state='normal')
            ue.delete(0,END)
            update=True
    bqk=Button(page,command=bqkcmd,text='×',fg='green',font=('楷体',12))
    bqk.grid(row=1,column=1)
    def bsscmd():
        global update
        if update:
            ue.config(state='readonly')
            update=False
            if not isuser:
                mb.showwarning('Error','没有这个用户!(UserNotFount Error)')
    bss=Button(page,command=bsscmd,text='搜索',fg='green',font=('楷体',12))
    bss.grid(row=1,column=2)
    def bfscmd():
        k=ul.curselection()
        if len(k)>0:
            k=ul.get(int(k[0]))
            sock.sendall(b'system')
            sock.recv(1024)
            sock.sendall(b'add')
            sock.recv(1024)
            sock.sendall(k.encode())
            ret=sock.recv(1024).decode()
            if ret=='yes':
                mb.showinfo('Successful','Send the requirement successfully.')
            else:
                mb.showwarning('Failed',"You've sent the requirement already!(SendRqmtTwice Error)")
        else:
            mb.showwarning('Error','未选择用户!(NoUserSelected Error)')
        page.attributes('-topmost',True)
    bfs=Button(page,command=bfscmd,text='发送请求',fg='green',font=('楷体',12))
    bfs.grid(row=2,column=0,columnspan=3)
    page.after(50,updating)
    page.mainloop()
mr='D:/TkTest/TkTest-User/'
if not os.path.exists(mr):
    os.makedirs(mr)
win=Tk()
win.attributes('-topmost',True)
win.protocol('WM_DELETE_WINDOW',mainclose)
csock=socket(AF_INET,SOCK_STREAM)
sock=socket(AF_INET,SOCK_STREAM)
sock.settimeout(1000)
win.geometry('600x300')
win.iconbitmap('D:/Test/qq.ico')
win.title('Hello Communication | Made by LDH & Jerry-Hello')
user=StringVar()
us=Label(win,textvariable=user,font=('楷体',15),fg='green')
adus=Button(win,text='✚',fg='green',width=3,height=1,font=('楷体',12),command=AddUser)
s=Scrollbar(win)
msgs=Scrollbar(win)
es=Scrollbar(win,orient='horizontal')
lb=Listbox(win,yscrollcommand=s.set,height=11,selectborderwidth=3,selectmode='single',selectbackground='green',font=('楷体',12))
msg=Text(win,yscrollcommand=msgs.set,height=13,width=48,state='disabled',font=('楷体',12))
msg.tag_config('white',foreground='white')
msg.tag_config('green',foreground='green')
e=Entry(win,exportselection=True,width=48,xscrollcommand=es.set)
bt1=Button(win,width=4,height=1,text='发送',font=('楷体'),bg='green',fg='blue',command=lambda:NewMsg(2))
win.bind('<Return>',lambda func:bt1.invoke())
s.config(command=lb.yview)
msgs.config(command=msg.yview)
es.config(command=e.xview)
lb.pack(side='left',fill='x')
s.pack(side='left',fill='y')
msg.place(x=185,y=40)
msgs.pack(side='right',fill='y')
e.place(x=185,y=260)
es.pack(side='bottom',fill='x')
bt1.place(x=530,y=255.5)
us.place(x=185,y=12)
adus.place(x=540,y=12)
vis='-1'
username=None
cansend=False
number=None
rqnm=None
gotten=False
update=True
isuser=False
states={}
GetAddr()
win.mainloop()