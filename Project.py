from tkinter import *
from tkinter import messagebox as msg
import tkinter as tk
from tkinter import ttk,simpledialog
from PIL import ImageTk
import csv
import re
import random
import  mysql.connector
from tkcalendar import Calendar,DateEntry 



class HealthFitnessApp:
    def __init__(self, root):
        self.root = root
        self.user_profile_window = None
        self.combo_food = None
        self.login_window = None
        self.result_label = None  
        self.root.title("Health and Fitness App")
        self.root.geometry('950x600+100+50')
        self.root.configure(bg='#fff')
        self.root.resizable(False, False)
        self.generated_otp = None
       

        # Load nutrition data from CSV 
        self.nutrition_data = self.load_nutrition_data()
      # Load exercise data from CSV
        self.exercise_data = self.load_exercise_data()

        self.bg = ImageTk.PhotoImage(file='F:\\New\\healthcare.png')
        self.image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)   
        self.profile_img = ImageTk.PhotoImage(file='F:\\New\\profile.png')
        self.dashboard = ImageTk.PhotoImage(file='F:\\New\\dash.png')
            
        self.advance_exercise_frame = None
        self.yoga_frame = None
        self.surya_namaskar_frame = None

        
        #Login frame
        frame = Frame(self.root, width=360, height=400, bg='white')
        frame.place(x=520, y=100)
        title = Label(frame, text='Login', bg='White', fg='#d77337', font=('Georgia', 30))
        title.place(x=130, y=10)

        username_label = tk.Label(frame, text="Username:", bg='white', font=('Georgia', 15, 'bold')).place(x=30, y=90)
        self.txt_user = Entry(frame, font=('Georgia', 15))
        self.txt_user.place(x=30, y=130, width=200, height=35)

        password_label = tk.Label(frame, text="Password:", bg='white', font=('Georgia', 15, 'bold')).place(x=30, y=180)
        self.txt_pass = Entry(frame,show='*', font=('Georgia', 15))
        self.txt_pass.place(x=30, y=220, width=200, height=35)

        forget_bt = Button(frame, text='Forget Password', command=self.forget_password, cursor='hand2', bg='white',
                           fg='#d77337', bd=0, font=('Georgia', 15)).place(x=30, y=260)
        Login_bt = Button(frame, command=self.login, cursor='hand2', text='Login', bg='#d77337', fg='white', bd=0,
                          font=('Georgia', 18)).place(x=120, y=300)
        register_bt = Button(frame, text="Don't have an account? Register here", command=self.open_registration,
                             cursor='hand2', bg='white', fg='#d77337', bd=0, font=('Georgia', 15)).place(x=10, y=360)

    def login(self):
        if self.txt_user.get() == "" or self.txt_pass.get() == "":
            msg.showerror("Error", "All fields are required", parent=self.root)
        else:
            db = mysql.connector.connect(host='localhost', user='root', password='root', database='health_fitness_db')
            cursor = db.cursor()
            query = "SELECT user_id FROM user WHERE username=%s AND password=%s"
            values = (self.txt_user.get(), self.txt_pass.get())
            cursor.execute(query, values)
            user_id_tuple = cursor.fetchone()
            db.close()

            if user_id_tuple:
                user_id = user_id_tuple[0] 
                msg.showinfo("Welcome", "Welcome", parent=self.root)
                self.close_login_window()
                self.open_user_profile(user_id)
            else:
                msg.showerror("Error", "Invalid username/Password", parent=self.root)

    def forget_password(self):
        msg.showinfo("Reset Password", "Password reset instructions sent to your email.", parent=self.root)

#**********************************************************************************************************************************#   

    def open_registration(self):
        registration_window = Toplevel(self.root)
        registration_window.title("Register")
        registration_window.geometry('400x450+300+100')
        registration_window.configure(bg="black")

        registration_frame = Frame(registration_window, width=380, height=430, bg='white')
        registration_frame.pack()

        title = Label(registration_frame, text='Register', bg='White', fg='#d77337', font=('Georgia', 30))
        title.place(x=120, y=10)

        username_label = Label(registration_frame, text="Username:", bg='white', font=('Georgia', 15, 'bold')).place(x=20, y=90)
        self.register_user_entry = Entry(registration_frame, font=('Georgia', 15))
        self.register_user_entry.place(x=20, y=120, width=200, height=25)

        password_label = Label(registration_frame, text="Password:", bg='white',font=('Georgia', 15, 'bold')).place(x=20, y=160)
        self.register_pass_entry = Entry(registration_frame, show='*',font=('Georgia', 15))
        self.register_pass_entry.place(x=20, y=190, width=200, height=25)

        contact_label = Label(registration_frame, text="Contact No.:", bg='white', font=('Georgia', 15, 'bold')).place(x=20, y=230)
        self.contact_entry = Entry(registration_frame, font=('Georgia', 15))
        self.contact_entry.place(x=20, y=260, width=200, height=25)

        otp_label = Label(registration_frame, text="OTP:", bg='white', font=('Georgia', 15, 'bold')).place(x=20, y=320)
        self.otp_entry = Entry(registration_frame, font=('Georgia', 15))
        self.otp_entry.place(x=20, y=350, width=200, height=25)

        generate_otp_button = Button(registration_frame, text='Generate OTP', command=self.generate_and_send_otp,
                                     cursor='hand2', bg='white', fg='#d77337', bd=0, font=('Georgia', 15)).place(x=120, y=280)

        register_button = Button(registration_frame, text='Register', command=self.register_user, cursor='hand2',
                             bg='#d77337', fg='white', bd=0, font=('Georgia', 15)).place(x=20, y=400)

        B = Button(registration_frame, text='Close', command=registration_window.destroy, cursor='hand2', bg='Red',
               fg='white', font=('Georgia', 15)).place(x=250, y=400)

    def generate_and_send_otp(self):
        self.generated_otp = self.generate_otp()

        msg.showinfo("OTP", f"Your OTP is: {self.generated_otp}", parent=self.root)

    def generate_otp(self):
        return str(random.randint(1000, 9999))

    def register_user(self):
        username = self.register_user_entry.get()
        password = self.register_pass_entry.get()
        contact = self.contact_entry.get()
        user_entered_otp = self.otp_entry.get()

        if username == "" or password == "" or contact == "" or user_entered_otp == "":
            msg.showerror("Error", "All fields are required", parent=self.root)
        else:
        # Verify the entered OTP
            if user_entered_otp == self.generated_otp:
            # If OTP is correct, save user details
                self.save_user_details(username, password, contact)

            # Inform the user about successful registration
                msg.showinfo("Registration Successful", "Registration successful!", parent=self.root)
            else:
                msg.showerror("Error", "Invalid OTP. Registration failed.", parent=self.root)

    def save_user_details(self, username, password, contact):
        db = None
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='root', database='health_fitness_db')
            cursor = db.cursor()

        # Check if the username already exists
            check_query = "SELECT * FROM user WHERE username=%s"
            check_values = (username,)
            cursor.execute(check_query, check_values)
            existing_user = cursor.fetchone()

            if existing_user:
                msg.showerror("Error", "Username already exists. Please choose a different username.",parent=self.root)
            else:
            # Insert the new user into the database
                insert_query = "INSERT INTO user (username, password, contact) VALUES (%s, %s, %s)"
                insert_values = (username, password, contact)
                cursor.execute(insert_query, insert_values)
                db.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if db:
                db.close()


#***********************************************************************************************************************************#
        # USER_PROFILE
           
    def open_user_profile(self, user_id):
        self.user_id=user_id
        user_profile_window = Toplevel(self.root)
        user_profile_window.title("User Profile")
        user_profile_window.geometry('750x400+300+100')
        user_profile_window.configure(bg='black')

        user_profile_frame = Frame(user_profile_window, width=700, height=380 )
        user_profile_frame.pack()

    # Load the profile logo image
        profile_logo = PhotoImage(file='F:\\New\\profile.png')
        profile_logo_label = Label(user_profile_frame, image=profile_logo, bg='white')
        profile_logo_label.image = profile_logo
        profile_logo_label.place(x=280, y=20)  # Adjust the coordinates as needed

        Label(user_profile_frame, text="Name:", font=('Georgia', 15, 'bold')).place(x=10, y=140)
        self.name_entry = Entry(user_profile_frame, width=10,font=('Georgia', 14))
        self.name_entry.place(x=110, y=140)

        Label(user_profile_frame, text="Age:", font=('Georgia', 15, 'bold')).place(x=370, y=140)
        self.age_var = StringVar()
        self.age_var.set("  ")

        age_options = [str(i) for i in range(1, 101)]  # Assuming age can be from 1 to 100
        self.age_combobox = ttk.Combobox(user_profile_frame, textvariable=self.age_var, values=age_options, font=('Georgia', 14))
        self.age_combobox.place(x=450, y=140)
        self.age_combobox.config(width=10)  # Set a fixed width for the age combobox

        Label(user_profile_frame, text="Gender:", font=('Georgia', 15, 'bold')).place(x=10, y=200)
        self.gender_var = StringVar()
        self.gender_var.set(" ")

        gender_options = ["Male", "Female", "Other"]
        self.gender_combobox = ttk.Combobox(user_profile_frame, textvariable=self.gender_var, values=gender_options, font=('Georgia', 14))
        self.gender_combobox.place(x=110, y=200)
        self.gender_combobox.config(width=10)

        Label(user_profile_frame, text="Height(cm):", font=('Georgia', 15, 'bold')).place(x=370, y=200)
        self.height_entry = Entry(user_profile_frame, width=10,font=('Georgia', 14))
        self.height_entry.place(x=520, y=200)

        Label(user_profile_frame, text="Weight(kg):", font=('Georgia', 15, 'bold')).place(x=10, y=260)
        self.weight_entry = Entry(user_profile_frame, width=10,font=('Georgia', 14))
        self.weight_entry.place(x=150, y=260)

        Label(user_profile_frame, text="Goal Weight(kg):", font=('Georgia', 15, 'bold')).place(x=370, y=260)
        self.goal_weight_entry = Entry(user_profile_frame,width=10, font=('Georgia', 14))
        self.goal_weight_entry.place(x=545, y=260)

        save_button = Button(user_profile_frame, text='Save', command=lambda: self.save_and_open_homepage(user_id),
                     cursor='hand2', bg='#d77337', fg='white', bd=0, font=('Georgia', 18))
        save_button.place(x=280, y=320)

    def save_and_open_homepage(self, user_id):
        self.save_user_data(user_id)
        self.open_home_page(user_id)
                     
    def save_user_data(self, user_id):
        self.user_id = user_id
        name = self.name_entry.get()
        age = int(self.age_combobox.get())
        gender = self.gender_combobox.get()
        height = float(self.height_entry.get())
        weight = float(self.weight_entry.get())
        goal_weight = float(self.goal_weight_entry.get())

        db = None
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='root', database='health_fitness_db')
            cursor = db.cursor()

        # Check if the user exists in the users table
            user_exists_query = "SELECT * FROM user WHERE user_id = %s"
            cursor.execute(user_exists_query, (self.user_id,))
            user_exists = cursor.fetchone()

            if user_exists:
                save_user_data_query = """
                    INSERT INTO user_profiles (user_id, name, age, gender, height, weight, goal_weight)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name=VALUES(name), age=VALUES(age), gender=VALUES(gender),
                    height=VALUES(height), weight=VALUES(weight), goal_weight=VALUES(goal_weight)
            """

            # Replace the placeholders with actual values
                save_user_data_data = (self.user_id, name, age, gender, height, weight, goal_weight)

            # Execute the query
                cursor.execute(save_user_data_query, save_user_data_data)
                db.commit()
                msg.showinfo("User Profile", "User data saved successfully", parent=self.user_profile_window)
            else:
                print("User does not exist")

        except Exception as e:
            print(f"Error : {e}", e)

        finally:
            if db:
                db.close()
          
#********************************************************************************************************************************#
        # HOME_PAGE

    def open_home_page(self,user_id):
        if self.user_profile_window:
            self.user_profile_window.destroy()

        # Create a new homepage window
        home_page_window = Toplevel(self.root)
        home_page_window.title("Home Page")
        home_page_window.geometry('850x500+100+50')
        home_page_window.configure(bg="black")

        home_page_frame = Frame(home_page_window, bg='honeydew2' ,width=830, height=480)
        home_page_frame.pack()
        
        # Create a Label widget for the image
        image_label = Label(home_page_frame, image=self.dashboard)
        image_label.place(x=10, y=10)

        # Create a Label for "Health Dashboard"
        health_dashboard_label = Label(home_page_frame, text="Health Dashboard", font=('Georgia', 18,'bold'), bg='honeydew2')
        health_dashboard_label.place(x=260, y=10)

        height_label = Label(home_page_frame, text="Height:", font=('Georgia', 16), bg='honeydew2')
        height_label.place(x=250, y=50)
        height_entry = Entry(home_page_frame, font=('Georgia', 13), width=8, bg='honeydew2')
        height_entry.place(x=340, y=50)

        weight_label = Label(home_page_frame, text="Weight:", font=('Georgia', 16), bg='honeydew2')
        weight_label.place(x=250, y=80)
        weight_entry = Entry(home_page_frame, font=('Georgia', 13),width=8,bg='honeydew2')
        weight_entry.place(x=340, y=80)

        goal_weight_label = Label(home_page_frame, text="Goal weight:", font=('Georgia', 16), bg='honeydew2')
        goal_weight_label.place(x=250, y=110)
        goal_weight_entry = Entry(home_page_frame, font=('Georgia', 13),width=8,bg='honeydew2')
        goal_weight_entry.place(x=370, y=110)

        #Retrieve user data from the database
        user_data = self.fetch_user_data(user_id)

   
        if user_data:
            height_entry.insert(0, user_data['height'])
            weight_entry.insert(0, user_data['weight'])
            goal_weight_entry.insert(0, user_data['goal_weight'])

            # Add buttons for different functionalities on the home page
            health_tips_bt = Button(home_page_frame, text="Health Tips", command=self.show_health_tips, cursor='hand2',
                            bg='old lace', fg='#d77337', bd=0, font=('Georgia', 15)).place(x=100, y=300)

            diet_planner_bt = Button(home_page_frame, text="Diet Planner", command=self.show_diet_planner, cursor='hand2',
                             bg='old lace', fg='#d77337', bd=0, font=('Georgia', 15)).place(x=300, y=300)

            exercise_bt = Button(home_page_frame, text="Excercise", command=self.show_exercise, cursor='hand2',
                              bg='old lace', fg='#d77337', bd=0, font=('Georgia', 15)).place(x=180, y=380)

            health_calculator_bt = Button(home_page_frame, text="Health Calculator", command=self.show_health_calculator,
                                  cursor='hand2', bg='old lace', fg='#d77337', bd=0, font=('Georgia', 15)).place(x=330, y=380)

            goal_setting_bt = tk.Button(home_page_frame, text="Goal Setting", command=lambda: self.open_goal_setting_window(user_id),
                                     cursor='hand2', bg='old lace', fg='#d77337', bd=0, font=('Georgia', 15))
            goal_setting_bt.place(x=500, y=300)

          

         # Calendar widget directly on the home page
            cal_width = 300
            cal_height = 150
            cal_x = 520
            cal_y = 10
            cal = Calendar(home_page_frame, selectmode="day", date_pattern="yyyy-mm-dd")
            cal.place(width=cal_width, height=cal_height, x=cal_x, y=cal_y)
            self.show_calendar(home_page_frame)

        

            
    def show_calendar(self, parent):
        pass
       

    def fetch_user_data(self, user_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='root', database='health_fitness_db')
            cursor = db.cursor()
            query = "SELECT height, weight, goal_weight FROM user_profiles WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()   
            cursor.close()
            db.close()
            
        # Return user data as a dictionary or None if not found
            if user_data:
                return {
                    'height': user_data[0],
                    'weight': user_data[1],
                    'goal_weight': user_data[2],
                    }
            else:
                return None

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    


       
#*********************************************************************************************************************************#
        #SET_GOALS
        
    def open_goal_setting_window(self,user_id):
        self.user_id = user_id
        self.goal_setting_window = tk.Toplevel()
        self.goal_setting_window.title("Goal Setting")
        self.goal_setting_window.geometry('400x400+300+100')
        self.goal_setting_window.configure(bg='honeydew2')

        # Widgets for goal setting
        goal_type_label = tk.Label(self.goal_setting_window, text="Goal Type:", font=('Georgia', 15))
        goal_type_label.place(x=10, y=10)

        self.goal_type_var = tk.StringVar()
        goal_type_combobox = ttk.Combobox(self.goal_setting_window, textvariable=self.goal_type_var, values=["Weight Loss", "Muscle Gain", "Cardio", "Flexibility"], font=('Georgia', 15))
        goal_type_combobox.place(x=140, y=10 ,width=150)

        target_value_label = tk.Label(self.goal_setting_window, text="Target Value:", font=('Georgia', 15))
        target_value_label.place(x=10, y=60)

        self.target_value_entry = tk.Entry(self.goal_setting_window,  width=10,font=('Georgia', 15))
        self.target_value_entry.place(x=140, y=60)

        current_value_label = tk.Label(self.goal_setting_window, text="Current Value:", font=('Georgia', 15))
        current_value_label.place(x=10, y=110)

        self.current_value_entry = tk.Entry(self.goal_setting_window, width=10, font=('Georgia', 15))
        self.current_value_entry.place(x=140, y=110)

        # ComboBox Label for Start Day
        start_date_label = tk.Label(self.goal_setting_window, text="Start Date:", font=('Georgia', 15))
        start_date_label.place(x=10, y=160)

        # ComboBox for Start Day
        self.start_day_combobox = ttk.Combobox(self.goal_setting_window, values=[str(day) for day in range(1, 32)], font=('Georgia', 15))
        self.start_day_combobox.place(x=120, y=160,width=60)
        self.start_month_combobox = ttk.Combobox(self.goal_setting_window, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], font=('Georgia', 15))
        self.start_month_combobox.place(x=180, y=160,width=90)
        self.start_year_combobox = ttk.Combobox(self.goal_setting_window, values=[str(year) for year in range(2022, 2033)], font=('Georgia', 15))
        self.start_year_combobox.place(x=270, y=160,width=90)

        # ComboBox Label for end Day
        end_date_label = tk.Label(self.goal_setting_window, text="End Date:", font=('Georgia', 15))
        end_date_label.place(x=10, y=210)

        # ComboBox for End Day
        self.end_day_combobox = ttk.Combobox(self.goal_setting_window, values=[str(day) for day in range(1, 32)], font=('Georgia', 15))
        self.end_day_combobox.place(x=120, y=210,width=60)
        self.end_month_combobox = ttk.Combobox(self.goal_setting_window, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], font=('Georgia', 15))
        self.end_month_combobox.place(x=180, y=210,width=90)
        self.end_year_combobox = ttk.Combobox(self.goal_setting_window, values=[str(year) for year in range(2022, 2033)], font=('Georgia', 15))
        self.end_year_combobox.place(x=270, y=210,width=90)

        # Save button
        save_button = tk.Button(self.goal_setting_window, text="Save Goal", command=self.save_goal, cursor='hand2', bg='#d77337', fg='white', bd=0, font=('Georgia', 15))
        save_button.place(x=10, y=300)

        B = tk.Button(self.goal_setting_window, text='Close', command=self.goal_setting_window.destroy, cursor='hand2', bg='Red', fg='white', font=('Georgia', 15))
        B.place(x=200, y=300)


        
    def save_goal(self):
        goal_type = self.goal_type_var.get()
        target_value = float(self.target_value_entry.get())
        current_value = float(self.current_value_entry.get()) if self.current_value_entry.get() else None
        # Retrieve selected values from ComboBoxes for start date
        start_day = int(self.start_day_combobox.get())
        start_month = self.start_month_combobox.get()
        start_year = int(self.start_year_combobox.get())
        start_date = f"{start_year:04d}-{self.month_to_number(start_month):02d}-{start_day:02d}"

    # Retrieve selected values from ComboBoxes for end date
        end_day = int(self.end_day_combobox.get())
        end_month = self.end_month_combobox.get()
        end_year = int(self.end_year_combobox.get())
        end_date = f"{end_year:04d}-{self.month_to_number(end_month):02d}-{end_day:02d}"

        db = None
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='root', database='health_fitness_db')
            cursor = db.cursor()

              # Check if a record with the same goal_type already exists for the user
            select_query = "SELECT * FROM set_goals WHERE user_id = %s AND goal_type = %s"
            cursor.execute(select_query, (self.user_id, goal_type))
            existing_record = cursor.fetchone()

            if existing_record:
            # Update the existing record
                update_query = (
                "UPDATE set_goals SET target_value = %s, current_value = %s, start_date = %s, end_date = %s "
                "WHERE user_id = %s AND goal_type = %s"
            )
                update_data = (target_value, current_value, start_date, end_date, self.user_id, goal_type)
                cursor.execute(update_query, update_data)
            else:
            # Insert a new goal
                insert_query = "INSERT INTO set_goals (user_id, goal_type, target_value, current_value, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (self.user_id, goal_type, target_value, current_value, start_date, end_date))

            db.commit()
            msg.showinfo("Success", "Goal saved successfully!")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if db:
                db.close()

    # Add a helper function to convert month name to number
    def month_to_number(self, month_name):
        months = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
        }
        return months.get(month_name, 1)  # Default to 1 if month name is not found
                
#**********************************************************************************************************************************#
     #HEALTH_TIPS
  
    def show_health_tips(self):
        # Add code here to display health tips on the home page
        health_tips_window = Toplevel(self.root)
        health_tips_window.title("Health Tips")
        health_tips_window.geometry('400x400+300+100')
        health_tips_window.configure(bg="black")

        health_tips_frame = Frame(health_tips_window, bg='honeydew2',width=400, height=480)
        health_tips_frame.pack()

        title = Label(health_tips_frame, text='Health Tips', bg='honeydew2', fg='#d77337', font=('Georgia', 30))
        title.place(x=80, y=20)

        tips_label = Label(health_tips_frame, text="1. Stay hydrated.\n2. Get regular exercise.\n3. Eat a balanced diet.\n4. Eat nuts and seeds.\n5. Get enough sleep.\n6. Avoid bright lights before sleep.\n7. Eat adequate protein.\n8. Minimize your sugar intake.\n9. Meditate.\n10. Check your blood pressure regularly.",
                           bg='honeydew2', font=('Georgia', 15)).place(x=10, y=90)
        B1= Button(health_tips_frame, text=' Close ', command=health_tips_window.destroy, cursor='hand2', bg='Red',
                           fg='white',font=('Georgia', 15)).place(x=180, y=350)

  

#**********************************************************************************************************************************#    
     #DIET_PLANNER

    def show_diet_planner(self):
        diet_planner_window = Toplevel(self.root)
        diet_planner_window.title("Diet Planner")
        diet_planner_window.geometry('400x400+300+100')

        diet_planner_frame = Frame(diet_planner_window, width=400, height=380, bg='honeydew2')
        diet_planner_frame.pack()

        title = Label(diet_planner_frame, text='Diet Planner', bg='honeydew2', fg='#d77337', font=('Georgia', 30))
        title.place(x=80, y=20)

        # Relevant diet information
        diet_info = "1. Breakfast: Oatmeal with fruits\n" \
                    "2. Snack: Greek yogurt with almonds\n" \
                    "3. Lunch: Grilled chicken salad\n" \
                    "4. Snack: Fresh fruit smoothie\n" \
                    "5. Dinner: Baked salmon with quinoa"

        diet_label = Label(diet_planner_frame, text=diet_info, bg='honeydew2', font=('Georgia', 15)).place(x=10, y=90)

        diet_bt = Button(diet_planner_frame, text=' Close ', command=diet_planner_window.destroy, cursor='hand2', bg='Red',
                     fg='white', font=('Georgia', 15)).place(x=150, y=300)

#***********************************************************************************************************************************#
    # HEALTH_CALCULATOR

    def show_health_calculator(self):
        health_calculator_window = Toplevel(self.root)
        health_calculator_window.title("Health Calculator")
        health_calculator_window.geometry('400x350+300+100')
        health_calculator_window.configure(bg="black")

        health_calculator_frame = Frame(health_calculator_window, bg='honeydew2')
        health_calculator_frame.pack(expand=True, fill='both')

        # Title label
        title_label = Label(health_calculator_frame, text='Health Calculator', bg='honeydew2', fg='#d77337',
                   font=('Georgia', 20))
        title_label.grid(row=0, column=1, columnspan=2, pady=10)

        # Button to calculate BMI
        bmi_button = Button(health_calculator_frame, text="Calculate BMI", command=self.show_bmi_calculator,
                   compound="left", cursor='hand2', bg='old lace', fg='black', bd=0,
                   font=('Georgia', 15))
        bmi_button.place(x=100, y=100)

        # Button to calculate water requirements
        water_button = Button(health_calculator_frame, text="Calculate Water", command=self.show_water_calculator,
                     compound="left", cursor='hand2', bg='old lace', fg='black', bd=0,
                     font=('Georgia', 15))
        water_button.place(x=100, y=150)

        # Button to calculate nutrient content
        nutrient_button = Button(health_calculator_frame, text="Calculate Nutrients", command=self.show_nutrient_calculator,
                         compound="left", cursor='hand2', bg='old lace', fg='black',
                         bd=0, font=('Georgia', 15))
        nutrient_button.place(x=100, y=200)

        close_button = Button(health_calculator_window, text='Close', command=health_calculator_window.destroy, cursor='hand2',
                      bg='Red', fg='white', font=('Georgia', 15))
        close_button.place(x=100, y=300)


        

    def show_bmi_calculator(self):
        bmi_calculator_window = Toplevel(self.root)
        bmi_calculator_window.title("BMI Calculator")
        bmi_calculator_window.geometry('400x300+300+100')
       

        # Age entry
        age_label = Label(bmi_calculator_window, text="Age:", font=('Georgia', 15)).place(x=30, y=20)
        age_entry = Entry(bmi_calculator_window, font=('Georgia', 13))
        age_entry.place(x=160, y=20)

        # Height entry
        height_label = Label(bmi_calculator_window, text="Height (cm):", font=('Georgia', 15)).place(x=30, y=60)
        height_entry = Entry(bmi_calculator_window, font=('Georgia', 13))
        height_entry.place(x=160, y=60)

        # Weight entry
        weight_label = Label(bmi_calculator_window, text="Weight (kg):", font=('Georgia', 15)).place(x=30, y=100)
        weight_entry = Entry(bmi_calculator_window, font=('Georgia', 13))
        weight_entry.place(x=160, y=100)

        result_label = Label(bmi_calculator_window, text="", font=('Georgia', 15))
        result_label.place(x=30, y=250)

        calculate_button = Button( bmi_calculator_window, text="Calculate BMI", command=lambda: self.calculate_bmi_result(age_entry, height_entry, weight_entry, result_label), cursor='hand2',
                                  bg='#d77337', fg='white', bd=0, font=('Georgia', 15)).place(x=30, y=200)

        close= Button( bmi_calculator_window , text='Close', command=bmi_calculator_window.destroy, cursor='hand2', bg='Red',
                           fg='white',font=('Georgia', 15)).place(x=200, y=200)

   

    def calculate_bmi_result(self, age_entry, height_entry, weight_entry,result_label):
        try:
            age = int(age_entry.get())
            height = float(height_entry.get()) / 100
            weight = float(weight_entry.get())
              
            bmi_result = weight/height**2 # Placeholder value, replace with actual result
        
            if bmi_result<18.5:
                result_label.config(text=f"BMI Result: {bmi_result: .2f}Underweight")
            elif bmi_result>=18.5 and bmi_result<25:
                result_label.config(text=f"BMI Result: {bmi_result: .2f} Normal")
            elif  bmi_result>=25 and bmi_result<30:
                result_label.config(text=f"BMI Result: {bmi_result: .2f}Overweight")
            else:
                result_label.config(text=f"BMI Result: {bmi_result: .2f}Obeise")

        except ValueError:
            msg.showerror("Error","Please enter valid values for age, height, weight.")

    def show_water_calculator(self):
        water_calculator_window = Toplevel(self.root)
        water_calculator_window.title("Water Calculator")
        water_calculator_window.geometry('400x300+300+100')

        # Age entry
        age_label = Label(water_calculator_window, text="Enter your age:", font=('Georgia', 15))
        age_label.place(x=10, y=10)
        age_entry = Entry(water_calculator_window,width=10, font=('Georgia', 13))
        age_entry.place(x=250, y=10)

        # Weight entry
        weight_label = Label(water_calculator_window, text="Enter your weight (kg):", font=('Georgia', 15))
        weight_label.place(x=10, y=50)
        weight_entry = Entry(water_calculator_window, width=10, font=('Georgia', 13))
        weight_entry.place(x=250, y=50)

        # Activity dropdown
        activity_label = Label(water_calculator_window, text="Select your daily activity:", font=('Georgia', 15))
        activity_label.place(x=10, y=90)
        activity_options = ["Sedentary", "Light", "Moderate", "High", "Extreme"]
        activity_var = StringVar(water_calculator_window)
        activity_var.set(activity_options[0])  # Default selection
        activity_dropdown = OptionMenu(water_calculator_window, activity_var, *activity_options)
        activity_dropdown.place(x=250, y=90)

        self.result_label = Label(water_calculator_window, text="", font=('Georgia', 15))
        self.result_label.place(x=30, y=200)

        # Button to calculate water requirements
        calculate_button = Button(water_calculator_window, text="Calculate", command=lambda: self.calculate_water(age_entry.get(), weight_entry.get(), activity_var.get()), cursor='hand2',
                          bg='#d77337', fg='white', bd=0, font=('Georgia', 15))
        calculate_button.place(x=10, y=150)

        # Close button
        close_button = Button(water_calculator_window, text="Close", command=water_calculator_window.destroy, cursor='hand2',
                      bg='Red', fg='white', bd=0, font=('Georgia', 15))
        close_button.place(x=150, y=150)


    def calculate_water(self, age, weight, activity):
        # Simple water requirement calculation (example, you may need to refine this logic)
        try:
            age = float(age)
            weight = float(weight)
            activity_factor = {"Sedentary": 30, "Light": 35, "Moderate": 40, "High": 45, "Extreme": 50}
            water_requirement = weight * activity_factor.get(activity, 35) / 1000  # Assuming result in liters
            result_text = f"You need: {water_requirement:.2f} liters per day"
            self.result_label.config(text=result_text)  # Use self.result_label

        except ValueError:
            self.result_label.config(text="Please enter valid numeric values for age and weight.")
       
        

     
 #**********************************************************************************************************************************#       

    def show_nutrient_calculator(self):
        nutrient_calculator_window = Toplevel(self.root)
        nutrient_calculator_window.title("Nutrient Calculator")
        nutrient_calculator_window.geometry('400x400+300+100')

        nutrient_calculator_frame = Frame(nutrient_calculator_window, width=400, height=400, bg='honeydew2')
        nutrient_calculator_frame.pack()

        # Dropdown for selecting food
        label_food = Label(nutrient_calculator_frame, text='Select Food:', font=('Georgia', 15))
        label_food.place(x=10, y=10)

        food_items = list(self.nutrition_data.keys())
        self.combo_food = ttk.Combobox(nutrient_calculator_frame, values=food_items)
        self.combo_food.place(x=150, y=10)

        # Button to calculate nutrients
        button_calculate = Button(nutrient_calculator_frame, text='Calculate Nutrients', font=('Georgia', 14),
                          command=self.calculate_nutrients)
        button_calculate.place(x=100, y=100)

        # Close button
        button_close = Button(nutrient_calculator_frame, text='Close',  bg='Red', font=('Georgia', 14),
                      command=nutrient_calculator_window.destroy)
        button_close.place(x=150, y=350)

        # Result Display
        self.result_text = StringVar()
        label_result = Label(nutrient_calculator_frame, textvariable=self.result_text, font=('Georgia', 15))
        label_result.place(x=100, y=140)

    def load_nutrition_data(self):
        nutrition_data = {}
        try:
            with open('C:\\Rutu\\nutrition_data.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    food_name = row.get('Food_name', '').strip()  

                    nutrition_data[food_name] = {
                    'Serving_size': row.get('Serving_size (g) ', '').replace('(g)', '').strip(),
                    'Calories': row.get('Calories', '').replace('(g)', '').strip(),
                    'Fat': row.get('Fat (g)', '').replace('(g)', '').strip(),
                    'Fiber': row.get('Fiber (g)', '').replace('(g)', '').strip(),
                    'Carbohydrate': row.get('Carbohydrates (g)', '').replace('(g)', '').strip(),
                    'Protein': row.get('Proteins  (g)', '').replace('(g)', '').strip(),
                  
                       }
            return nutrition_data
        except FileNotFoundError:
           msg.showerror("File Not Found", "The nutrition data file (nutrition_data.csv) was not found.")
           return {}


    def calculate_nutrients(self):
        selected_food = self.combo_food.get()
        nutrient_info = self.nutrition_data.get(selected_food, {})
        
        if nutrient_info:
            result = f" {selected_food}:\n"
            for nutrient, value in nutrient_info.items():
                result += f"{nutrient}: {value} g\n"
            self.result_text.set(result)
        else:
            self.result_text.set("Nutrition information not available for selected food.")

 #**********************************************************************************************************************************#
        # WORLOUT_PLANS
        
    def show_exercise(self):
        exercise_window = Toplevel(self.root)
        exercise_window.title("Exercises")
        exercise_window.geometry('400x400+300+100')

        exercise_frame = Frame(exercise_window, width=380, height=380, bg='honeydew2')
        exercise_frame.pack()

        title = Label(exercise_frame, text='Exercises', bg='honeydew2', fg='#d77337', font=('Georgia', 30))
        title.place(x=80, y=20)

    # Assuming you have a list of workout plans
        excercise_plans = ["Exercises", "Yoga", "Surya_Namaskar"]

    # Create a Listbox to display workout plans
        exercise_listbox = Listbox(exercise_frame, selectmode=SINGLE, height=len(excercise_plans), font=('Georgia', 15))

        for plan in  excercise_plans:
            exercise_listbox.insert(END, plan)
        exercise_listbox.place(x=100, y=90, width=150, height=200)

    # Button to view selected workout plan
        view_button = Button(exercise_frame , text="View ",
                         command=lambda: self.view_exercise(exercise_listbox,  exercise_window),
                         cursor='hand2', bg='#d77337', fg='white', bd=0, font=('Georgia', 15)).place(x=50, y=330)

    # Close button
        close_button = Button( exercise_frame , text="Close", command= exercise_window.destroy, cursor='hand2',
                          bg='Red', fg='white', bd=0, font=('Georgia', 15)).place(x=200, y=330)

    def view_exercise(self, listbox, exercise_window):
        selected_index = listbox.curselection()
        if selected_index:
            selected_plan = listbox.get(selected_index)

        if selected_plan == "Exercises":
            self.show_advance_exercise( exercise_window)
        elif selected_plan == "Yoga":
            self.show_yoga( exercise_window)
        elif selected_plan == "Surya_Namaskar":
            self.show_surya_namaskar( exercise_window)

    def show_advance_exercise(self,  exercise_window):
        advance_exercise_frame = Toplevel( exercise_window)
        advance_exercise_frame.title('Exercise')
        advance_exercise_frame.geometry('350x400+250+100')

        # Create a Listbox to display exercise names
        exercise_listbox = tk.Listbox(advance_exercise_frame, selectmode=tk.SINGLE, height=10, font=('Georgia', 12))
        for exercise_name in self.exercise_data.keys():
            exercise_listbox.insert(tk.END, exercise_name)
        exercise_listbox.place(x=60, y=30)

    # Label to display exercise details
        details_label = tk.Label(advance_exercise_frame, text="", font=('Georgia', 12))
        details_label.place(x=80, y=280)

    # Button to view selected exercise details
        view_button = tk.Button(advance_exercise_frame, text="View Details", font=('Georgia', 12),
                            command=lambda: self.view_exercise_details(exercise_listbox, details_label))
        view_button.place(x=100, y=250)

    # Close button
        close_button = tk.Button(advance_exercise_frame, text="Close",bg='Red', font=('Georgia', 12),
                             command=advance_exercise_frame.destroy)
        close_button.place(x=100, y=350)

    def load_exercise_data(self):
        exercise_data = {}
        try:
            with open('C:\\Rutu\\fitness_exercise.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    exercise_name = row.get('Exercise_name', '').strip()

                    exercise_data[exercise_name] = {
                        'BodyPart': row.get('BodyPart', '').strip(),
                        'Equipment': row.get('Equipment', '').strip(),
                        'Target': row.get('Target', '').strip(),
                    }
            return exercise_data
        except FileNotFoundError:
            tk.messagebox.showerror("File Not Found", "The exercise data file (fitness_exercise.csv) was not found.")
            return {}

    def view_exercise_details(self, listbox, details_label):
        selected_index = listbox.curselection()
        if selected_index:
            selected_exercise = listbox.get(selected_index)
            details = self.exercise_data.get(selected_exercise, {})
            details_text = "\n".join([f"{key}: {value}" for key, value in details.items()])
            details_label.config(text=details_text)

#*********************************************************************************************************************************#        
    
    def show_yoga(self,  exercise_window):
        yoga_frame = Toplevel( exercise_window)
        yoga_frame.title('Yoga')
        yoga_frame.geometry('550x500+300+100')

        # Load the first image
        image_path1 = 'F:\\New\\yogapose1.png'
        img1 = PhotoImage(file=image_path1)
        image_label1 = Label(yoga_frame, image=img1, bg='white')
        image_label1.image = img1
        image_label1.place(x=30, y=20)  

    # Load the second image
        image_path2 =  'F:\\New\\yogapose1.png'
        img2 = PhotoImage(file=image_path2)
        image_label2 = Label(yoga_frame, image=img2, bg='white')
        image_label2.image = img2
        image_label2.place(x=30, y=180)  

    # Load the third image
        image_path3 =  'F:\\New\\yogapose1.png'
        img3 = PhotoImage(file=image_path3)
        image_label3 = Label(yoga_frame, image=img3, bg='white')
        image_label3.image = img3
        image_label3.place(x=30, y=300)  

   
        b6= Button( yoga_frame , text="Close", command= yoga_frame.destroy, cursor='hand2',
                          bg='Red', fg='white', bd=0, font=('Georgia', 15)).place(x=250, y=460)

#*********************************************************************************************************************************#                
    def show_surya_namaskar(self,  exercise_window):
        surya_namaskar_frame = Toplevel( exercise_window)
        surya_namaskar_frame.title('Surya Namaskar')
        surya_namaskar_frame.geometry('650x630+300+100')


         # Load the first image
        image_path1 =  'F:\\New\\surya1.png'
        img1 = PhotoImage(file=image_path1)
        image_label1 = Label( surya_namaskar_frame, image=img1, bg='white')
        image_label1.image = img1
        image_label1.place(x=20, y=20)  

    # Load the second image
        image_path2 ='F:\\New\\surya2.png'
        img2 = PhotoImage(file=image_path2)
        image_label2 = Label( surya_namaskar_frame, image=img2, bg='white')
        image_label2.image = img2
        image_label2.place(x=350, y=20)  

    # Load the third image
        image_path3 =   'F:\\New\\surya3.png'
        img3 = PhotoImage(file=image_path3)
        image_label3 = Label( surya_namaskar_frame, image=img3, bg='white')
        image_label3.image = img3
        image_label3.place(x=20, y=130)  

         # Load the first image
        image_path4 = 'F:\\New\\surya4.png'
        img4 = PhotoImage(file=image_path4)
        image_label4 = Label( surya_namaskar_frame, image=img4, bg='white')
        image_label4.image = img4
        image_label4.place(x=350, y=130)  

    # Load the second image
        image_path12 =  'F:\\New\\surya5.png'
        img12 = PhotoImage(file=image_path12)
        image_label12 = Label( surya_namaskar_frame, image=img12, bg='white')
        image_label12.image = img12
        image_label12.place(x=20, y=210)  

    # Load the third image
        image_path5 = 'F:\\New\\surya6.png'
        img5 = PhotoImage(file=image_path5)
        image_label5 = Label( surya_namaskar_frame, image=img5, bg='white')
        image_label5.image = img5
        image_label5.place(x=350, y=210)  

         # Load the first image
        image_path6 =  'F:\\New\\surya7.png'
        img6 = PhotoImage(file=image_path6)
        image_label6 = Label( surya_namaskar_frame, image=img6, bg='white')
        image_label6.image = img6
        image_label6.place(x=20, y=310)  

    # Load the second image
        image_path7 =   'F:\\New\\surya8.png'
        img7 = PhotoImage(file=image_path7)
        image_label7 = Label( surya_namaskar_frame, image=img7, bg='white')
        image_label7.image = img7
        image_label7.place(x=350, y=310)  

    # Load the third image
        image_path8 =   'F:\\New\\surya9.png'
        img8 = PhotoImage(file=image_path8)
        image_label8 = Label( surya_namaskar_frame, image=img8, bg='white')
        image_label8.image = img8
        image_label8.place(x=20, y=410)

         # Load the first image
        image_path9 ='F:\\New\\surya10.png'
        img9 = PhotoImage(file=image_path9)
        image_label9 = Label( surya_namaskar_frame, image=img9, bg='white')
        image_label9.image = img9
        image_label9.place(x=350, y=410)  

    # Load the second image
        image_path10 =   'F:\\New\\surya11.png'
        img10 = PhotoImage(file=image_path10)
        image_label0 = Label( surya_namaskar_frame, image=img10, bg='white')
        image_label0.image = img10
        image_label0.place(x=20, y=510)  

    # Load the third image
        image_path11 =  'F:\\New\\surya12.png'
        img11 = PhotoImage(file=image_path11)
        image_label1 = Label( surya_namaskar_frame, image=img11, bg='white')
        image_label1.image = img11
        image_label1.place(x=350, y=510)  

   
        b7= Button(surya_namaskar_frame  , text="Close", command= surya_namaskar_frame.destroy, cursor='hand2',
                          bg='Red', fg='white', bd=0, font=('Georgia', 15)).place(x=300, y=610)
        
        
    def close_homepage(self):
        if self.home_page_window:
            self.home_page_window.destroy()

     
    def close_login_window(self):
        if self.login_window:
            self.login_window.destroy()


# Create the main Tkinter window
root = Tk()
ob = HealthFitnessApp(root)
root.mainloop()
