"""
EES Project Automatic Reporting Software - Release Version 1.7.0
Developed by Fraser Love on 14/03/19

Automatic reporting software for Evolution and lients with the aim to improve communication
between company and clients and help keep machine downtime to a minimum.

Core functionality is that it allows clients to send off reports to Evolution.

All known bugs have been patched, however if through use of the software you notice
a bug contact us with detail of the bug to help get it patched.

--------------------------------------
Final Release
--------------------------------------

Features
- Automatic CSV file creation
- Automatic additon of user entered values to CSV files
- Login with username and password
- Stylish GUI
- Hashed passwords and usernames for extra security
- Extra UI robustness enhancements
- Automatic email of reports
- Login cooldowns for extra security
- Automatic email of sucessfull and unsuccessfull login attempts
- Server login increasing robustness
- Enhanced UI displaying more useful data
- Client Side Storage of Information
- Ability to upload content
- Automatic Table UI Updates
- Different colour themes
- Automatic Report PDF creation
- PDF Language Translation
- UI Error Output System
- Image webcam capture system
- Video webcam and screen capture system
- Integrated smartphone streaming
- Integrated Google Text To Speech
- Integrated AI Image Recognition
- Integrated Image Capturing System
"""

from tkinter import *
import numpy as np
import requests
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Image
from textblob import TextBlob
from flask import Flask
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from twilio.rest import Client
from passlib.hash import pbkdf2_sha256
from threading import Thread
import speech_recognition as sr
from PIL import Image, ImageGrab
import datetime, csv, os, time, hashlib, uuid, smtplib, threading, urllib, pyglet, pytesseract, cv2
from gtts import gTTS

try:
    pyglet.lib.load_library('avbin')
    pyglet.have_avbin=True
except:
    print("Error: avbin not installed")
    append_error("Error: avbin not installed")

def app():

    def gen_folders():
        if os.path.exists("{}/media".format(os.getcwd())) == False:
            os.makedirs("{}/media".format(os.getcwd()))
        if os.path.exists("{}/data".format(os.getcwd())) == False:
            os.makedirs("{}/data".format(os.getcwd()))
        if os.path.exists("{}/pdfs".format(os.getcwd())) == False:
            os.makedirs("{}/pdfs".format(os.getcwd()))

    def screen_cap():
        vid_path = ""
        try:
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            exists = True
            i = 1
            while exists:
                if os.path.isfile(("media/video-{}.mp4").format(i)) == False:
                    out = cv2.VideoWriter(("media/video-{}.mp4".format(i)), fourcc, 24.0, (root.winfo_screenwidth(), root.winfo_screenheight()))
                    exists = False
                    vid_path = ("media/video-{}.mp4".format(i))
                else:
                    i += 1
            while True:
                img = ImageGrab.grab()
                img_np = np.array(img)
                frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                cv2.imshow("Screen Capture - Click Enter to Stop", frame)
                out.write(frame)
                if cv2.waitKey(1) & 0xFF == 13:
                    break
            out.release()
            cv2.destroyAllWindows()
        except:
            print("Error: screen capture failed")
            append_error("Error: screen capture failed")
        return vid_path

    def video_cap():
        vid_path = ""
        try:
            cap = cv2.VideoCapture(0)
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            exists = True
            i = 1
            while exists:
                if os.path.isfile(("media/video-{}.mp4").format(i)) == False:
                    out = cv2.VideoWriter(("media/video-{}.mp4".format(i)), fourcc, 24.0, (int(width), int(height)))
                    exists = False
                    vid_path = ("media/video-{}.mp4".format(i))
                else:
                    i += 1
            while True:
                ret, frame = cap.read()
                cv2.imshow("Video Capture - Click Enter to Confirm", frame)
                out.write(frame)
                if cv2.waitKey(1) & 0xFF == 13:
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()
        except:
            vid_path=""
            print("Error: video capture failed - no camera detected")
            append_error("Error: video capture failed - no camera detected")
        return vid_path

    def image_cap():
        img_path = ""
        try:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow("Image Capture - Click Enter to Confirm", frame)
                if cv2.waitKey(1) & 0xFF == 13:
                    break
            cv2.destroyAllWindows()
            cv2.imshow("Image", frame)
            exists = True
            i = 1
            while exists:
                if os.path.isfile(("media/image-{}.jpg").format(i)) == False:
                    cv2.imwrite(("media/image-{}.jpg".format(i)), frame)
                    exists = False
                    img_path = ("media/image-{}.jpg".format(i))
                else:
                    i += 1
            cap.release()
        except:
            img_path = ""
            print("Error: image capture failed - no camera detected")
            append_error("Error: image capture failed - no camera detected")
        return img_path

    def itt():
        try:
            img = Image.open("temp.jpg")
            pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
            result = pytesseract.image_to_string(img)
            os.remove("temp.jpg")
        except:
            result = ""
            print("Error: Tesseract not installed")
            append_error("Error: speech entry failed - tesseract not installed")
        return result

    def image_capture():
        try:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow("Image Capture - Click Enter to Confirm", frame)
                if cv2.waitKey(1) & 0xFF == 13:
                    break
            cv2.destroyAllWindows()
            cv2.imshow("Image", frame)
            cv2.imwrite("temp.jpg", frame)
            cap.release()
            result = itt()
        except:
            result = ""
            print("Error: scanning image failed - no camera detected")
            append_error("Error: scanning image failed - no camera detected")
        return result

    def tts(text, lang):
        try:
            file = gTTS(text = text, lang = lang)
            file.save("temp.mp3")
            music = pyglet.media.load("temp.mp3", streaming = False)
            music.play()
            os.remove("temp.mp3")
        except:
            print("Error: unable to play feedback - avbin not installed")
            append_error("Error: unable to play feedback - avbin not installed")


    def speech_man():
        r = sr.Recognizer()
        text = ""
        try:
            with sr.Microphone() as source:
                try:
                    audio = r.listen(source)
                    text = r.recognize_google(audio)
                    print("You said:\n" + text)
                    lang = "en"
                    tts(text + ", was entered", lang)
                except:
                    tts("Error: voice not detected, try again", "en")
                    append_error("Error: voice not detected - try again")
        except:
            print("Error: speech entry failed - no microphone detected")
            append_error("Error: speech entry failed - no microphone detected")
        return text

    def display_time():
        global time_canvas, time_text, uk_text, uk_work, italy_work, italy_text
        time_canvas = Canvas(page, width=240, height=60, bg=check_panels(), borderwidth=0, bd=0, highlightthickness=0, relief='flat')
        time_canvas.place(x=965, y=15, anchor="n")
        time_text = Label(page, text="TIME", bg=check_panels(), fg=check_fg(), font=('Segoe UI', '18', 'bold'))
        time_text.place(x=960, y=35, anchor="center")
        uk_text = Label(page, text="", bg=check_panels(), fg=check_fg(), font=('Segoe UI', '12'))
        uk_text.place(x=890, y=35, anchor="center")
        uk_work = Label(page, text="", bg=check_panels(), fg=check_fg(), font=('Segoe UI', '9'))
        uk_work.place(x=890, y=60, anchor="center")
        italy_work = Label(page, text="", bg=check_panels(), fg=check_fg(), font=('Segoe UI', '9'))
        italy_work.place(x=1035, y=60, anchor="center")
        italy_text = Label(page, text="", bg=check_panels(), fg=check_fg(), font=('Segoe UI', '12'))
        italy_text.place(x=1035, y=35, anchor="center")
        while True:
            uk_now = datetime.datetime.now()
            italy_now = uk_now + datetime.timedelta(hours=1)
            uk_text.config(text=("UK: {}".format(uk_now.strftime("%H:%M"))))
            italy_text.config(text=("Italy: {}".format(italy_now.strftime("%H:%M"))))
            if int(uk_now.strftime("%H")) > 9 and int(uk_now.strftime("%H")) < 17:
                uk_work.config(text=("Working"))
            else:
                uk_work.config(text=("Not Working"))
            if int(italy_now.strftime("%H")) > 9 and int(italy_now.strftime("%H")) < 17:
                italy_work.config(text=("Working"))
            else:
                italy_work.config(text=("Not Working"))

    def clear():
        global error_list, error_text_list, bg_canvas
        error_list = []
        error_text_list = []
        append_error("")

    def error_system(page):
        global error_header, error_canvas, clear_button
        error_header = Label(page, text="ERRORS", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
        error_header.place(x=1715, y=790, anchor="center")
        error_canvas = Canvas(page, width=370, height=170, bg=check_panels(), borderwidth=0, bd=0, highlightthickness=0, relief='flat')
        error_canvas.place(x=1715, y=820, anchor="n")
        clear_button = Button(page, text="Clear", fg="white", bg="#474747", borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=clear)
        clear_button.place(x=1530, y=1000)

    def append_error(error):
        global error_text_list, error_list, error_canvas
        error_canvas.destroy()
        error_canvas = Canvas(page, width=370, height=170, bg=check_panels(), borderwidth=0, bd=0, highlightthickness=0, relief='flat')
        error_canvas.place(x=1715, y=820, anchor="n")
        if error != "":
            error_list.append(error)
        if len(error_list) > 8:
            error_list = error_list[1:]
        count = 0
        for entry in error_list:
            error_text = Label(page, text=entry, bg=check_panels(), fg=check_fg(), font=('Segoe UI', '8'))
            error_text.place(x=1534, y=823+count*20)
            error_text_list.append(error_text)
            count += 1

    def check_panels():
        if theme_slider.get() == 1:
            panels = "#CCCCCC"
        else:
            panels = "#333333"
        return panels

    def check_buttons():
        if theme_slider.get() == 1:
            panels = "#1366C4"
        else:
            panels = "#333333"
        return panels
    def check_bg():
        if theme_slider.get() == 1:
            bg = "#E9E9E9"
        else:
            bg = "#161616"
        return bg

    def check_fg():
        if theme_slider.get() == 1:
            fg = "#000000"
        else:
            fg = "#ffffff"
        return fg

    def initalise_app():
        root = Tk()
        return root

    def close_window():
        root.destroy()

    def root_screen(root):
        tries = 3

        def navbar(root):
            global nav, title, exit
            nav = Frame(root, bg="#333333", width=1920, height=20)
            title = Label(nav, text="Automatic Reporting Software", bg="#333333", fg="white")
            exit = Button(nav, text="Exit", fg="white", bg="#333333", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white", command=close_window)
            nav.place(x=0, y=0, anchor="nw")
            exit.place(x=1920, y=10, anchor="e")
            title.place(x=960, y=10, anchor="center")

        def gen_id():
            form_id = 1
            if os.path.isfile("data/data.csv"):
                file = open("data/data.csv", "r")
                for row in csv.reader(file):
                    form_id += 1
            return form_id

        def main(root):
            def destroy_widgit(widgit):
                widgit.destroy()

            def live_stream(page, ip, port):
                global ls_error_text
                try:
                    url = "http://{}:{}/shot.jpg".format(ip, port)
                    while True:
                        img_resp = requests.get(url)
                        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                        img = cv2.imdecode(img_arr, -1)
                        cv2.imshow("PhoneCam - Press Enter to Exit", img)
                        if cv2.waitKey(1) & 0xFF == 13:
                            break
                    cv2.destroyAllWindows()
                except:
                    ls_error_text = Label(page, text="Error: cannot contact device", bg=check_bg(), fg="red", font=('Segoe UI', '10'))
                    ls_error_text.place(x=1540, y=525, anchor="w")
                    ls_error_text.after(2000, destroy_widgit, ls_error_text)
                    append_error("Error: live stream failed - cannot contact device")

            def send_email(message, subject, login=False):
                email = sending_email.get()
                e_password = email_pass.get()
                if login == True:
                    send_to_email = email
                else:
                    send_to_email = recieving_email.get()

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))
                if len(file_array) > 0 and login == False:
                    for i in range(0,len(file_array)):
                        if file_array[i] != "":
                            attachment = open(file_array[i], "rb")
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload((attachment).read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', "attachment; filename= %s" % file_name_array[i])
                            msg.attach(part)

                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email, e_password)
                    text = msg.as_string()
                    server.sendmail(email, send_to_email, text)
                    server.quit()
                except:
                    print("Error: email not sent")
                    append_error("Error: sending email failed - check username and password")

            def check_attachments():
                if len(file_array) > 0:
                    return "True"
                else:
                    return "False"

            def translate(language, title, job_str, time_str, engineer_str, manufacturer_str, model_str, machine_id_str, customer_str, contact_str, location_str, type_str, charge_str, description_str):
                title_tb= TextBlob(title)
                job_tb = TextBlob(job_str)
                time_tb = TextBlob(time_str)
                engineer_tb = TextBlob(engineer_str)
                manufacturer_tb = TextBlob(manufacturer_str)
                model_tb = TextBlob(model_str)
                machine_id_tb = TextBlob(machine_id_str)
                customer_tb = TextBlob(customer_str)
                contact_tb = TextBlob(contact_str)
                location_tb = TextBlob(location_str)
                type_tb = TextBlob(type_str)
                charge_tb = TextBlob(charge_str)
                description_tb = TextBlob(description_str)
                title = title_tb.translate(to=language)
                job_str = job_tb.translate(to=language)
                time_str = time_tb.translate(to=language)
                engineer_str = engineer_tb.translate(to=language)
                manufacturer_str = manufacturer_tb.translate(to=language)
                model_str = model_tb.translate(to=language)
                machine_id_str = machine_id_tb.translate(to=language)
                customer_str = customer_tb.translate(to=language)
                contact_str = contact_tb.translate(to=language)
                location_str = location_tb.translate(to=language)
                type_str = type_tb.translate(to=language)
                charge_str = charge_tb.translate(to=language)
                description_str = description_tb.translate(to=language)
                return title, job_str, time_str, engineer_str, manufacturer_str, model_str, machine_id_str, customer_str, contact_str, location_str, type_str, charge_str, description_str

            def create_pdf(page, id, time, name, manufacturer_name, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge, description, language):
                global locked
                if locked == False:
                    title = "Report"
                    job_str = ("Job Number: {}".format(id))
                    time_str = ("Time Sent: {}".format(time))
                    engineer_str = ("Engineer Name: {}".format(name))
                    manufacturer_str = ("Manufacturer Name: {}".format(manufacturer_name))
                    model_str = ("Machine Model: {}".format(machine_model))
                    machine_id_str = ("Machine ID: {}".format(machine_id))
                    customer_str = ("Customer Name: {}".format(customer_name))
                    contact_str = ("Contact Name: {}".format(contact_name))
                    location_str = ("Location: {}".format(location))
                    type_str = ("Job Type: {}".format(job_type))
                    charge_str = ("Customer Charge: {}".format(customer_charge))
                    description_str = ("Description: {}".format(description))
                    if language == "":
                        language = "en"
                    if language != "en":
                        title, job_str, time_str, engineer_str, manufacturer_str, model_str, machine_id_str, customer_str, contact_str, location_str, type_str, charge_str, description_str = translate(language, title, job_str, time_str, engineer_str, manufacturer_str, model_str, machine_id_str, customer_str, contact_str, location_str, type_str, charge_str, description_str)
                    try:
                        pdf = canvas.Canvas(("pdfs/report-{}.pdf").format(language))
                        pdf.setFont("Helvetica-Bold", 30, leading=None)
                        pdf.drawCentredString(300, 750, str(title))
                        pdf.setFont("Helvetica", 14, leading=None)
                        pdf.drawCentredString(300, 700, str(job_str))
                        pdf.drawCentredString(300, 670, str(time_str))
                        pdf.drawCentredString(300, 640, str(engineer_str))
                        pdf.drawCentredString(300, 610, str(manufacturer_str))
                        pdf.drawCentredString(300, 580, str(model_str))
                        pdf.drawCentredString(300, 550, str(machine_id_str))
                        pdf.drawCentredString(300, 520, str(customer_str))
                        pdf.drawCentredString(300, 490, str(contact_str))
                        pdf.drawCentredString(300, 460, str(location_str))
                        pdf.drawCentredString(300, 430, str(type_str))
                        pdf.drawCentredString(300, 400, str(charge_str))
                        pdf.drawCentredString(300, 370, str(description_str))
                        logo = "logo.jpg"
                        pdf.drawImage(logo, 0, 0, width=700, height=150)
                        pdf.showPage()
                        pdf.save()
                        submit_display(page, "PDF CREATED SUCESSFULLY", "#2aaa42")
                    except:
                        submit_display(page, "ERROR: UNABLE TO CREATE PDF", "red")
                if locked == True:
                    submit_display(page, "ERROR: PDF NOT CREATED, YOU ARE NOT LOGGED IN", "red")


            def get_entries(page, form_id, time_now, name, manufacturer, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge, description, message):
                global locked
                if locked == False:
                    file = open("data/data.csv", "a", newline="")
                    writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
                    writer.writerow([form_id, time_now, name, manufacturer, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge, description, check_attachments()])
                    file.close()
                    info = open("data/user_info.txt", "r+")
                    for row in info:
                        text = row.split(",")
                        if text[0] == username.get().lower():
                            text[2] = str(gen_id()-1)
                            text = ",".join(text)
                    info.close()
                    info = open("data/user_info.txt", "w")
                    info.write(text)
                    info.close()
                    send_email(message, '{}: Breakdown Report'.format(username.get()))
                    submit_display(page, "FORM ID {}: SUCESSFULLY SUBMITTED".format(gen_id()-2), "#2aaa42")
                if locked == True:
                    submit_display(page, "ERROR: FORM NOT SUBMITTED, YOU ARE NOT LOGGED IN", "red")

            def report_head(page):
                global report_header
                report_header = Label(page, text="REPORT", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                report_header.place(x=480, y=30, anchor="center")

            def submit_display(page, string, colour):
                global submit_text
                submit_text = Label(page, text=string, bg=check_bg(), fg=colour, font=('Segoe UI', '10'))
                submit_text.place(x=680, y=500, anchor="e")
                submit_text.after(3500, destroy_widgit, submit_text)

            def collect_time(page):
                global submit_time
                time_now = datetime.datetime.now()
                time_now = time_now.strftime("%X") + " (" + time_now.strftime("%x") + ")"
                submit_time = Label(page, text="Time: {}".format(time_now), bg="#161616", fg="white", font=('Segoe UI', '13'))
                submit_time.place(x=10, y=70)
                return time_now

            def job_no(page):
                global job_text, job_no_text
                job_text = Label(page, text="Job Number: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                job_text.place(x=10, y=30)
                job_no_text = Label(page, text=str(gen_id()-1), bg="#161616", fg="white", font=('Segoe UI', '13'))
                job_no_text.place(x=110, y=30)

            def name_input(page):
                global name_text, name_set
                name_text = Label(page, text="Engineer Name: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                name_text.place(x=10, y=110)
                name_list = ("Engineer 1", "Engineer 2", "Engineer 3", "Engineer 4", "Engineer 5")
                name = StringVar()
                name.set("Select Name")
                name_set = OptionMenu(page, name, *name_list)
                name_set.configure(text="File", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, font=('Segoe UI', '10'), activebackground="#333333", activeforeground="white", highlightthickness=0, indicatoron=1)
                name_set.place(x=140, y=113)
                return name

            def machine_info(page):

                def set_id(text):
                    machine_id.set(text)
                global manufacturer, manufacturer_set, machine_model_input, machine_model_text, machine_id_input, machine_id_text, itt_button, customer_name_input, customer_name_text, contact_name_text, contact_name_input, location_input, location_text, customer_charge_text, customer_charge_set, job_type_text, job_type_1, job_type_2, job_type_3, job_type_4, job_type_5, job_type_6, extra_upload_text, open_file_button, video_cap_button, screen_cap_button, picture_button, remove_button
                manufacturer = Label(page, text="Machine Manufacturer: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                manufacturer.place(x=10, y=150)
                manufacturer_list = ("MBF", "P.E.", "ROBINO", "TMG", "Logistics & Controls")
                manufacturer_name = StringVar()
                manufacturer_name.set("Select Manufacturer")
                manufacturer_set = OptionMenu(page, manufacturer_name, *manufacturer_list)
                manufacturer_set.configure(text="File", fg="white", bg="#474747", borderwidth=0, height = 1, width = 16, font=('Segoe UI', '10'), activebackground="#333333", activeforeground="white", highlightthickness=0, indicatoron=1)
                manufacturer_set.place(x=200, y=153)
                machine_model = StringVar()
                machine_model_input = Entry(page, textvariable=machine_model, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                machine_model_input.place(x=495, y=156)
                machine_model_text = Label(page, text="Machine Model: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                machine_model_text.place(x=360, y=150)
                machine_id = StringVar()
                machine_id_input = Entry(page, textvariable=machine_id, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                machine_id_input.place(x=815, y=156)
                itt_button = Button(page, text="Scan Image", fg="white", bg="#474747", borderwidth=0, height = 1, width = 11, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '8'), command=lambda:(set_id(image_capture())))
                itt_button.place(x=980, y=157)
                machine_id_text = Label(page, text="Machine Serial No: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                machine_id_text.place(x=660, y=150)
                customer_name = StringVar()
                customer_name_input = Entry(page, textvariable=customer_name, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                customer_name_input.place(x=150, y=196)
                customer_name_text = Label(page, text="Customer Name: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                customer_name_text.place(x=10, y=190)
                contact_name = StringVar()
                contact_name_input = Entry(page, textvariable=contact_name, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                contact_name_input.place(x=385, y=196)
                contact_name_text = Label(page, text="Contact: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                contact_name_text.place(x=310, y=190)
                location = StringVar()
                location_input = Entry(page, textvariable=location, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                location_input.place(x=630, y=196)
                location_text = Label(page, text="Location: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                location_text.place(x=550, y=190)
                customer_charge_text = Label(page, text="Customer Charge: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                customer_charge_text.place(x=790, y=190)
                customer_charge_list = ("Yes", "No")
                customer_charge = StringVar()
                customer_charge.set("Select Y/N")
                customer_charge_set = OptionMenu(page, customer_charge, *customer_charge_list)
                customer_charge_set.configure(text="File", fg="white", bg="#474747", borderwidth=0, height = 1, width = 9, font=('Segoe UI', '10'), activebackground="#333333", activeforeground="white", highlightthickness=0, indicatoron=1)
                customer_charge_set.place(x=940, y=193)
                job_type_text = Label(page, text="Job Type: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                job_type_text.place(x=10, y=230)
                job_type = StringVar()
                job_type_1 = Radiobutton(page, text="Installation", value="Installation", variable=job_type, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'), relief="flat")
                job_type_2 = Radiobutton(page, text="Overhaul", value="Overhaul", variable=job_type, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'), relief="flat")
                job_type_3 = Radiobutton(page, text="Survey", value="Survey", variable=job_type, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'), relief="flat")
                job_type_4 = Radiobutton(page, text="Maintenance", value="Maintenance", variable=job_type, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'), relief="flat")
                job_type_5 = Radiobutton(page, text="Breakdown", value="Breakdown", variable=job_type, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'), relief="flat")
                job_type_6 = Radiobutton(page, text="Other", value="Other", variable=job_type, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'), relief="flat")
                job_type_1.place(x=92, y=233)
                job_type_2.place(x=192, y=233)
                job_type_3.place(x=284, y=233)
                job_type_4.place(x=358, y=233)
                job_type_5.place(x=467, y=233)
                job_type_6.place(x=568, y=233)
                extra_upload_text = Label(page, text=" - Pictures/Video/Documentation etc.", bg="#161616", fg="white", font=('Segoe UI', '10'))
                extra_upload_text.place(x=130, y=483)
                open_file_button = Button(page, text="Upload File", fg="white", bg="#474747", borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=lambda:open_file(page))
                open_file_button.place(x=10, y=480)
                video_cap_button = Button(page, text="Record Video", fg="white", bg="#474747", borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=lambda:open_cap(page, video_cap()))
                video_cap_button.place(x=10, y=520)
                screen_cap_button = Button(page, text="Record Screen", fg="white", bg="#474747", borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=lambda:open_cap(page, screen_cap()))
                screen_cap_button.place(x=10, y=560)
                picture_button = Button(page, text="Take Picture", fg="white", bg="#474747", borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=lambda:open_cap(page, image_cap()))
                picture_button.place(x=10, y=600)
                remove_button = Button(page, text="Remove", fg="white", bg="#474747", borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=lambda:(remove(page, file_array)))
                remove_button.place(x=10, y=640)
                return manufacturer_name, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge

            def remove(page, array):
                global file_array, file_name_array, bg_canvas
                if len(file_array) > 0:
                    bg_canvas = Canvas(page, width=400, height=len(file_name_array)*20, bg=check_bg(), borderwidth=0, bd=0, highlightthickness=0, relief='flat')
                    bg_canvas.place(x=130, y=520)
                check_table(page)
                file_array = []
                file_name_array = []

            def open_cap(page, src_path):
                global file_text, attach_file, file_array
                file_array.append(src_path)
                file_name_array.append(src_path)
                append_file(page, file_array, file_name_array)

            def open_file(page):
                global file_text, attach_file, file_array
                file_text = askopenfilenames(filetypes=[("All files", "*.*")], initialdir="C:\\", title="Upload File")
                for entry in file_text:
                    entry = entry.split("(")
                    for file_name in entry:
                        file_array.append(file_name)
                        index = (file_name.rfind('/')+1)
                        file_name_array.append(file_name[index:])
                append_file(page, file_array, file_name_array)

            def append_file(page, file_array, file_name_array):
                global file_text, file_text_array
                count = 0
                for entry in file_name_array:
                    if entry != "":
                        entry = entry.split("/")
                        if len(entry) > 1:
                            entry = entry[1]
                        show_text = []
                        for char in entry:
                            if len(show_text) < 40:
                                show_text.append(char)
                        show_text = "".join(show_text)
                        if len(entry) > 40:
                            show_text = show_text + "..."
                        file_text = Label(page, text="Uploaded: " + show_text, bg=check_bg(), fg="#2aaa42", font=('Segoe UI', '8'))
                        file_text.place(x=130, y=520+count*20)
                        file_text_array.append(file_text)
                        count += 1

            def check_speech(text):
                a_text = ".\n"
                if len(text) == 0:
                    a_text = ""
                return text + a_text

            def note_input(page):
                global description_text, extra_text, description, speech_button
                description_text = Label(page, text="Description Of Work Carried Out: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                description_text.place(x=10, y=270)
                extra_text = Label(page, text=" - Issues, checks/testing done, conclusions, further actions/parts required", bg="#161616", fg="white", font=('Segoe UI', '10'))
                extra_text.place(x=270, y=273)
                description = Text(page, width = 100, height=10, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                description.place(x=10,y=310)
                speech_button = Button(page, text="Speech Entry", fg="white", bg="#474747", borderwidth=0, height = 1, width = 11, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=lambda:(description.insert(INSERT,check_speech(speech_man()))))
                speech_button.place(x=708, y=270)

                return description

            def get_message(time_now, name, manufacturer_name, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge, description):
                return 'Emergency Breakdown Report from {}\n\n\tJob Number: {}\n\tSubmission Time: {}\n\tEngineer: {}\n\tManufacturer Name: {}\n\tMachine Model: {}\n\tMachine ID: {}\n\tCustomer Name: {}\n\tContact Name: {}\n\tLocation: {}\n\tJob Type: {}\n\tCustomer Charge: {} \n\tExtra Information: {}'.format(username.get(), gen_id()-1, time_now, name, manufacturer_name, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge, description)

            def check_table(page):
                global locked
                if locked == False:
                    display_table(page)

            def submit_setup(page, time_now, name, manufacturer_name, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge, description):
                global submit_button, pdf_button, lang_text, lang_entry
                submit_button = Button(page, text="Submit", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '15'), command=lambda:(get_entries(page, gen_id()-1, time_now, name.get(), manufacturer_name.get(), machine_model.get(), machine_id.get(), customer_name.get(), contact_name.get(), location.get(), job_type.get(), customer_charge.get(), description.get("1.0","end-1c"), get_message(time_now, name.get(), manufacturer_name.get(), machine_model.get(), machine_id.get(), customer_name.get(), contact_name.get(), location.get(), job_type.get(), customer_charge.get(), description.get("1.0","end-1c"))), check_table(page)))
                submit_button.place(x=697, y=480)
                pdf_button = Button(page, text="Create PDF", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '15'), command=lambda:(create_pdf(page, gen_id()-1, time_now, name.get(), manufacturer_name.get(), machine_model.get(), machine_id.get(), customer_name.get(), contact_name.get(), location.get(), job_type.get(), customer_charge.get(), description.get("1.0","end-1c"), lang_input.get())))
                pdf_button.place(x=697, y=530)
                lang_text = Label(page, text="PDF Language: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                lang_text.place(x=697, y=580)
                lang_input = StringVar()
                lang_entry = Entry(page, textvariable=lang_input, width=5, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                lang_entry.place(x=820, y=586)

            def login_head(page):
                global login_header
                login_header = Label(page, text="LOGIN", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                login_header.place(x=1540, y=30, anchor="center")

            def update_email(page, recieving_email, sending_email, email_pass):
                global update_text
                with open("data/user_info.txt", "r") as file:
                    data = file.readlines()
                    to_write = []
                    for line in data:
                        line = line.split(",")
                        if line[0] == username.get().lower():
                            line[3] = recieving_email
                            line[4] = sending_email
                            line[5] = email_pass
                        line = line[0] + "," + line[1] + "," + line[2] + "," + line[3] + "," + line[4] + "," + line[5]
                        to_write.append(line)
                with open("data/user_info.txt", "w") as file:
                    for line in to_write:
                        file.write(line)
                update_text = Label(page, text="Email Updated Sucessfully!", bg=check_bg(), fg="#2aaa42", font=('Segoe UI', '10'), width=23)
                update_text.place(x=1645, y=377, anchor="e")
                update_text.after(3000, destroy_widgit, update_text)

            def display_table(page):
                global prevous_text, elements, table_canvas, table_error_text
                elements = []
                table_canvas = Canvas(page, width=800, height=400, bg=check_bg(), borderwidth=0, bd=0, highlightthickness=0, relief='ridge')
                table_canvas.place(x=10, y=790)
                prevous_text = Label(page, text="LATEST REPORTS", bg=check_bg(), fg=check_fg(), font=('Segoe UI', '18', 'bold'))
                prevous_text.place(x=480, y=790, anchor="center")
                with open('data/data.csv') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    row_no = 0
                    for table_row in csv.reader(csv_file):
                        row_no += 1
                if row_no >= 2:
                    with open('data/data.csv') as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        row_no = 0
                        active_row = 0
                        for table_row in csv.reader(csv_file):
                            font = ('Segoe UI', '10')
                            if row_no == 0:
                                font = ('Segoe UI', '10', 'bold')
                            if row_no + 7 > gen_id()-1 or row_no == 0:
                                for column in range(len(table_row)):
                                    if column == 11:
                                        continue
                                    elif column == 0:
                                        element = Label(page, text=table_row[column], bg=check_bg(), fg=check_fg(), font=font, width=20, anchor="w")
                                        element.place(x=10+column*110, y=830+active_row*30, anchor="w")
                                    elif column == 1:
                                        element = Label(page, text=table_row[column], bg=check_bg(), fg=check_fg(), font=font, width=20, anchor="w")
                                        element.place(x=(column*100)-10, y=830+active_row*30, anchor="w")
                                    elif column == 5:
                                        element = Label(page, text=table_row[column], bg=check_bg(), fg=check_fg(), font=font, width=20, anchor="w")
                                        element.place(x=70+column*110, y=830+active_row*30, anchor="w")
                                    elif column == 4:
                                        element = Label(page, text=table_row[column], bg=check_bg(), fg=check_fg(), font=font, width=20, anchor="w")
                                        element.place(x=70+column*110, y=830+active_row*30, anchor="w")
                                    elif column == 12:
                                        element = Label(page, text=table_row[column], bg=check_bg(), fg=check_fg(), font=font, width=20, anchor="w")
                                        element.place(x=column*110, y=830+active_row*30, anchor="w")
                                    else:
                                        element = Label(page, text=table_row[column], bg=check_bg(), fg=check_fg(), font=font, width=45, anchor="w")
                                        element.place(x=55+column*110, y=830+active_row*30, anchor="w")
                                    elements.append(element)
                                active_row += 1
                            row_no += 1
                else:
                    table_error_text = Label(page, text="No Previous Reports To Be Displayed", bg=check_bg(), fg="red", font=('Segoe UI', '13'))
                    table_error_text.place(x=480, y=820, anchor="center")

            def create_email():
                global subject_text, email_message_text, email_subject_entry, email_back_button, email_message, email_speech_button, send_email_button
                email_button.destroy()
                sms_button.destroy()
                email_subject = StringVar()
                subject_text = Label(page, text="Subject: ", bg=check_bg(), fg=check_fg(), font=('Segoe UI', '13'))
                subject_text.place(x=1395, y=610, anchor="e")
                email_message_text = Label(page, text="Message: ", bg=check_bg(), fg=check_fg(), font=('Segoe UI', '13'))
                email_message_text.place(x=1395, y=640, anchor="e")
                email_subject_entry = Entry(page, textvariable=email_subject, width=53, bg=check_panels(), fg=check_fg(), highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                email_subject_entry.place(x=1400, y=600)
                email_back_button = Button(page, text="Back", fg=check_fg(), bg=check_buttons(), borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:(subject_text.destroy(), email_message_text.destroy(), email_subject_entry.destroy(), send_email_button.destroy(), email_back_button.destroy(), email_message.destroy(), email_speech_button.destroy(), message_panel(page)))
                email_back_button.place(x=1487, y=690)
                email_message = Text(page, width = 40, height=4, bg=check_panels(), fg=check_fg(), highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                email_message.place(x=1400,y=620)
                email_speech_button = Button(page, text="Speech Entry", fg=check_fg(), bg=check_buttons(), borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:(email_message.insert(INSERT,check_speech(speech_man()))))
                email_speech_button.place(x=1567, y=690)
                send_email_button = Button(page, text="Send Email", fg=check_fg(), bg=check_buttons(), borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:(send_email(email_message.get('1.0', END), email_subject.get(), True)))
                send_email_button.place(x=1647, y=690)

            def message_panel(page):
                global email_button, sms_button, message_header
                message_header = Label(page, text="COMMUNICATE WITH HEAD OFFICE", bg=check_bg(), fg=check_fg(), font=('Segoe UI', '18', 'bold'))
                message_header.place(x=1540, y=580, anchor="center")
                email_button = Button(page, text="Email", fg=check_fg(), bg=check_buttons(), borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=lambda:create_email())
                email_button.place(x=1460, y=600)
                sms_button = Button(page, text="Text", fg=check_fg(), bg=check_buttons(), borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white",  font=('Segoe UI', '12'), command=lambda:create_sms())
                sms_button.place(x=1570, y=600)

            def create_sms():
                global sms_message_text, sms_message, sms_back_button, sms_speech_button, send_sms_button
                email_button.destroy()
                sms_button.destroy()
                sms_message_text = Label(page, text="Message: ", bg=check_bg(), fg=check_fg(), font=('Segoe UI', '13'))
                sms_message_text.place(x=1395, y=610, anchor="e")
                sms_message = Text(page, width = 40, height=4, bg=check_panels(), fg=check_fg(), highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                sms_message.place(x=1400,y=600)
                sms_back_button = Button(page, text="Back", fg=check_fg(), bg=check_buttons(), borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white", command=lambda:(sms_message_text.destroy(), sms_message.destroy(), sms_speech_button.destroy(), send_sms_button.destroy(), sms_back_button.destroy(), message_panel(page)))
                sms_back_button.place(x=1447, y=670)
                sms_speech_button = Button(page, text="Speech Entry", fg=check_fg(), bg=check_buttons(), borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white", command=lambda:(sms_message.insert(INSERT,check_speech(speech_man()))))
                sms_speech_button.place(x=1540, y=670)
                send_sms_button = Button(page, text="Send Message", fg=check_fg(), bg=check_buttons(), borderwidth=0, height = 1, width = 12, activebackground="#333333", activeforeground="white", command=lambda:(send_sms(sms_message.get('1.0', END))))
                send_sms_button.place(x=1633, y=670)

            def send_sms(msg):
                global username
                account_sid = ""
                auth_token = ""
                receiving_num = ""
                sending_num = "+447480781230"
                msg = "Message from {}:\n".format(username.get()) + msg
                client = Client(account_sid, auth_token)
                message = client.messages.create(to=receiving_num, from_=sending_num, body=msg)

            def login_panel(page, login_time):
                global recieving_email, sending_email, email_pass, ip_input, port_input
                global stats_header, latest_login, forms_sent, r_email_text, s_email_text, r_email_entry, s_email_entry, pass_text, email_password, set_email, live_stream_header, ip_text, ip_entry, port_entry, live_stream_button
                stats_header = Label(page, text="STATS/SETTINGS", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                stats_header.place(x=1540, y=170, anchor="center")
                latest_login = Label(page, text="Last Login: " + str(login_time), bg="#161616", fg="white", font=('Segoe UI', '13'))
                latest_login.place(x=1540, y=220, anchor="center")
                forms_sent = Label(page, text="Total Forms Sent: " + str(gen_id()-2), bg="#161616", fg="white", font=('Segoe UI', '13'))
                forms_sent.place(x=1540, y=250, anchor="center")
                recieving_email = StringVar()
                sending_email = StringVar()
                email_pass = StringVar()
                info = open("data/user_info.txt", "r+")
                for row in info:
                    text = row.split(",")
                    if text[0] == username.get().lower():
                        recieving_email.set(text[3])
                        sending_email.set(text[4])
                        email_pass.set(text[5])
                info.close()
                r_email_text = Label(page, text="Receiving Email: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                r_email_text.place(x=1480, y=290, anchor="e")
                s_email_text = Label(page, text="Your Email: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                s_email_text.place(x=1480, y=320, anchor="e")
                r_email_entry = Entry(page, textvariable=recieving_email, width=40, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                r_email_entry.place(x=1480, y=283)
                s_email_entry = Entry(page, textvariable=sending_email, width=40, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                s_email_entry.place(x=1480, y=313)
                pass_text = Label(page, text="Email Password: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                pass_text.place(x=1480, y=350, anchor="e")
                email_password = Entry(page, textvariable=email_pass, width=40, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb", show="•")
                email_password.place(x=1480, y=343)
                set_email = Button(page, text="Set Email", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:update_email(page, recieving_email.get(), sending_email.get(), email_pass.get()))
                set_email.place(x=1647, y=368)
                ip_input = StringVar()
                port_input = StringVar()
                live_stream_header = Label(page, text="LIVE STREAM", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                live_stream_header.place(x=1540, y=450, anchor="center")
                ip_text = Label(page, text="Host IP and Port: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                ip_text.place(x=1490, y=500, anchor="e")
                ip_entry = Entry(page, textvariable=ip_input, width=15, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                ip_entry.place(x=1490, y=493)
                port_entry = Entry(page, textvariable=port_input, width=5, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                port_entry.place(x=1590, y=493)
                live_stream_button = Button(page, text="Live Stream", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:live_stream(page, ip_entry.get(), port_entry.get()))
                live_stream_button.place(x=1630, y=503, anchor="w")
                display_table(page)

            def hash(password):
                hash_object = hashlib.sha256(password.encode())
                hex_dig = hash_object.hexdigest()
                return hex_dig

            def request_timeout(time_now):
                global to_wait, time_out
                time_out = 300  #In seconds
                if os.path.isfile("data/logins.txt"):
                    file = open("data/logins.txt","r")
                    for attempt in file:
                        to_wait = round(((float(attempt) + time_out) - time_now),5)
                        if time_now > float(attempt) + time_out:
                            return True
                        else:
                            return False
                    file.close()
                else:
                    return True

            def gen_data_file(username):
                if os.path.isfile("data/user_info.txt") == False:
                    info = open("data/user_info.txt", "w")
                    info.write(username + "," + "First Time Logging In" + "," + "0" + "," + "" + "," + "" + "," + "")
                    info.close()
                else:
                    info = open("data/user_info.txt", "a")
                    info.write("\n" + username + "," + "First Time Logging In" + "," + "0" + "," + "" + "," + "" + "," + "")
                    info.close()

            def username_file_check(username):
                in_file = False
                if os.path.isfile("data/user_info.txt") == True:
                    with open("data/user_info.txt", "r") as file:
                        data = file.readlines()
                        for line in data:
                            line = line.split(",")
                            if username == line[0]:
                                in_file = True
                return in_file

            def sign_in(page, username, password, username_text, password_text, username_input, password_input, login_button):
                global tries_text, welcome_text, about_text, locked
                nonlocal tries
                if request_timeout(time.time()) == True and tries < 1:
                    tries = 3
                if request_timeout(time.time()) == True:
                    try:
                        file = urllib.request.urlopen("http://0.0.0.0:3402/static/credentials.txt")
                    except:
                        tries_text = Label(page, text="ERROR: cannot contact server", bg=check_bg(), fg="red", font=('Segoe UI', '10'))
                        tries_text.place(x=1648, y=183, anchor="e")
                        tries_text.after(2000, destroy_widgit, tries_text)
                    try:
                        if locked == True:
                            for line in file:
                                line = line.decode("utf-8")
                                values = line.split(",")
                                for value in values:
                                    value = value.encode("utf-8")
                                if pbkdf2_sha256.verify(password, values[1][:87]) and pbkdf2_sha256.verify(username, values[0]):
                                    locked = False
                                    destroy_widgit(username_text)
                                    destroy_widgit(username_input)
                                    destroy_widgit(password_text)
                                    destroy_widgit(password_input)
                                    destroy_widgit(login_button)
                            tries -= 1
                        file.close()
                        if locked == True:
                            tries_text = Label(page, text="Incorrect Username and Password: {} Tries Left".format(tries), bg=check_bg(), fg="red", font=('Segoe UI', '10'))
                            tries_text.place(x=1648, y=183, anchor="e")
                            tries_text.after(2000, destroy_widgit, tries_text)
                        if locked == False:
                            last_login = ""
                            if username_file_check(username) == False:
                                gen_data_file(username)
                            with open("data/user_info.txt", "r") as file:
                                data = file.readlines()
                                to_write = []
                                for line in data:
                                    line = line.split(",")
                                    if line[0] == username:
                                        last_login = line[1]
                                        line[1] = str(datetime.datetime.now())
                                    line = line[0] + "," + line[1] + "," + line[2] + "," + line[3] + "," + line[4] + "," + line[5]
                                    to_write.append(line)
                            with open("data/user_info.txt", "w") as file:
                                for line in to_write:
                                    file.write(line)
                            welcome_text = Label(page, text="Welcome {}".format(username.capitalize()), bg="#161616", fg="white", font=('Segoe UI', '20'))
                            about_text = Label(page, text="To The Automatic Reporting System", bg="#161616", fg="white", font=('Segoe UI', '15'))
                            welcome_text.place(x=1540, y=90, anchor="center")
                            about_text.place(x=1540, y=120, anchor="center")
                            login_panel(page, last_login)
                            message_panel(page)
                            send_email("Security Alert: \n\n\tA sucessfull login attempt occured at {}".format(datetime.datetime.now()), "Security Alert: Sucessfull Login Attempt", True)
                            theme_update(str(theme_slider.get()))
                    except:
                        print("Error: cannot log in")
                    if locked == True and tries < 1:
                        file = open("data/logins.txt","w+")
                        file.write(str(time.time()))
                        file.close()
                if request_timeout(time.time()) == False:
                    tries_text = Label(page, text="Error: Out of Attempts, wait {:.2f}s".format(to_wait), bg=check_bg(), fg="red", font=('Segoe UI', '10'), width=60)
                    tries_text.place(x=1753, y=183, anchor="e")
                    tries_text.after(2000, destroy_widgit, tries_text)

            def login(page):
                global username, username_text, password_text, username_input, password_input, login_button
                username_text = Label(page, text="Username: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                username_text.place(x=1490, y=83, anchor='e')
                password_text = Label(page, text="Password: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                password_text.place(x=1490, y=113, anchor='e')
                username = StringVar()
                password = StringVar()
                username_input = Entry(page, textvariable=username, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                username_input.place(x=1490, y=76)
                password_input = Entry(page, textvariable=password, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb", show="•")
                password_input.place(x=1490, y=106)
                login_button = Button(page, text="Login", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:sign_in(page, username.get().lower(), password.get(), username_text, password_text, username_input, password_input, login_button), font=('Segoe UI', '12'))
                login_button.place(x=1547, y=136)

            def check_csv():
                if os.path.isfile("data/data.csv") == False:
                    file = open("data/data.csv", "a", newline="")
                    writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
                    writer.writerow(["Report ID", "Time/Date", "Engineer", "Manufacturer", "Machine Model", "Machine ID", "Customer", "Contact", "Location", "Job Type", "Customer Charge", "Description", "Attachments"])
                    file.close()

            def theme_switch(page):
                global theme_slider, theme_text
                theme_text = Label(page, text="Dark/Light Theme: ", bg="#161616", fg="white", font=('Segoe UI', '11', 'bold'))
                theme_text.place(x=1850, y=1018, anchor='e')
                theme_slider = Scale(page, orient=HORIZONTAL, length=50, width=20, sliderlength=20, from_=0, to=1, bg="#474747", bd=0, borderwidth=0, activebackground="#333333", font=('Segoe UI', '12'), highlightthickness=0, sliderrelief="flat", showvalue=0, troughcolor="#333333", command=theme_update)
                theme_slider.place(x=1850, y=1010)

            def theme_update(is_theme):
                dark = {"fg": "#ffffff", "buttons": "#474747", "panels": "#333333", "bg": "#161616", "radio_bg": "#000000", "highlight": "#dbdbdb", "entry": "#474747", "select": "#474747"}
                light = {"fg": "#000000", "buttons": "#1366C4", "panels": "#CCCCCC", "bg": "#E9E9E9", "radio_bg": "#1366C4", "highlight": "#848484", "entry": "#CCCCCC", "select": "#1366C4"}
                if is_theme == "1":
                    time_canvas.config(bg=light["buttons"])
                    time_text.config(bg=light["buttons"], fg=light["fg"])
                    uk_text.config(bg=light["buttons"], fg=light["fg"])
                    uk_work.config(bg=light["buttons"], fg=light["fg"])
                    italy_text.config(bg=light["buttons"], fg=light["fg"])
                    italy_work.config(bg=light["buttons"], fg=light["fg"])
                    clear_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    error_header.config(bg=light["bg"], fg=light["fg"])
                    error_canvas.config(bg=light["panels"])
                    for error_text in error_text_list:
                        error_text.config(bg=light["panels"], fg=light["fg"])
                    theme_slider.config(bg=light["buttons"], activebackground=light["buttons"], troughcolor=light["panels"])
                    theme_text.config(bg=light["bg"], fg=light["fg"])
                    page.config(bg=light["bg"])
                    bar.config(bg=light["panels"])
                    info1.config(bg=light["panels"], fg=light["fg"])
                    info2.config(bg=light["panels"], fg=light["fg"])
                    info3.config(bg=light["panels"], fg=light["fg"])
                    login_header.config(bg=light["bg"], fg=light["fg"])
                    submit_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    pdf_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    lang_text.config(bg=light["bg"], fg=light["fg"])
                    lang_entry.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                    description_text.config(bg=light["bg"], fg=light["fg"])
                    extra_text.config(bg=light["bg"], fg=light["fg"])
                    description.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                    speech_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    manufacturer.config(bg=light["bg"], fg=light["fg"])
                    manufacturer_set.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"], activebackground=light["select"])
                    machine_model_text.config(bg=light["bg"], fg=light["fg"])
                    machine_model_input.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                    machine_id_text.config(bg=light["bg"], fg=light["fg"])
                    machine_id_input.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                    customer_name_text.config(bg=light["bg"], fg=light["fg"])
                    customer_name_input.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                    contact_name_text.config(bg=light["bg"], fg=light["fg"])
                    contact_name_input.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                    location_text.config(bg=light["bg"], fg=light["fg"])
                    location_input.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                    customer_charge_text.config(bg=light["bg"], fg=light["fg"])
                    customer_charge_set.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"], activebackground=light["select"])
                    job_type_text.config(bg=light["bg"], fg=light["fg"])
                    job_type_1.config(bg=light["bg"], fg=light["fg"], activebackground=light["panels"], activeforeground=light["radio_bg"], selectcolor=light["panels"])
                    job_type_2.config(bg=light["bg"], fg=light["fg"], activebackground=light["panels"], activeforeground=light["radio_bg"], selectcolor=light["panels"])
                    job_type_3.config(bg=light["bg"], fg=light["fg"], activebackground=light["panels"], activeforeground=light["radio_bg"], selectcolor=light["panels"])
                    job_type_4.config(bg=light["bg"], fg=light["fg"], activebackground=light["panels"], activeforeground=light["radio_bg"], selectcolor=light["panels"])
                    job_type_5.config(bg=light["bg"], fg=light["fg"], activebackground=light["panels"], activeforeground=light["radio_bg"], selectcolor=light["panels"])
                    job_type_6.config(bg=light["bg"], fg=light["fg"], activebackground=light["panels"], activeforeground=light["radio_bg"], selectcolor=light["panels"])
                    extra_upload_text.config(bg=light["bg"], fg=light["fg"])
                    open_file_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    video_cap_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    screen_cap_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    picture_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    remove_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    itt_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    submit_time.config(bg=light["bg"], fg=light["fg"])
                    job_text.config(bg=light["bg"], fg=light["fg"])
                    job_no_text.config(bg=light["bg"], fg=light["fg"])
                    name_text.config(bg=light["bg"], fg=light["fg"])
                    name_set.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"], activebackground=light["select"])
                    report_header.config(bg=light["bg"], fg=light["fg"])
                    nav.config(bg=light["panels"])
                    title.config(bg=light["panels"], fg=light["fg"])
                    exit.config(fg=light["fg"], bg=light["panels"], activebackground=light["panels"], activeforeground=light["fg"])
                    for text in file_text_array:
                        text.config(bg=light["bg"])
                    try:
                        tries_text.config(bg=light["bg"])
                    except:
                        pass
                    try:
                        update_text.config(bg=light["bg"])
                    except:
                        pass
                    try:
                        ls_error_text.config(bg=light["bg"])
                    except:
                        pass
                    try:
                        submit_text.config(bg=light["bg"])
                    except:
                        pass
                    try:
                        file_text.config(bg=light["bg"])
                    except:
                        pass
                    try:
                        bg_canvas.config(bg=light["bg"])
                    except:
                        pass
                    if locked == True:
                        username_text.config(bg=light["bg"], fg=light["fg"])
                        password_text.config(bg=light["bg"], fg=light["fg"])
                        username_input.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        password_input.config(bg=light["entry"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        login_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                    if locked == False:
                        welcome_text.config(bg=light["bg"], fg=light["fg"])
                        about_text.config(bg=light["bg"],  fg=light["fg"])
                        stats_header.config(bg=light["bg"], fg=light["fg"])
                        latest_login.config(bg=light["bg"], fg=light["fg"])
                        forms_sent.config(bg=light["bg"], fg=light["fg"])
                        r_email_text.config(bg=light["bg"], fg=light["fg"])
                        s_email_text.config(bg=light["bg"], fg=light["fg"])
                        pass_text.config(bg=light["bg"], fg=light["fg"])
                        r_email_entry.config(bg=light["panels"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        s_email_entry.config(bg=light["panels"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        email_password.config(bg=light["panels"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        set_email.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        live_stream_header.config(bg=light["bg"], fg=light["fg"])
                        ip_text.config(bg=light["bg"],  fg=light["fg"])
                        ip_entry.config(bg=light["panels"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        port_entry.config(bg=light["panels"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        live_stream_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        prevous_text.config(bg=light["bg"], fg=light["fg"])
                        for element in elements:
                            element.config(bg=light["bg"], fg=light["fg"])
                        table_canvas.config(bg=light["bg"])
                        try:
                            table_error_text.config(bg=light["bg"], fg=light["fg"])
                        except:
                            pass
                        try:
                            subject_text.config(bg=light["bg"],  fg=light["fg"])
                        except:
                            pass
                        try:
                            email_message_text.config(bg=light["bg"],  fg=light["fg"])
                        except:
                            pass
                        try:
                            message_header.config(bg=light["bg"],  fg=light["fg"])
                        except:
                            pass
                        try:
                            sms_message_text.config(bg=light["bg"],  fg=light["fg"])
                        except:
                            pass
                        try:
                            email_back_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        except:
                            pass
                        try:
                            email_speech_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        except:
                            pass
                        try:
                            send_email_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        except:
                            pass
                        try:
                            email_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        except:
                            pass
                        try:
                            sms_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        except:
                            pass
                        try:
                            sms_back_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        except:
                            pass
                        try:
                            sms_speech_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        except:
                            pass
                        try:
                            send_sms_button.config(fg=light["fg"], bg=light["buttons"], activebackground=light["panels"], activeforeground=light["fg"])
                        except:
                            pass
                        try:
                            email_subject_entry.config(bg=light["panels"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        except:
                            pass
                        try:
                            email_message.config(bg=light["panels"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        except:
                            pass
                        try:
                            sms_message.config(bg=light["panels"], fg=light["fg"], highlightcolor=light["bg"], highlightbackground = light["highlight"])
                        except:
                            pass

                if is_theme == "0":
                    time_canvas.config(bg=dark["buttons"])
                    time_text.config(bg=dark["buttons"], fg=dark["fg"])
                    uk_text.config(bg=dark["buttons"], fg=dark["fg"])
                    uk_work.config(bg=dark["buttons"], fg=dark["fg"])
                    italy_text.config(bg=dark["buttons"], fg=dark["fg"])
                    italy_work.config(bg=dark["buttons"], fg=dark["fg"])
                    clear_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    error_header.config(bg=dark["bg"], fg=dark["fg"])
                    error_canvas.config(bg=dark["panels"])
                    for error_text in error_text_list:
                        error_text.config(bg=dark["panels"], fg=dark["fg"])
                    theme_slider.config(bg=dark["buttons"], activebackground=dark["buttons"], troughcolor=dark["panels"])
                    theme_text.config(bg=dark["bg"], fg=dark["fg"])
                    page.config(bg=dark["bg"])
                    bar.config(bg=dark["panels"])
                    info1.config(bg=dark["panels"], fg=dark["fg"])
                    info2.config(bg=dark["panels"], fg=dark["fg"])
                    info3.config(bg=dark["panels"], fg=dark["fg"])
                    login_header.config(bg=dark["bg"], fg=dark["fg"])
                    submit_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    pdf_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    lang_text.config(bg=dark["bg"], fg=dark["fg"])
                    lang_entry.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                    description_text.config(bg=dark["bg"], fg=dark["fg"])
                    extra_text.config(bg=dark["bg"], fg=dark["fg"])
                    description.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                    speech_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    manufacturer.config(bg=dark["bg"], fg=dark["fg"])
                    manufacturer_set.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"], activebackground=dark["select"])
                    machine_model_text.config(bg=dark["bg"], fg=dark["fg"])
                    machine_model_input.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                    machine_id_text.config(bg=dark["bg"], fg=dark["fg"])
                    machine_id_input.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                    customer_name_text.config(bg=dark["bg"], fg=dark["fg"])
                    customer_name_input.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                    contact_name_text.config(bg=dark["bg"], fg=dark["fg"])
                    contact_name_input.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                    location_text.config(bg=dark["bg"], fg=dark["fg"])
                    location_input.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                    customer_charge_text.config(bg=dark["bg"], fg=dark["fg"])
                    customer_charge_set.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"], activebackground=dark["select"])
                    job_type_text.config(bg=dark["bg"], fg=dark["fg"])
                    job_type_1.config(bg=dark["bg"], fg=dark["fg"], activebackground=dark["panels"], activeforeground=dark["radio_bg"], selectcolor=dark["panels"])
                    job_type_2.config(bg=dark["bg"], fg=dark["fg"], activebackground=dark["panels"], activeforeground=dark["radio_bg"], selectcolor=dark["panels"])
                    job_type_3.config(bg=dark["bg"], fg=dark["fg"], activebackground=dark["panels"], activeforeground=dark["radio_bg"], selectcolor=dark["panels"])
                    job_type_4.config(bg=dark["bg"], fg=dark["fg"], activebackground=dark["panels"], activeforeground=dark["radio_bg"], selectcolor=dark["panels"])
                    job_type_5.config(bg=dark["bg"], fg=dark["fg"], activebackground=dark["panels"], activeforeground=dark["radio_bg"], selectcolor=dark["panels"])
                    job_type_6.config(bg=dark["bg"], fg=dark["fg"], activebackground=dark["panels"], activeforeground=dark["radio_bg"], selectcolor=dark["panels"])
                    extra_upload_text.config(bg=dark["bg"], fg=dark["fg"])
                    open_file_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    video_cap_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    screen_cap_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    picture_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    remove_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    itt_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    submit_time.config(bg=dark["bg"], fg=dark["fg"])
                    job_text.config(bg=dark["bg"], fg=dark["fg"])
                    job_no_text.config(bg=dark["bg"], fg=dark["fg"])
                    name_text.config(bg=dark["bg"], fg=dark["fg"])
                    name_set.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"], activebackground=dark["select"])
                    report_header.config(bg=dark["bg"], fg=dark["fg"])
                    nav.config(bg=dark["panels"])
                    title.config(bg=dark["panels"], fg=dark["fg"])
                    exit.config(fg=dark["fg"], bg=dark["panels"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    for text in file_text_array:
                        text.config(bg=dark["bg"])
                    try:
                        tries_text.config(bg=dark["bg"])
                    except:
                        pass
                    try:
                        update_text.config(bg=dark["bg"])
                    except:
                        pass
                    try:
                        ls_error_text.config(bg=dark["bg"])
                    except:
                        pass
                    try:
                        submit_text.config(bg=dark["bg"])
                    except:
                        pass
                    try:
                        file_text.config(bg=dark["bg"])
                    except:
                        pass
                    try:
                        bg_canvas.config(bg=dark["bg"])
                    except:
                        pass
                    if locked == True:
                        username_text.config(bg=dark["bg"], fg=dark["fg"])
                        password_text.config(bg=dark["bg"], fg=dark["fg"])
                        username_input.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        password_input.config(bg=dark["entry"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        login_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                    if locked == False:
                        welcome_text.config(bg=dark["bg"], fg=dark["fg"])
                        about_text.config(bg=dark["bg"],  fg=dark["fg"])
                        stats_header.config(bg=dark["bg"], fg=dark["fg"])
                        latest_login.config(bg=dark["bg"], fg=dark["fg"])
                        forms_sent.config(bg=dark["bg"], fg=dark["fg"])
                        r_email_text.config(bg=dark["bg"], fg=dark["fg"])
                        s_email_text.config(bg=dark["bg"], fg=dark["fg"])
                        pass_text.config(bg=dark["bg"], fg=dark["fg"])
                        r_email_entry.config(bg=dark["buttons"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        s_email_entry.config(bg=dark["buttons"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        email_password.config(bg=dark["buttons"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        set_email.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        live_stream_header.config(bg=dark["bg"], fg=dark["fg"])
                        ip_text.config(bg=dark["bg"],  fg=dark["fg"])
                        ip_entry.config(bg=dark["buttons"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        port_entry.config(bg=dark["buttons"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        live_stream_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        prevous_text.config(bg=dark["bg"], fg=dark["fg"])
                        for element in elements:
                            element.config(bg=dark["bg"], fg=dark["fg"])
                        table_canvas.config(bg=dark["bg"])
                        try:
                            table_error_text.config(bg=dark["bg"], fg=dark["fg"])
                        except:
                            pass
                        try:
                            subject_text.config(bg=dark["bg"],  fg=dark["fg"])
                        except:
                            pass
                        try:
                            email_message_text.config(bg=dark["bg"],  fg=dark["fg"])
                        except:
                            pass
                        try:
                            message_header.config(bg=dark["bg"],  fg=dark["fg"])
                        except:
                            pass
                        try:
                            sms_message_text.config(bg=dark["bg"],  fg=dark["fg"])
                        except:
                            pass
                        try:
                            email_back_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        except:
                            pass
                        try:
                            email_speech_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        except:
                            pass
                        try:
                            send_email_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        except:
                            pass
                        try:
                            email_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        except:
                            pass
                        try:
                            sms_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        except:
                            pass
                        try:
                            sms_back_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        except:
                            pass
                        try:
                            sms_speech_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        except:
                            pass
                        try:
                            send_sms_button.config(fg=dark["fg"], bg=dark["buttons"], activebackground=dark["panels"], activeforeground=dark["fg"])
                        except:
                            pass
                        try:
                            email_subject_entry.config(bg=dark["buttons"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        except:
                            pass
                        try:
                            email_message.config(bg=dark["buttons"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        except:
                            pass
                        try:
                            sms_message.config(bg=dark["buttons"], fg=dark["fg"], highlightcolor=dark["bg"], highlightbackground = dark["highlight"])
                        except:
                            pass

            def setup():
                global page
                page = Frame(root, bg="#161616", width = 1920, height = 1080)
                page.place(x=0, y=15, anchor="nw")
                check_csv()
                report_head(page)
                login_head(page)
                login(page)
                theme_switch(page)
                time_now = collect_time(page)
                job_no(page)
                error_system(page)
                name = name_input(page)
                Thread(target = display_time).start()
                manufacturer_name, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge = machine_info(page)
                description = note_input(page)
                submit_setup(page, time_now, name, manufacturer_name, machine_model, machine_id, customer_name, contact_name, location, job_type, customer_charge, description)

            setup()

        def about(root):
            global bar, info1, info2, info3
            bar = Frame(root, bg="#333333")
            bar.place(x=960, y=1080, anchor="s", width=1920)
            info1 = Label(bar, text="Version 1.7.0", bg="#333333", fg="white")
            info2 = Label(bar, text="Developed by PHS Students: Fraser, Adam, Finlay, Lucas, Peter and Sam", bg="#333333", fg="white")
            info3 = Label(bar, text="Partners: Evolution BPS", bg="#333333", fg="white")
            info1.grid(row=0, column=0, padx=10)
            info2.grid(row=0, column=1, padx=10)
            info3.grid(row=0, column=2, padx=10)

        main(root)
        navbar(root)
        about(root)

    gen_folders()
    root = initalise_app()
    root_screen(root)
    x_pos = int(root.winfo_screenwidth()/2)-800
    y_pos = int(root.winfo_screenheight()/2)-450
    root.attributes("-fullscreen", True)
    root.resizable(0, 0)
    root.mainloop()

file_name_array = []
file_text_array = []
file_array = []
error_list  = []
error_text_list = []
locked = True
app()
