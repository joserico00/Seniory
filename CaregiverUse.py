import PySimpleGUI as pg
import sqlite3
from geopy.geocoders import Nominatim
import haversine as hs

def searchElders(array):
    conn = sqlite3.connect('central.db')
    cursor = conn.cursor()
    liste=array[0]
    copy=[]
    for i in liste:
        copy.append(i[1+(i.find(':')):])
    copy.pop()
    print(copy)
    tup=tuple(copy)
    cursor.execute('''SELECT ID FROM ELDERS WHERE NAME == (?) AND ADDRESS == (?) ''',(tup[0],tup[3]) )
    RESULT=cursor.fetchone()
    print(RESULT)
    return  RESULT[0]
def calculateMiles(loca1,loca2):  
  print(loca1)
  print(loca2)
  
  loc = Nominatim(user_agent="GetLoc")
  getLoc = loc.geocode(loca1)
  
  loc1=(getLoc.latitude,getLoc.longitude)
  getLoc = loc.geocode(loca2)
  loc2=(getLoc.latitude,getLoc.longitude)
  print(loc1,loc2)
  print(hs.haversine(loc1,loc2))
  return(str(hs.haversine(loc1,loc2)))

def formatString(string):
  return "'" + string + "'"

def Listofelder(values):
    conn = sqlite3.connect('central.db')
    cursor = conn.cursor()
    
    ID= values['-ID-']
    print('ID:',ID)
    cursor.execute('''SELECT CITY FROM CAREGIVER WHERE ID == (?) ''',(ID) )
    
    city=cursor.fetchone()
    print(city)
    cursor.execute(
    "SELECT * FROM ELDERS WHERE CITY == %s  AND NEED_HELP==1" % (formatString(city[0]))
    )
    result=cursor.fetchall()
    print(result)
    
    cursor.execute('''SELECT ADDRESS FROM CAREGIVER WHERE ID == (?) ''',(ID) )
    adress=cursor.fetchone()
    conn.commit()
    conn.close()
    newresult=[]
    for i in result:
        newresult.append(i[1:])
    return(newresult,adress)
    

def CheckID(values):
    
    conn = sqlite3.connect('central.db')
    cursor = conn.cursor()
    tuple=values['-ID-']
    #cursor.execute('''SELECT ID FROM ELDERS
    #            (NAME) VALUES (?)''',tuple)
    cursor.execute('''SELECT EXISTS(SELECT * from CAREGIVER WHERE ID=(?) )''',tuple )
    bol=cursor.fetchone()
    print("bools suppose :  " , bol)
    conn.commit()
    conn.close()
    return bol[0]
#def chosencaregiver(value):
    
def ElderList(carelist,CareAdress):
    newlist=[]
    print("Elder adress is: ", CareAdress)
    
    for i in carelist:
        print("caregiver adress is: ", i[3])
        diffrence= calculateMiles(CareAdress[0],i[3])
        newlist.append(["name:"+i[0],'gender:'+i[1],'city:'+i[2],'address:'+i[3], 'email:'+i[4],'number:'+i[5],'Miles away:'+ diffrence ])
        
    #maybe add moore to it
    layout=[
        [pg.Listbox(values=newlist,size=(50,5), select_mode='single', key = '-carechoice-')],
        [pg.Button("exit"),pg.Button("Submit")]
    ]
    window= pg.Window("Form", layout,modal=True,font=('Any 50'))

    while True:
        event,values = window.read()
        if event in ("exit",pg.WIN_CLOSED):
            break
        elif event == "exit":
            break
        elif event == "Submit":
            print(values['-carechoice-'])

            re=values['-carechoice-']
            Elderid=searchElders(re)
            conn = sqlite3.connect('central.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT HELP FROM ELDERS WHERE ID==(?) ''',(Elderid,) )
            msg=cursor.fetchone()
            choice = pg.popup_yes_no("Help Details:",msg,font=('Any 50'))
            conn.commit()
            conn.close()

            
            #chosencaregiver(values)
            #pg.popup("good id")
            if choice=='Yes':
                pg.popup("succesfully chose Senior",font=('Any 50'))
                return values['-carechoice-']

def Notify(): 
        print(pg)
        pg.theme("DarkAmber")    
        layout=[
            [pg.Text("Your ID"),pg.Input(key ='-ID-',  do_not_clear=True, size=(20,1))],
            [pg.Button("Submit"), pg.Button("Cancel")]
            ]
        window= pg.Window("Form", layout,font=('Any 50'))
        list_of_names=[]
        #event loop
        while True:
            event,values = window.read()
            if event == "Cancel":
                break
            elif event ==pg.WIN_CLOSED:
                break
            elif event == "Submit":
                if CheckID(values):
                    
                    conn = sqlite3.connect('central.db')
                    carerID=values['-ID-']
                    cursor = conn.cursor()
                    cursor.execute('''SELECT AVAILABILITY  FROM CAREGIVER  WHERE ID == (?) ''',(carerID) )
                    ava=cursor.fetchone()
                    print("AVABIALITY FOR CURRENT ID: ", ava)
                    conn.commit()
                    
                    
                    print("is there any id",CheckID(values))
                    if  ava[0] == 0:
                        choice=pg.popup_yes_no('have you finished with your current Senior',font=('Any 50'))
                        print("CHOICE: ",choice)
                        if choice== 'Yes': #modify database to free up caretaker and put the one caring for to -1 in table 
                            cursor.execute('''UPDATE CAREGIVER SET AVAILABILITY=1 WHERE ID == (?)''',(carerID) )
                            cursor.execute('''UPDATE ELDERS SET  VOLUNTEER_HELPING=-1 WHERE VOLUNTEER_HELPING == (?)''',(carerID) )
                            conn.commit()
                        else: #runin it aguan
                            pg.popup("already taking care of one senior",font=('Any 50'))
                        #already cuidando a alguien
                        
                    else:
                        elderlist,address=Listofelder(values)
                        re = ElderList(elderlist,address)
                        if re:
                            print('notify:', re[0][0])
                            Elderid=searchElders(re)
                            cursor.execute('''UPDATE CAREGIVER SET AVAILABILITY=0 WHERE ID == (?)''',(carerID) )
                            cursor.execute('''UPDATE ELDERS SET  VOLUNTEER_HELPING=(?),NEED_HELP=0 WHERE ID == (?)''',(carerID,Elderid) )
                            conn.commit()
                            pg.popup("You Have Succesfuly gotten the request of the Senior",font=('Any 50'))
                    conn.close()
                
                else:
                    pg.popup("wrong ID",font=('Any 50'))
            #elif values['-NOFOOD-']:
            #    print("they need food")
                
            #print(values[0])
            #list_of_names.append(values[0])
            
    # print(list_of_names)
        window.close()
        

def CareUse(): 
        print(pg)
        pg.theme("DarkAmber")    
        layout=[
            [pg.Text("Seniority")],

            [pg.Button("Check if needed"), pg.Button("Exit")]
            ]
        window= pg.Window("Form", layout,font=('Any 50'))
        list_of_names=[]
        #event loop
        while True:
            event,values = window.read()
            if event == "Exit":
                break
            elif event ==pg.WIN_CLOSED:
                break
            elif event == "Check if needed":
                Notify()
                break
            #elif values['-NOFOOD-']:
            #    print("they need food")
                
            #print(values[0])
            #list_of_names.append(values[0])
            
    # print(list_of_names)
        window.close()
        
#ElderUse()
