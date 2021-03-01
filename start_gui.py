import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Boiler up!')],
            [sg.Text('Current balance: $0', key='balanceText')],
            [sg.Button('Start trading bot', key='startButton'), sg.Button('Close trading bot', key='endButton')],
            [sg.Button('Panick sell', key='panicButton')]]

# Create the Window
window = sg.Window('SIGAI BTC Terminal', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()
