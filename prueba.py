import PySimpleGUI as sg

layout = [
    [sg.Text("Hola, PySimpleGUI!")],
    [sg.Button("OK")]
]

window = sg.Window("Prueba", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "OK":
        break

window.close()