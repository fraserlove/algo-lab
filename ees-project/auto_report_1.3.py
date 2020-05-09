"""
EES Project Automatic Error Report Software - Development Version 1.3
Developed by Fraser Love on 01/02/19
Dependencies: Tkinter

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
"""

from tkinter import *
from flask import Flask
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from passlib.hash import pbkdf2_sha256
import datetime, csv, os, time, hashlib, uuid, smtplib, threading, urllib, pysftp

def app():
    def initalise_app():
        root = Tk()
        root.overrideredirect(1)
        return root

    def close_window():
        root.destroy()

    def root_screen(root):
        tries = 3
        locked = True
        def background(root):
            background = Frame(root, bg="#212121", width = 1920, height = 1080)
            title = Label(background, text="AUTO REPORT", bg="#212121", fg="white", font=('Segoe UI', '18', 'bold'))
            background.place(x=1920/2, y=1080/2, anchor="center")
            title.place(x=10, y=40, anchor="w")

        def navbar(root):
            nav = Frame(root, bg="#474747")
            title = Label(nav, text="Automatic Report Software - Development Version", bg="#474747", fg="white")
            button1 = Button(nav, text="File", fg="white", bg="#474747", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white")
            button2 = Button(nav, text="Open", fg="white", bg="#474747", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white")
            button3 = Button(nav, text="Help", fg="white", bg="#474747", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white")
            button4 = Button(nav, text="Exit", fg="white", bg="#474747", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white", command=close_window)
            nav.place(x=0, y=0, anchor="nw")
            button1.grid(row=0, column=0)
            button2.grid(row=0, column=1)
            button3.grid(row=0, column=2)
            button4.grid(row=0, column=3, padx=1436, sticky="E")
            title.place(x=800, y=10, anchor="center")

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

            def send_email(message, subject):
                email = sending_email.get()
                password = email_pass.get()
                send_to_email = recieving_email.get()

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                text = msg.as_string()
                server.sendmail(email, send_to_email, text)
                server.quit()

            def get_entries(page, form_id, time_now, name, issue, enteredText, message):
                if locked == False:
                    file = open("data/data.csv", "a", newline="")
                    writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
                    writer.writerow([form_id, username.get(), time_now, name, issue, enteredText])
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
                    submit_display(page, "FORM ID {}: SUCESSFULLY SUBMITTED".format(gen_id()-1), "#42f456")
                    send_email(message, '{}: Breakdown Report'.format(username.get()))
                    print("Appended: {} {} {} {}".format(form_id, username.get(), time_now, name, issue, enteredText))
                if locked == True:
                    submit_display(page, "ERROR: FORM NOT SUBMITTED, YOU ARE NOT LOGGED IN", "red")


            def submit_display(page, string, colour):
                submit_text = Label(page, text=string, bg="#161616", fg=colour, font=('Segoe UI', '10'))
                submit_text.place(x=790, y=550, anchor="e")
                submit_text.after(3500, destroy_widgit, submit_text)

            def collect_time(page):
                time_now = datetime.datetime.now()
                time_now = time_now.strftime("%X") + " - " + time_now.strftime("%x")
                submit_time = Label(page, text="Time: {}".format(time_now), bg="#161616", fg="white", font=('Segoe UI', '13'))
                submit_time.place(x=10, y=70)
                return time_now

            def name_input(page):
                nameText = Label(page, text="Your Name: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                nameText.place(x=10, y=110)
                nameList = ("Engineer 1", "Engineer 2", "Engineer 3", "Engineer 4", "Engineer 5")
                name = StringVar()
                name.set("Select Name")
                set = OptionMenu(page, name, *nameList)
                set.configure(text="File", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, font=('Segoe UI', '10'), activebackground="#333333", activeforeground="white", highlightthickness=0, indicatoron=1)
                set.place(x=110, y=113)
                return name

            def area_select(page):
                issueAreaText = Label(page, text="Area of Issue: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                issueAreaText.place(x=10, y=150)
                issue = StringVar()
                issueArea1 = Radiobutton(page, text="Bottle Dispention", value="Bottle Dispention", variable=issue, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'))
                issueArea2 = Radiobutton(page, text="Bottle Cleaning", value="Bottle Cleaning", variable=issue, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'))
                issueArea3 = Radiobutton(page, text="Bottle Filling", value="Bottle Filling", variable=issue, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'))
                issueArea4 = Radiobutton(page, text="Bottle Wrapping", value="Bottle Wrapping", variable=issue, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'))
                issueArea5 = Radiobutton(page, text="Bottle Packaging", value="Bottle Packaging", variable=issue, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'))
                issueArea6 = Radiobutton(page, text="Box Packaging", value="Box Packaging", variable=issue, selectcolor='black', fg="white", bg="#161616", activebackground="#333333", activeforeground="white", highlightthickness=0,  font=('Segoe UI', '10'))
                issueArea1.place(x=122, y=153)
                issueArea2.place(x=250, y=153)
                issueArea3.place(x=365, y=153)
                issueArea4.place(x=464, y=153)
                issueArea5.place(x=585, y=153)
                issueArea6.place(x=710, y=153)
                return issue

            def note_input(page):
                descriptionText = Label(page, text="Extra Notes: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                descriptionText.place(x=10, y=190)
                description = Text(page, width = 100, height=20, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                description.place(x=113,y=196)
                return description

            def get_message(time_now, name_text, issue_text, description_text):
                return 'Emergency Breakdown Report from {}\n\n\tIssue ID: {}\n\tSubmission Time: {}\n\tContact Employees Name: {}\n\tArea of Issue: {}\n\tExtra Information: {}'.format(username.get(), gen_id(), time_now, name_text, issue_text, description_text)

            def submit_setup(page, time_now, name, issue, description):
                submit_button = Button(page, text="Submit", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:get_entries(page, gen_id(), time_now, name.get(), issue.get(), description.get("1.0","end-1c"), get_message(time_now, name.get(), issue.get(), description.get("1.0","end-1c"))), font=('Segoe UI', '15'))
                submit_button.place(x=800, y=530)

            def report_head(page):
                report_header = Label(page, text="REPORT", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                report_header.place(x=480, y=30, anchor="center")

            def login_head(page):
                login_header = Label(page, text="LOGIN", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                login_header.place(x=1240, y=30, anchor="center")

            def update_email(page, recieving_email, sending_email, email_pass):
                info = open("data/user_info.txt", "r+")
                text = ""
                for row in info:
                    text = row.split(",")
                    if text[0] == username.get().lower():
                        text[3] = recieving_email
                        text[4] = sending_email
                        text[5] = email_pass
                        text = ",".join(text)
                info.close()
                info = open("data/user_info.txt", "w")
                info.write(text)
                info.close()
                update_text = Label(page, text="Email Updated Sucessfully!", bg="#161616", fg="#42f456", font=('Segoe UI', '10'), width=23)
                update_text.place(x=1345, y=487, anchor="e")
                update_text.after(3000, destroy_widgit, update_text)

            def display_table(page):
                prevous_text = Label(page, text="LATEST REPORTS", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                prevous_text.place(x=480, y=590, anchor="center")
                if os.path.isfile("data/data.csv"):
                    id_header = Label(page, text="Report ID", bg="#161616", fg="white", font=('Segoe UI', '10', 'bold'))
                    username_header = Label(page, text="Submitted By", bg="#161616", fg="white", font=('Segoe UI', '10', 'bold'))
                    time_header = Label(page, text="Date/Time", bg="#161616", fg="white", font=('Segoe UI', '10', 'bold'))
                    name_header = Label(page, text="Engineer Name", bg="#161616", fg="white", font=('Segoe UI', '10', 'bold'))
                    area_header = Label(page, text="Area Of Issue", bg="#161616", fg="white", font=('Segoe UI', '10', 'bold'))
                    info_header = Label(page, text="Extra Information", bg="#161616", fg="white", font=('Segoe UI', '10', 'bold'))
                    id_header.place(x=105, y=630, anchor="w")
                    username_header.place(x=193, y=630, anchor="w")
                    time_header.place(x=315, y=630, anchor="w")
                    name_header.place(x=475, y=630, anchor="w")
                    area_header.place(x=615, y=630, anchor="w")
                    info_header.place(x=755, y=630, anchor="w")
                    with open('data/data.csv') as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        row_no = 0
                        active_row = 0
                        for table_row in csv.reader(csv_file):
                            if row_no + 6 > gen_id()-1:
                                for column in range(len(table_row)):
                                    if column == 0:
                                        element = Label(page, text=table_row[column], bg="#161616", fg="white", font=('Segoe UI', '10'), anchor="w")
                                        element.place(x=105+column*140, y=660+active_row*30, anchor="w")
                                    elif column == 2:
                                        element = Label(page, text=table_row[column], bg="#161616", fg="white", font=('Segoe UI', '10'), width=25, anchor="w")
                                        element.place(x=35+column*140, y=660+active_row*30, anchor="w")
                                    elif column < len(table_row)-1:
                                        element = Label(page, text=table_row[column], bg="#161616", fg="white", font=('Segoe UI', '10'), width=25, anchor="w")
                                        element.place(x=55+column*140, y=660+active_row*30, anchor="w")
                                    else:
                                        element = Label(page, text=table_row[column], bg="#161616", fg="white", font=('Segoe UI', '10'), width=50, anchor="w")
                                        element.place(x=55+column*140, y=660+active_row*30, anchor="w")
                                active_row += 1
                            row_no += 1
                else:
                    table_error_text = Label(page, text="No Previous Reports To Be Displayed", bg="#161616", fg="red", font=('Segoe UI', '13'))
                    table_error_text.place(x=480, y=630, anchor="center")

            def login_panel(page, login_time):
                global recieving_email, sending_email, email_pass
                stats_header = Label(page, text="STATS/INFO", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                stats_header.place(x=1240, y=200, anchor="center")
                latest_login = Label(page, text="Last Login: " + str(login_time), bg="#161616", fg="white", font=('Segoe UI', '13'))
                latest_login.place(x=1240, y=250, anchor="center")
                forms_sent = Label(page, text="Total Forms Sent: " + str(gen_id()-1), bg="#161616", fg="white", font=('Segoe UI', '13'))
                forms_sent.place(x=1240, y=280, anchor="center")
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
                settings_header = Label(page, text="SETTINGS", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
                settings_header.place(x=1240, y=350, anchor="center")
                r_email_text = Label(page, text="Recieving Email: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                r_email_text.place(x=1180, y=400, anchor="e")
                s_email_text = Label(page, text="Your Email: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                s_email_text.place(x=1180, y=430, anchor="e")
                r_email_entry = Entry(page, textvariable=recieving_email, width=40, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                r_email_entry.place(x=1180, y=393)
                s_email_entry = Entry(page, textvariable=sending_email, width=40, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                s_email_entry.place(x=1180, y=423)
                pass_text = Label(page, text="Email Password: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                pass_text.place(x=1180, y=460, anchor="e")
                email_password = Entry(page, textvariable=email_pass, width=40, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                email_password.place(x=1180, y=453)
                set_email = Button(page, text="Set Email", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:update_email(page, recieving_email.get(), sending_email.get(), email_pass.get()))
                set_email.place(x=1347, y=478)
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

            def sign_in(page, username, password, username_text, password_text, username_input, password_input, login_button):
                nonlocal tries, locked
                if request_timeout(time.time()) == True and tries < 1:
                    tries = 3
                if request_timeout(time.time()) == True:
                    file = urllib.request.urlopen("http://1.1.1.1:3402/static/credentials.txt")
                    if locked == True:
                        for line in file:
                            line = line.decode("utf-8")
                            values = line.split(",")
                            for value in values:
                                value = value.encode("utf-8")
                            password = password.encode("utf-8")
                            username = username.encode("utf-8")
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
                        tries_text = Label(page, text="Incorrect Username and Password: {} Tries Left".format(tries), bg="#161616", fg="red", font=('Segoe UI', '10'))
                        tries_text.place(x=1070, y=183, anchor="w")
                        tries_text.after(2000, destroy_widgit, tries_text)
                    if locked == False:
                        last_login = "First Time Logging In"
                        if os.path.isfile("data/user_info.txt"):
                            info = open("data/user_info.txt", "r+")
                            file_len = 0
                            for row in info:
                                file_len += 1
                                text = row.split(",")
                                if text[0] == username.decode("utf-8"):
                                    last_login = text[1]
                                    text[1] = str(datetime.datetime.now())
                                    text = ",".join(text)
                            if file_len > 0:
                                info.close()
                                info = open("data/user_info.txt", "w")
                                info.write(text)
                                info.close()
                            else:
                                info = open("data/user_info.txt", "w")
                                info.write(username.decode("utf-8") + "," + str(datetime.datetime.now()) + "," + "0" + "," + "" + "," + "" + "," + "")
                                info.close()
                        else:
                            info = open("data/user_info.txt", "w")
                            info.write(username.decode("utf-8") + "," + str(datetime.datetime.now()) + "," + "0" + "," + "" + "," + "" + "," + "")
                            info.close()
                        welcome_text = Label(page, text="Welcome {}".format(username.decode("utf-8")), bg="#161616", fg="white", font=('Segoe UI', '20'))
                        about_text = Label(page, text="Enter values for each field then press submit", bg="#161616", fg="white", font=('Segoe UI', '15'))
                        welcome_text.place(x=1240, y=90, anchor="center")
                        about_text.place(x=1240, y=120, anchor="center")
                        login_panel(page, last_login)
                        send_email("Security Alert: \n\n\tA sucessfull login attempt occured at {}".format(datetime.datetime.now()), "Security Alert: Sucessfull Login Attempt")
                    if locked == True and tries < 1:
                        file = open("data/logins.txt","w+")
                        file.write(str(time.time()))
                        file.close()
                        send_email("Security Alert: \n\n\tUnsuccessful login attempt occured at {}\n\tYour account is now locked for {} seconds\n\tContact Administrator for further assistance".format(datetime.datetime.now(), time_out), "Security Alert: Unsuccessful Login Attempt")
                if request_timeout(time.time()) == False:
                    tries_text = Label(page, text="Error: Out of Attempts, wait {:.2f}s".format(to_wait), bg="#161616", fg="white", font=('Segoe UI', '10'), width=60)
                    tries_text.place(x=1037, y=183, anchor="w")
                    tries_text.after(2000, destroy_widgit, tries_text)

            def login(page):
                global username
                username_text = Label(page, text="Username: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                username_text.place(x=1190, y=83, anchor='e')
                password_text = Label(page, text="Password: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
                password_text.place(x=1190, y=113, anchor='e')
                username = StringVar()
                password = StringVar()
                username_input = Entry(page, textvariable=username, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                username_input.place(x=1190, y=76)
                password_input = Entry(page, textvariable=password, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
                password_input.place(x=1190, y=106)
                login_button = Button(page, text="Login", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:sign_in(page, username.get().lower(), password.get(), username_text, password_text, username_input, password_input, login_button), font=('Segoe UI', '12'))
                login_button.place(x=1247, y=136)

            def setup():
                page = Frame(root, bg="#161616", width = 1920, height = 1000)
                page.place(x=1920/2, y=60, anchor="n")
                report_head(page)
                login_head(page)
                login(page)
                time_now = collect_time(page)
                name = name_input(page)
                issue = area_select(page)
                description = note_input(page)
                submit_setup(page, time_now, name, issue, description)

            setup()

        def about(root):
            bar = Frame(root, bg="#474747")
            bar.place(x=800, y=900, anchor="s", width=1600)
            info1 = Label(bar, text="Version 1.3", bg="#474747", fg="white")
            info2 = Label(bar, text="Developed by Fraser Love", bg="#474747", fg="white")
            info3 = Label(bar, text="Partners: Evolution BPS", bg="#474747", fg="white")
            info1.grid(row=0, column=0, padx=10)
            info2.grid(row=0, column=1, padx=10)
            info3.grid(row=0, column=2, padx=10)

        background(root)
        main(root)
        navbar(root)
        about(root)

    root = initalise_app()
    root_screen(root)
    x_pos = int(root.winfo_screenwidth()/2)-800
    y_pos = int(root.winfo_screenheight()/2)-450
    root.geometry("1600x900+" + str(x_pos) + "+" + str(y_pos))
    root.resizable(0, 0)
    root.mainloop()

app()
