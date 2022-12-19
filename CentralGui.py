import ElderUse
import submitData
import CaregiverUse
import PySimpleGUI as pg

def Central():
        layout=[
            [pg.Text('Central Terminal for Seniority')],
            
            [pg.Button("Submit Users page")],
            [pg.Button("For Seniors")],
            [pg.Button("For Volunteers")]
            ]
        window= pg.Window("Central", layout,resizable=True,font=('Any 50'))
        #event loop
        while True:
            event,values = window.read()
            if event == "Submit Users page":
                submitData.Submitpage()
            elif event ==pg.WIN_CLOSED:
                break
            elif event == "For Seniors":
                ElderUse.ElderUse()
            elif event == "For Volunteers":
                CaregiverUse.CareUse()
                
            #elif values['-NOFOOD-']:
            #    print("they need food")
                
            #print(values[0])
            #list_of_names.append(values[0])
            
    # print(list_of_names)
        window.close()
        
        
Central() 