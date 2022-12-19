import PySimpleGUI as pg
import sqlite3
from geopy.geocoders import Nominatim
import haversine as hs

print(pg)
pg.theme("DarkAmber")


def elder_info(values):
    information="Senior:"
    name=values['-NAME-']
    city=values['-city-']
    adress=values['-ADRESS-']
    email=values['-EMAIL-']
    phone=values['-PHONENUMBER-']
 #   if values[-FEMALE-]:

def Submitinfo(values):
    conn = sqlite3.connect('central.db')
    cursor = conn.cursor()
    information="Senior:"
    name=values['-NAME-']
    city=values['-city-']
    address=values['-ADRESS-']
    email=values['-EMAIL-']
    phone=values['-PHONENUMBER-']
    gender=""
    need_food=False
    if values['-MALE-']:
        gender="M"
    elif values['-FEMALE-']:
        gender="F"
    else:
        gender="nonbinary"
   # if values['-YESFOOD-']:
    #    need_food="TRUE"
    #else:
    #    need_food="FALSE"
    tuple=(name, gender ,city,address,email,phone)

    cursor.execute('''INSERT INTO ELDERS
                   (NAME,GENDER,CITY, ADDRESS, EMAIL, PHONE_NUMBER) VALUES (?,?,?,?,?,?)''',tuple)
    conn.commit()
    conn.close()

def ElderSubmit():     
        layout=[
            [pg.Text("Enter Seniors name"),pg.Input(key ='-NAME-',  do_not_clear=True, size=(20,1))],
            [pg.Text("Enter Seniors city"),pg.Input(key ='-city-',  do_not_clear=True, size=(20,1))],
            [pg.Text("Enter Seniors adress"),pg.Input(key ='-ADRESS-',  do_not_clear=True, size=(20,1))],
            [pg.Text("Enter Seniors email"),pg.Input(key ='-EMAIL-',  do_not_clear=True, size=(20,1))],
            [pg.Text("Enter Seniors phone number"),pg.Input(key ='-PHONENUMBER-',  do_not_clear=True, size=(20,1))],
            [pg.Radio("Male","SEX",key='-MALE-'),pg.Radio("Female","SEX",key='-FEMALE-'),pg.Radio("Nonbinary","SEX",key='-NONBINARY-')],
            #[pg.Text("Can they Drive"),pg.Radio("YES","DRIVE",key='-YESDRIVE-'),pg.Radio("NO","DRIVE",key='-DRIVE-')],

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
                loc=Nominatim(user_agent="GetLoc")
                print(loc.geocode(values['-ADRESS-']))
                if loc.geocode(values['-ADRESS-']): # returns None therefore, 
                    Submitinfo(values)
                    pg.popup("Senior Submitted",font=('Any 50'))
                    break
                else:
                    pg.popup("invalid adress",font=('Any 50'))
                
            #elif values['-NOFOOD-']:
            #    print("they need food")
                
            #print(values[0])
            #list_of_names.append(values[0])
            
    # print(list_of_names)
        window.close()
        
        
#ElderSubmit() 