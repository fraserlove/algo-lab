"""
TODO:
  - Show table for last 10 days of BloodLevels and Insulin
  - Add ability to add extra blood levels at snack times
  - Add another table for insulin given
  - Add another table for description of what was eat and the carbs
  - Add another table for extra info such as type and length of exercise and when it was done
  - Add a method to graph out blood levels and insulin given against time, as well as weekly and monthly mean values
  - Include in the graph lines to show the max and min blood levels set by the user
  - Include location tracking ability so that when walking and running it can see how much exercise has been done
  - When enough exercise has been done notify user (with sound or buzz) that they should eat to increase blood levels and what it should be
  - Include options for user to record carbs in favorite foods (e.g. 40g in Porridge)
  - Include machine learning algo to guess the amount of carbs in a food from a photo (e.g. guess carbs in Cake just from photo of it using previous data)
  - Include notifications for user for when to take base insulin (degladec)
  - Find out the curve of novorapid and use machine learning to calculate the percentage of time a user spends within insulin limits e.g between 4-12
  - Include carb counting feature (adding up items of food)
  - Allow way for restaraunts to upload info on the carbs in their foods so that a user can easily search for a menu item and add it to their list
  - Use machine learning to find optimum ratio for:
        - insulin to inject per 10g of carbs
        - how much your blood levels decrease overnight and between each meal
        - how much your blood levels decrease for every unit of correction dose
        - how much your blood levels decrease for every mile of walking (or other unit of exercise)



"""


from tkinter import *
from db import Database

db = Database('Diatrac.db')

def submit_levels():
    db.insert(br_text.get(), ln_text.get(), dn_text.get(), bt_text.get())

# Create window object
app = Tk()

# Window variables
app.title('Diatrac')
app.geometry('1200x550')

# Widgits
bsl_title = Label(app, text='Blood Sugar Levels', font=('bold', 28))
bsl_title.place(x=20, y=20)
input_bsl_title = Label(app, text='Record your blood sugar levels for today by entering their values and clicking submit.', font=('bold', 16))
input_bsl_title.place(x=20, y=80)
# ------------------------ Blood Sugar Inputs ------------------------
values = db.fetch_current()
if values != None:
    br_text, ln_text, dn_text, bt_text = (StringVar(value=values[i]) for i in range (0,4))
else:
    br_text, ln_text, dn_text, bt_text = StringVar(), StringVar(), StringVar(), StringVar()

br_label = Label(app, text='Breakfast', font=('bold', 14))
br_label.place(x=20, y=108)
br_entry = Entry(app, textvariable=br_text, width=4)
br_entry.place(x=90, y=105)
ln_label = Label(app, text='Lunch', font=('bold', 14))
ln_label.place(x=140, y=108)
ln_entry = Entry(app, textvariable=ln_text, width=4)
ln_entry.place(x=190, y=105)
dn_label = Label(app, text='Dinner', font=('bold', 14))
dn_label.place(x=240, y=108)
dn_entry = Entry(app, textvariable=dn_text, width=4)
dn_entry.place(x=290, y=105)
bt_label = Label(app, text='Bedtime', font=('bold', 14))
bt_label.place(x=340, y=108)
bt_entry = Entry(app, textvariable=bt_text, width=4)
bt_entry.place(x=405, y=105)
submit_button = Button(app, text='Submit', command=submit_levels, width=4)
submit_button.place(x=460, y=105)
# ---------------------------------------------------------------------

# Start program
app.mainloop()
