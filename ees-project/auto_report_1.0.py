"""
EES Project Automatic Error Report Software - Development Version 1.0
Developed by Fraser Love on 8/12/18
Dependencies: Tkinter

Features
- Automatic CSV file creation
- Automatic additon of user entered values to CSV files
- Login with username and password
- Stylish GUI
- Hashed passwords for extra security
- Extra UI robustness enhancements
- Automatic email of reports
"""

from tkinter import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime, csv, os, time, hashlib, uuid, smtplib

def initalise_app():
    root = Tk()
    root.attributes("-fullscreen", True)
    return root

def close_window():
    root.destroy()

def root_screen(root):
    tries = 3
    locked = True
    def background(root):
        background = Frame(root, bg="#212121", width = 1920, height = 1080)
        title = Label(background, text="Auto Report System", bg="#212121", fg="white", font=('Segoe UI', '24', 'bold'))
        background.place(x=1920/2, y=1080/2, anchor="center")
        title.place(x=10, y=50, anchor="w")

    def navbar(root):
        nav = Frame(root, bg="#474747")
        title = Label(nav, text="Client Interface Software - Development Version", bg="#474747", fg="white")
        button1 = Button(nav, text="File", fg="white", bg="#474747", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white")
        button2 = Button(nav, text="Open", fg="white", bg="#474747", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white")
        button3 = Button(nav, text="Help", fg="white", bg="#474747", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white")
        button4 = Button(nav, text="Exit", fg="white", bg="#474747", borderwidth=0, height = 1, width = 5, activebackground="#333333", activeforeground="white", command=close_window)
        nav.place(x=0, y=0, anchor="nw")
        button1.grid(row=0, column=0)
        button2.grid(row=0, column=1)
        button3.grid(row=0, column=2)
        button4.grid(row=0, column=3, padx=1756, sticky="E")
        title.place(x=1920/2, y=10, anchor="center")

    def gen_id():
        form_id = 1
        if os.path.isfile("data.csv"):
            file = open("data.csv", "r")
            for row in csv.reader(file):
                form_id += 1
        return form_id

    def main(root):
        def destroy_widgit(widgit):
            widgit.destroy()

        def send_email(form_id, time_now, name, issue, enteredText):
            email = 'email@gmail.com'
            password = 'password'
            send_to_email = 'email@gmail.com'
            subject = '{}: Breakdown Report'.format(username.get())
            message = 'Emergency Breakdown Report from {}\n\n\tIssue ID: {}\n\tSubmission Time: {}\n\tContact Employees Name: {}\n\tArea of Issue: {}\n\tExtra Information: {}'.format(username.get(), form_id, time_now, name, issue, enteredText) #Add to message other contact info phone etc

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

        def get_entries(page, form_id, time_now, name, issue, enteredText):
            if locked == False:
                file = open("data.csv", "a", newline="")
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writerow([form_id, username.get(), time_now, name, issue, enteredText])
                send_email(form_id, time_now, name, issue, enteredText)
                print("Appended: {} {} {} {}".format(form_id, username.get(), time_now, name, issue, enteredText))
                file.close()
                submit_display(page, "FORM ID {}: SUCESSFULLY SUBMITTED".format(gen_id()-1), "white")
            if locked == True:
                submit_display(page, "ERROR: FORM NOT SUBMITTED, YOU ARE NOT LOGGED IN", "red")


        def submit_display(page, string, colour):
            submit_text = Label(page, text=string, bg="#161616", fg=colour, font=('Segoe UI', '10'))
            submit_text.place(x=920, y=595, anchor="e")
            submit_text.after(2500, destroy_widgit, submit_text)

        def collect_time(page):
            time_now = datetime.datetime.now()
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

        def submit_setup(page, time_now, name, issue, description):
            submitButton = Button(page, text="Submit", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:get_entries(page, gen_id(), time_now, name.get(), issue.get(), description.get("1.0",END)), font=('Segoe UI', '15'))
            submitButton.place(x=800, y=530)

        def report_head(page):
            report_header = Label(page, text="REPORT", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
            report_header.place(x=480, y=30, anchor="center")

        def login_head(page):
            login_header = Label(page, text="LOGIN", bg="#161616", fg="white", font=('Segoe UI', '18', 'bold'))
            login_header.place(x=1440, y=30, anchor="center")

        def hash_password(password):
            hash_object = hashlib.sha256(password.encode())
            hex_dig = hash_object.hexdigest()
            return hex_dig

        def sign_in(page, password, username_text, password_text, username_input, password_input, login_button):
            nonlocal tries, locked
            file = open("credentials.txt", "r") # Stored on server
            if tries > 0 and locked == True:
                for line in file:
                    values = line.split(",")
                    hashed_password = values[1][:64]
                    if username.get() == values[0] and hash_password(password) == hashed_password:
                        locked = False
                        destroy_widgit(username_text)
                        destroy_widgit(username_input)
                        destroy_widgit(password_text)
                        destroy_widgit(password_input)
                        destroy_widgit(login_button)
                else:
                    tries -= 1
            if locked == True:
                tries_text = Label(page, text="Incorrect Username and Password: {} Tries Left".format(tries), bg="#161616", fg="white", font=('Segoe UI', '10'))
                tries_text.place(x=1270, y=183, anchor="w")
                tries_text.after(2000, destroy_widgit, tries_text)
            if locked == False:
                tries_text = Label(page, text="SUCESSFULLY LOGGED IN", bg="#161616", fg="white", font=('Segoe UI', '10'))
                tries_text.place(x=1440, y=100, anchor="center")
                welcome_text = Label(page, text="Welcome {}".format(username.get()), bg="#161616", fg="white", font=('Segoe UI', '20'))
                about_text = Label(page, text="Enter values for each field then press submit", bg="#161616", fg="white", font=('Segoe UI', '15'))
                welcome_text.place(x=1440, y=200, anchor="center")
                about_text.place(x=1440, y=250, anchor="center")
            if locked == True and tries < 1:
                tries_text = Label(page, text="Ran out of tries: Account Locked", bg="#161616", fg="white", font=('Segoe UI', '10'), width=60)
                tries_text.place(x=1237, y=183, anchor="w")
                print("Ran out of tries: Account Locked")

        def login(page):
            global username
            username_text = Label(page, text="Username: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
            username_text.place(x=1390, y=83, anchor='e')
            password_text = Label(page, text="Password: ", bg="#161616", fg="white", font=('Segoe UI', '13'))
            password_text.place(x=1390, y=113, anchor='e')
            username = StringVar()
            password = StringVar()
            username_input = Entry(page, textvariable=username, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
            username_input.place(x=1390, y=76)
            password_input = Entry(page, textvariable=password, width=25, bg="#474747", fg="white", highlightcolor="#161616", bd=0, highlightthickness="1",  highlightbackground="#dbdbdb")
            password_input.place(x=1390, y=106)
            login_button = Button(page, text="Login", fg="white", bg="#474747", borderwidth=0, height = 1, width = 10, activebackground="#333333", activeforeground="white", command=lambda:sign_in(page, password.get(), username_text, password_text, username_input, password_input, login_button), font=('Segoe UI', '12'))
            login_button.place(x=1447, y=136)

        def setup():
            page = Frame(root, bg="#161616", width = 1920, height = 1000)
            page.place(x=1920/2, y=80, anchor="n")
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
        bar.place(x=1920/2, y=1080, anchor="s", width=1920)
        info1 = Label(bar, text="Version 1.0", bg="#474747", fg="white")
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
root.mainloop()
