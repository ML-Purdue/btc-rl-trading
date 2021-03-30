import PySimpleGUI as sg
import random
import numpy as np

print('Starting up...')   # This seems to be neccessary sometimes

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Boiler up!')],
            [sg.Text('Current balance: $0', key='balanceText', auto_size_text=True)],
            [sg.Listbox(values=['Current Holdings...'], size=(30, 10), key='currentList')],
            [sg.Button('Start trading bot', key='startButton'), sg.Button('Close trading bot', key='endButton')],
            [sg.Button('Sell all', key='panicButton')]]

# Create the Window
window = sg.Window('SIGAI BTC Terminal', layout, resizable=True)

def updateCurrentBalance(balance):
    updatetxt = 'Current balance: $'
    updatetxt += balance
    window.Element('balanceText').Update(updatetxt)

def updateCurrentHoldings(list):
    window.Element('currentList').Update(list)



# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break


    if event == "startButton":
        # Call upon start bot function
        print(event)


    if event == "endButton":
        # Call upon end bot function
        print(event)

    if event == "panicButton":
        # Call upon panic sell button from bot
        print(event)


window.close()
