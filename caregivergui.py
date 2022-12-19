import PySimpleGUI as pg
import sqlite3
from geopy.geocoders import Nominatim
import haversine as hs

def caregiver_info(values):
    information="caregiver:"
    name=values['-NAME-']
    city=values['-city-']
    adress=values['-ADRESS-']
    email=values['-EMAIL-']
    phone=values['-PHONENUMBER-']
 #   if values[-FEMALE-]:

def Submitinfo(values):
    conn = sqlite3.connect('central.db')
    cursor = conn.cursor()
    information="CAREGIVER:"
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

    tuple=(name, gender ,city,address,email,phone)

    cursor.execute('''INSERT INTO CAREGIVER
                   (NAME,GENDER,CITY, ADDRESS, EMAIL, PHONE_NUMBER) VALUES (?,?,?,?,?,?)''',tuple)
    conn.commit()
    conn.close()

def CaregiverSubmit():
    print(pg)
    pg.theme("DarkAmber")

    layout=[
        [pg.Text("Enter caregiver name"),pg.Input(key ='-NAME-',  do_not_clear=True, size=(20,1))],
        [pg.Text("Enter caregiver city"),pg.Input(key ='-city-',  do_not_clear=True, size=(20,1))],
        [pg.Text("Enter caregiver adress"),pg.Input(key ='-ADRESS-',  do_not_clear=True, size=(20,1))],
        [pg.Text("Enter caregiver email"),pg.Input(key ='-EMAIL-',  do_not_clear=True, size=(20,1))],
        [pg.Text("Enter caregiver phone number"),pg.Input(key ='-PHONENUMBER-',  do_not_clear=True, size=(20,1))],
        [pg.Radio("Male","SEX",key='-MALE-'),pg.Radio("Female","SEX",key='-FEMALE-'),pg.Radio("Nonbinary","SEX",key='-NONBINARY-')],
        #[pg.Text("Can they Drive"),pg.Radio("YES","DRIVE",key='-YESDRIVE-'),pg.Radio("NO","DRIVE",key='-DRIVE-')],
        #[pg.Text("Do they need food"),pg.Radio("YES","FOOD",key='-YESFOOD-'),pg.Radio("NO","FOOD",key='-NOFOOD-')],

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
                pg.popup("caregiver submitted",font=('Any 50'))
                break
            else:
                pg.popup("Invalid adress",font=('Any 50'))
        
    window.close()
    
#CaregiverSubmit()