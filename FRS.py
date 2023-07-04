from cgitb import text
from glob import glob
import imp
from msilib.schema import AppId
from pickle import TRUE
from tokenize import Name
from webbrowser import get
import pymssql
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, messagebox as msgbox

from sqlalchemy import null

### 목적지 Combobox ###
desValue = ["목적지",] 
conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
cursor = conn.cursor()
cursor.execute('SELECT DISTINCT destination FROM Airplane;')
for row in cursor:
    desValue+=row  
DEST_Value=[str(i) for i in desValue]
conn.close()

### 비행기 날짜 Combobox ###
dateValue = ["날짜", ]
conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
cursor = conn.cursor()
cursor.execute('SELECT DISTINCT date FROM Airplane;')
for row in cursor:
    dateValue+=row
DATE_Value=[str(i) for i in dateValue]
conn.close()

### 로그인 버튼 ###
def LoginBTClick():
    ### 항공 조회 버튼 ###
    def AirSearchBT():
        MainText=tk.Text(Mainwin, width=51, height=28)
        MainText.place(x=70, y=200)
        MainText.insert(END, "항공편명")
        MainText.insert(END, "###")
        MainText.insert(END, "목적지")
        MainText.insert(END, "###")
        MainText.insert(END, "출발날짜")
        MainText.insert(END, "\n")
        conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Airplane WHERE destination = %s OR date = %s;', (Descombobox.get(), Datecombobox.get()))
        for row in cursor:
            MainText.insert(END, row[0])
            MainText.insert(END, "   ")
            MainText.insert(END, row[1])
            MainText.insert(END, "   ")
            MainText.insert(END, row[2])
            MainText.insert(END, "\n")
            print(row[0], row[1], row[2])
        conn.close()
    
    ### 항공 예약 버튼 ###
    def AirResBT():
        LoginId = IdTBox.get()
        conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
        cursor = conn.cursor()
        cursor.execute('SELECT airplane_number FROM Airplane WHERE destination = %s AND date = %s;', (Descombobox.get(), Datecombobox.get()))
        Ap_Num = cursor.fetchone()
        #print(Ap_Num)
        cursor.execute('SELECT reservation_number FROM Reservation WHERE passenger_passid IS NULL AND airplane_number = %s;', (Ap_Num[0]))
        Resv_Num = cursor.fetchone()
        #print(Resv_Num)
        cursor.execute('UPDATE Reservation SET passenger_passid = %s WHERE reservation_number = %s ;', (LoginId ,Resv_Num[0]))
        conn.commit()
        conn.close()
        msgbox.showinfo("예약 완료", "예약이 완료 되었습니다. 예약 조회로 한번더 확인해주세요")


        
    ### 예약 조회 버튼 ###
    def MyResBT():
        ### 예약 취소 버튼 ###
        def AirResCanBT():
            LoginId = IdTBox.get()
            Ap_num = ApnBox.get()
            conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
            cursor = conn.cursor()
            cursor.execute('SELECT reservation_number FROM Reservation WHERE passenger_passid = %s AND airplane_number = %s;', (LoginId, Ap_num))
            Resv_num = cursor.fetchone()
            cursor.execute('DELETE FROM Reservation WHERE reservation_number = %s' , (Resv_num))
            #print(Resv_num, Ap_num)
            cursor.execute('INSERT INTO Reservation (reservation_number, airplane_number, passenger_passid) values (%s, %s, NULL);', (Resv_num[0], Ap_num))
            conn.commit()
            conn.close()
            MyResWin.destroy()
            msgbox.showinfo("예약 취소 완료", "예약이 취소 되었습니다. 예약 조회로 한번더 확인해주세요")
            #print(Resv_num, Ap_num)

        LoginId=IdTBox.get()
        MyResWin=tk.Toplevel(Mainwin)
        MyResWin.title("예약 조회")
        MyResWin.geometry("450x450+725+250")
        MyResWin.resizable(False, False)
        
        MyResText=tk.Text(MyResWin, width=50, height=25)
        MyResText.place(x=55, y=30)
        MyResText.insert(END, "====================예약 조회=====================")
        MyResText.insert(END, "\n")
        MyResText.insert(END, "항공편명")
        MyResText.insert(END, "##")
        MyResText.insert(END, "목적지")
        MyResText.insert(END, "##")
        MyResText.insert(END, "출발날짜")
        MyResText.insert(END, "##")
        MyResText.insert(END, "좌석수")
        MyResText.insert(END, "##")
        MyResText.insert(END, "항공사")
        MyResText.insert(END, "\n")
        
        CanReBT=tk.Button(MyResWin, relief="solid", text="예약 취소", width=10, bg="white", command=AirResCanBT) #취소 버튼
        CanReBT.place(x=270, y=400)
        
        ApnBox=tk.Entry(MyResWin, width=20, bg="white")
        ApnBox.insert(0, "airplane_number")
        ApnBox.place(x=100, y=403)
        
        conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
        cursor = conn.cursor()
        cursor.execute('SELECT airplane_number FROM Reservation WHERE passenger_passid = %s;', (LoginId))
        Airplane = cursor.fetchone()
        #print(Airplane)

        cursor.execute('SELECT * FROM Airplane as Ap RIGHT OUTER JOIN Reservation as Rv ON Ap.airplane_number = Rv. airplane_number WHERE Rv.airplane_number = %s AND Rv.passenger_passid = %s;', (Airplane[0], LoginId))
        for row in cursor:
            MyResText.insert(END, row[0])
            MyResText.insert(END, "   ")
            MyResText.insert(END, row[1])
            MyResText.insert(END, "   ")
            MyResText.insert(END, row[2])
            MyResText.insert(END, "   ")
            MyResText.insert(END, row[3])
            MyResText.insert(END, "   ")
            MyResText.insert(END, row[4])
            MyResText.insert(END, "\n")
            #print(row[0], row[1], row[2], row[3], row[4])
        conn.close()
        
        
        
    ### 정보 변경 버튼 ###
    def InfoChBT():
        def ChangInfoM():
            LoginId= IdTBox.get()
            #print(LoginId)
            conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
            cursor = conn.cursor()
            cursor.execute('UPDATE Passenger SET passenger_email = %s, passenger_dateofbrith = %s, passenger_phonenumber = %s, passenger_uniqueness = %s WHERE passenger_passid = %s;', (ChEmailEt.get(), ChBirthEt.get(), ChPhoneNumEt.get(), ChUniqeEt.get(), LoginId))
            conn.commit()
            
            msgbox.showinfo("정보 변경", "정보가 수정되었습니다.")
            ChWin.destroy()
            conn.close()
        
        ChWin=tk.Toplevel(Mainwin)
        ChWin.title("정보 변경")
        ChWin.geometry("450x350+725+250")
        ChWin.resizable(False, False)
        
        ChEmail=tk.Label(ChWin, text="이메일",width=15, height=2)
        ChEmail.place(x=49, y=15)
    
        ChEmailEt=tk.Entry(ChWin, width=40)
        ChEmailEt.insert(0, "Email")
        ChEmailEt.place(x=85, y=50)
    
        ChBirth=tk.Label(ChWin, text="생년월일(ex)2022-12-31)",width=25, height=2)
        ChBirth.place(x=64, y=75)
    
        ChBirthEt=tk.Entry(ChWin, width=40)
        ChBirthEt.insert(0, "date of birth")
        ChBirthEt.place(x=85, y=110)
    
        ChPhoneNum=tk.Label(ChWin, text="핸드폰번호",width=15, height=2)
        ChPhoneNum.place(x=62, y=140)
    
        ChPhoneNumEt=tk.Entry(ChWin, width=40)
        ChPhoneNumEt.insert(0, "PhoneNumber")
        ChPhoneNumEt.place(x=85, y=175)
    
        ChUniqe=tk.Label(ChWin, text="특이사항",width=15, height=2)
        ChUniqe.place(x=56, y=210)
        
        ChUniqeEt=tk.Entry(ChWin, width=40)
        ChUniqeEt.insert(0, "특이사항")
        ChUniqeEt.place(x=85, y=245)
    
        ChBT=tk.Button(ChWin, relief="solid", text="정보 변경 완료", width=30, bg="gray", command=ChangInfoM)
        ChBT.place(x=120, y=300)
    
    ### 로그인 ###
    id = "NULL"
    real = ""
    tempid=IdTBox.get()

    conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
    cursor = conn.cursor()
    cursor.execute('SELECT passenger_passid FROM Passenger;')
    Realid = cursor.fetchone()

    while Realid:
        real = Realid[0]
        if tempid == real:
            id = real
            real = ""
            break
        else:
            id = "NULL"
            real = ""
            Realid = cursor.fetchone()
    conn.close()

    ### 로그인 된 경우 ###
    if id == tempid:
        #LoginWin.destroy() #마지막에 추가
        ### 로그인 후 메인 화면 ###        
        Mainwin=tk.Tk()
        Mainwin.title("메인화면")
        Mainwin.geometry("650x600+625+150")
        Mainwin.resizable(False, False)
        
        Toplabel1=tk.Label(Mainwin, text="항공예약시스템", width=30, height=2, font=('Arial', 40), fg="black", bg="skyblue")
        Toplabel1.pack(side='top')
        
        ReserLKBT=tk.Button(Mainwin, relief="solid", text="항공 조회", width=20, bg="white", command=AirSearchBT) #항공 조회 버튼
        ReserLKBT.place(x=480, y=150)
        
        ReserBT=tk.Button(Mainwin, relief="solid", text="예약", width=20, bg="white", command=AirResBT) #예약 버튼
        ReserBT.place(x=480, y=200)

        LookupBT=tk.Button(Mainwin, relief="solid", text="예약 조회", width=20, bg="white", command=MyResBT) #조회 버튼
        LookupBT.place(x=480, y=250)
        
        UdUserBT=tk.Button(Mainwin, relief="solid", text="정보 변경", width=20, bg="white", command=InfoChBT) #정보 변경 버튼
        UdUserBT.place(x=480, y=300)

        Descombobox=ttk.Combobox(Mainwin, height=15, values=DEST_Value)
        Descombobox.place(x=70, y=150)
        Descombobox.set("목적지")
        
        Datecombobox=ttk.Combobox(Mainwin, height=15, values=DATE_Value)
        Datecombobox.place(x=270, y=150)
        Datecombobox.set("날짜")
        
        Mainwin.mainloop()
    else:
        msgbox.showinfo("로그인에러", "여권번호가 존재하지 않습니다. 여권번호를 다시 확인하거나 회원가입을 해주세요.")

### 회원가입 버튼 함수 ###
def SignUpWindow():
    def sgBT():
        cntt = 0
        global count
        conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Passenger;')

        count = cursor.fetchall()
        cursor.execute('SELECT passenger_passid FROM Passenger;')
        Pid = cursor.fetchone()

        while Pid:
            tempPid = Pid[0]
            if IdEt.get() == tempPid:
                msgbox.showinfo("회원가입에러", "해당 여권번호는 이미 가입되었습니다. 다시 확인해주세요.")
                SignupWin.destroy()
                break
            else:
                cntt += 1
                if int(count[0][0]) == cntt:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO Passenger (passenger_passid, passenger_name, passenger_email, passenger_dateofbrith, passenger_phonenumber, passenger_uniqueness) values (%s, %s, %s, %s, %s, %s);', (IdEt.get(), NameEt.get(), EmailEt.get(), BirthEt.get(), PhoneNumEt.get(), UniqeEt.get()))
                    conn.commit()
                    cntt=0
                    msgbox.showinfo("회원가입완료", "회원가입이 완료되었습니다.")
                    SignupWin.destroy()
                    break
                Pid = cursor.fetchone()
        conn.close()
        
    SignupWin=tk.Toplevel(LoginWin)
    SignupWin.title("회원가입")
    SignupWin.geometry("450x500+725+250")
    SignupWin.resizable(False, False)
    
    Id=tk.Label(SignupWin, text="여권번호",width=15, height=2)
    Id.place(x=54, y=15)
    
    IdEt=tk.Entry(SignupWin, width=40)
    IdEt.insert(0, "Passid")
    IdEt.place(x=85, y=50)
    
    Name=tk.Label(SignupWin, text="이름",width=15, height=2)
    Name.place(x=43, y=70)
    
    NameEt=tk.Entry(SignupWin, width=40)
    NameEt.insert(0, "Name")
    NameEt.place(x=85, y=105)
    
    Email=tk.Label(SignupWin, text="이메일",width=15, height=2)
    Email.place(x=49, y=140)
    
    EmailEt=tk.Entry(SignupWin, width=40)
    EmailEt.insert(0, "Email")
    EmailEt.place(x=85, y=175)
    
    Birth=tk.Label(SignupWin, text="생년월일(ex)2022-12-31)",width=25, height=2)
    Birth.place(x=64, y=210)
    
    BirthEt=tk.Entry(SignupWin, width=40)
    BirthEt.insert(0, "date of birth")
    BirthEt.place(x=85, y=245)
    
    PhoneNum=tk.Label(SignupWin, text="핸드폰번호",width=15, height=2)
    PhoneNum.place(x=62, y=280)
    
    PhoneNumEt=tk.Entry(SignupWin, width=40)
    PhoneNumEt.insert(0, "PhoneNumber")
    PhoneNumEt.place(x=85, y=315)
    
    Uniqe=tk.Label(SignupWin, text="특이사항",width=15, height=2)
    Uniqe.place(x=56, y=350)
    
    UniqeEt=tk.Entry(SignupWin, width=40)
    UniqeEt.insert(0, "특이사항")
    UniqeEt.place(x=85, y=385)
    
    SignBT=tk.Button(SignupWin, relief="solid", text="회원가입 완료", width=30, bg="yellow", command=sgBT)# command=sgBT
    SignBT.place(x=120, y=450)
    
    SignupWin.mainloop()

### 로그인 화면 ###
LoginWin = tk.Tk()
LoginWin.title("항공예약시스템")
LoginWin.geometry("400x300+750+300")
LoginWin.resizable(False, False)

Main=tk.Label(LoginWin, text="10조 항공예약시스템", width=18, height=3, font=('Arial', 30), fg="black", bg="skyblue")
Main.pack(side='top')

IdTBox=tk.Entry(LoginWin, width=30, bg="white")
IdTBox.insert(0, "Passid")
IdTBox.place(x=90, y=160)

LoginBT=tk.Button(LoginWin, relief="solid", text="로그인", width=25, bg="green2", command=LoginBTClick)
LoginBT.place(x=105, y=200)

SignUpBT=tk.Button(LoginWin, relief="solid", text="회원가입", width=25, bg="gray78", command=SignUpWindow)
SignUpBT.place(x=105, y=240)

LoginWin.mainloop()
