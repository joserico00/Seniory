import PySimpleGUI as pg
import sqlite3
from geopy.geocoders import Nominatim
import haversine as hs


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

def ListofCaregivers(values):
    conn = sqlite3.connect('central.db')
    cursor = conn.cursor()
    
    ID= values['-ID-']
    print('ID:',ID)
    cursor.execute('''SELECT CITY FROM ELDERS WHERE ID == (?) ''',(ID) )
    
    city=cursor.fetchone()
    print(city)
    cursor.execute(
    "SELECT * FROM CAREGIVER WHERE CITY == %s  AND AVAILABILITY==1"  % (formatString(city[0]))
    )
    result=cursor.fetchall()
    print(result)
    
    cursor.execute('''SELECT ADDRESS FROM ELDERS WHERE ID == (?) ''',(ID) )
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
    cursor.execute('''SELECT EXISTS(SELECT * from ELDERS WHERE ID=(?) )''',tuple )
    bol=cursor.fetchone()
    print("bools suppose :  " , bol)
    conn.commit()
    conn.close()
    return bol[0]
#def chosencaregiver(value):
    
def caregiverList(carelist,ElderAdress):
    newlist=[]
    print("Elder adress is: ", ElderAdress)
    for i in carelist:
        print("caregiver adress is: ", i[3])
        diffrence= calculateMiles(ElderAdress[0],i[3])
        newlist.append([" name: "+i[0],' gender: '+i[1],' city: '+i[2],' address: '+i[3],' email: '+i[4],' number: '+i[5],' Miles away: '+ diffrence ])
    
    #maybe add moore to it
    layout=[
        [pg.Listbox(values=newlist,size=(50,5), select_mode='single', key = '-carechoice-',font=('Any 50'))],
        [pg.Button("exit"),pg.Button("Submit")]
    ]
    window= pg.Window("List of avaliable volunteers at this time", layout,modal=True,font=('Any 50'))
    while True:
        event,values = window.read()
        if event == "exit":
            break
        elif event in ("exit",pg.WIN_CLOSED):
            break
        elif event == "Submit":
            #chosencaregiver(values)
            pg.popup("Volunteers have been notified wait shortly ",font=('Any 50'))
            #msg=pg.popup_get_text("what do you need?",font=('Any 50'))
            #conn = sqlite3.connect('central.db')
            #cursor = conn.cursor()
            #cursor.execute('''UPDATE ELDERS SET HELP = (?) FROM ELDERS WHERE ID==(?) ''',(msg) )
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
                    ID=values['-ID-']
                    cursor = conn.cursor()
                    cursor.execute('''SELECT volunteer_helping FROM ELDERS WHERE ID==(?) ''',(ID) )
                    attended=cursor.fetchone()
                    print("ATTENDED", attended)
                    if attended[0]==-1:
                        cursor.execute('''UPDATE ELDERS SET  NEED_HELP = 1  WHERE ID == (?) ''',(ID) )
                        cursor.execute('''SELECT ADDRESS FROM ELDERS WHERE ID == (?) ''',(ID) )
                        msg=pg.popup_get_text("what do you need?",font=('Any 50'))
                        cursor.execute('''UPDATE ELDERS SET  HELP = (?)  WHERE ID == (?) ''',(msg,ID) )
                        conn.commit()

                        print("is there any id",CheckID(values))
                        carelist,address=ListofCaregivers(values)
                        caregiverList(carelist,address)
                        
                    else:
                        choice=pg.popup_yes_no("has your caregiver left?",font=('Any 50'))
                        if choice=='Yes':
                            cursor.execute('''UPDATE CAREGIVER SET availability= 1  WHERE ID == (?) ''',(attended[0],) )
                            cursor.execute('''UPDATE ELDERS SET volunteer_helping= -1  WHERE ID == (?) ''',(ID) )
                            
                        else:
                            pg.popup("you still have your caretaker",font=('Any 50'))
                            
                    conn.commit()
                    conn.close()
                    
                
                else:
                    pg.popup("wrong ID",font=('Any 50'))
            #elif values['-NOFOOD-']:
            #    print("they need food")
                
            #print(values[0])
            #list_of_names.append(values[0])
            
    # print(list_of_names)
        window.close()
        

def ElderUse(): 
        print(pg)
        pg.theme("DarkAmber")    
        layout=[
            [pg.Text("Seniority")],

            [pg.Button("Notify for Help"), pg.Button("Exit")]
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
            elif event == "Notify for Help":
                Notify()
                break
            #elif values['-NOFOOD-']:
            #    print("they need food")
                
            #print(values[0])
            #list_of_names.append(values[0])
            
    # print(list_of_names)
        window.close()
        
#ElderUse()
