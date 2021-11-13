from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
import email_validator
from wtforms.validators import Length, EqualTo, Email, Required
from passlib.handlers.sha2_crypt import sha256_crypt
import database_script
import number_crypt
import os

class RegisterationForm(FlaskForm):
    username = StringField('User Name: ', validators = [Required(), Length(min=2, max=50)])
    email = StringField('Email Address: ', validators = [Required(), Email()])
    confirm_password = PasswordField('Confirm Password: ', validators=[Required()])
    password = PasswordField('Password: ', validators = [Required(), Length(min=6), EqualTo('confirm_password')])
    submit = SubmitField("Sign Up")

class SigninForm(FlaskForm):
    signin_username = StringField('Username: ', validators = [Required(), Length(min=2, max=50)])
    signin_password = PasswordField('Password: ', validators = [Required(), Length(min=6)])
    submit = SubmitField("Sign In")

class searchForm(FlaskForm):
    search = StringField('Filter: ', validators = [Required(), Length(max=20)])
    submit = SubmitField("Filter")

app = Flask(__name__)
app.config["SECRET_KEY"] = 'b273ea4c91d118774f716248'
username = ""
user_level = 0

drone_image_list=["3D_Robotics_Solo.jpg", "DJI_Inspire_1_Pro.jpg", "DJI_Mavic_2_Pro.jpg"
            , "DJI_Matrice_200.jpg", "DJI_Mavic_2_Zoom.jpg", "DJI_Mavic_Air.jpg"
            , "DJI_Mavic_Pro.jpg", "DJI_Phantom_3_Professional.jpg", "DJI_Phantom_4.jpg"
            , "DJI_Spreading_Wings-S900.jpg", "Flyability_Elios_Drone.jpg", "Yuneec_H520.jpg"
            , "Yuneec_Mantis_Q.jpg"]

drone_image_list = []

drone_name_list = []
drone_buy_link_list = []
drone_list = []
drone_info_lst = []

with open("Files/static/drone_info.txt", "r") as drone_info:
    drone_info_str = drone_info.read()
    info_lst = drone_info_str.split(',')

for info in info_lst:
    info = info.split("-")
    drone_info_lst.append(info)

file_dir = os.listdir("Files/static/images/Drone_Images")

for item in file_dir:
    drone_image_list.append(item)

for image in drone_image_list:
    drone_name_list.append(image.replace("_", " ")[:-4])
    drone_buy_link_list.append("https://www.amazon.in/s?k=" + image.replace("_", "+")[:-4] + "+Drone")

for image, name, link, info, number in zip(drone_image_list, drone_name_list, drone_buy_link_list, drone_info_lst, range(0, len(drone_name_list))):
    drone_list.append([image, name, link, info, number])

@app.route('/')
def home_start():
    return redirect(url_for("home", num_key = "false", wishlist = "false"))

@app.route('/home/<num_key>/<wishlist>')
def home(num_key, wishlist):
    verify = ""
    rows = database_script.view_userinfo()

    for row in rows:
        if number_crypt.encrypt(str(row[0])) == num_key:
            num_key = str(row[0])

    for row in rows:
        if str(row[0]) == num_key:
            verify = "verified"

    if verify == "verified":
            return render_template("home.html", num_key = number_crypt.encrypt(num_key), wishlist = wishlist)
    else:
        return render_template("home.html", num_key = "false", wishlist = "false")

@app.route('/register', methods=["POST", "GET"])
def register():
    database_script.dosomething("CREATE TABLE IF NOT EXISTS userinfo (id INTEGER PRIMARY KEY, username Text, email TEXT, password TEXT, wishlist TEXT)")
    register_form = RegisterationForm()
    errors_lst = []
    user_to_create = {"Username": "", "Email": "", "Schoolname": "", "Password": ""}
    registration_complete_html = ["", ""]
    rows = database_script.view_userinfo()
    num_key = "false"

    if register_form.validate_on_submit():

        user_to_create = {"Username": register_form.username.data, "Email": register_form.email.data, "Password": sha256_crypt.encrypt(register_form.password.data)}

        if rows != [] and rows != None:
            for row in rows:
                if user_to_create["Username"] == row[1]:
                    errors_lst.append("Username: This username is already taken. Please write a different one.")
            
        if len(errors_lst) == 0:                                                              
            registration_complete_html = ["Congratulations! You have registered successfully. Now let's get your favourite drone from our products page!!!Happy Droning", "Go to Products"]   
            user_to_create_command_str = "INSERT INTO userinfo VALUES(NULL, '%s', '%s', '%s', '')" % (user_to_create["Username"], user_to_create["Email"], user_to_create["Password"])
            database_script.dosomething(user_to_create_command_str)
            rows = database_script.view_userinfo()
            for row in rows:
                if user_to_create["Username"] == str(row[1]):
                    num_key = row[0]
            
    if register_form.errors != {}:
        for error_msg, field_name in zip(register_form.errors.values(), register_form.errors.keys()):
            errors_lst.append(field_name[0].upper() + field_name[1:] + ": " + error_msg[0])

    return render_template("register.html", register_form = register_form, errors_lst = errors_lst, registration_complete_text = registration_complete_html[0], registration_complete_button = registration_complete_html[1], num_key = number_crypt.encrypt(num_key), wishlist = "false")

@app.route('/login', methods=["POST", "GET"])
def signin():
    error_text = ""
    rows = database_script.view_userinfo()
    signin_form = SigninForm()

    if signin_form.validate_on_submit():
        signin_input = [signin_form.signin_username.data, signin_form.signin_password.data]
        for row in rows:
            if row[1] == signin_input[0]:
                if sha256_crypt.verify(signin_input[1], row[3]):
                    wishlist = row[4]
                    if wishlist == "":
                        wishlist = "false"
                    return redirect(url_for('home', num_key = number_crypt.encrypt(str(row[0])), wishlist = wishlist))

        error_text = "Wrong username or password entered. Please try again."
        
    return render_template("login.html", signin_form=signin_form, error_text = error_text, num_key = "false", wishlist = "false")

@app.route('/signout')
def signout():
    signout_text = ["Signed Out", "You have been signout. Please signin again to view your wishlist.", "Go home"]
    return render_template("signout.html", num_key = "false", signout_text = signout_text, wishlist = "false")

@app.route('/wishlist/<num_key>/<wishlist>', methods=["POST", "GET"])
def wishlist(num_key, wishlist):    
    username = "username"
    rows = database_script.view_userinfo()
    for row in rows:
        if number_crypt.encrypt(str(row[0])) == num_key:
            num_key = str(row[0])

    for row in rows:
        if str(row[0]) == str(num_key):
            username = row[1]

    if wishlist != "false":
        if wishlist.find("false-") == -1:
            wishlist = wishlist
        else:
            wishlist[6:]

        wishlist_update_command_str = "UPDATE userinfo SET wishlist='%s' WHERE id=%s" % (wishlist, num_key)
        database_script.dosomething(wishlist_update_command_str)

        drone_display_lst = []
        wishlist_str = str(wishlist)
        wishlist_lst = wishlist_str.split("-")
        for item in wishlist_lst:
            if item != "false":
                drone_display_lst.append(drone_list[int(item)])

        return render_template("wishlist.html", num_key = number_crypt.encrypt(num_key), wishlist = wishlist, drone_list = drone_display_lst, username = username)
    else:
        return render_template("wishlist.html", num_key = number_crypt.encrypt(num_key), wishlist = wishlist, drone_list = [], username = username)

@app.route('/products/<num_key>/')
def products_error(num_key):
    verify = ""
    rows = database_script.view_userinfo()
    
    for row in rows:
        if number_crypt.encrypt(str(row[0])) == num_key:
            num_key = str(row[0])

    for row in rows:
        if str(row[0]) == num_key:
            verify = "verified"

    if verify == "verified":
        return redirect(url_for("products", num_key = number_crypt.encrypt(num_key), wishlist = "false"))
    else:
        return redirect(url_for("products", num_key = "false", wishlist = "false"))

@app.route('/products/<num_key>/<wishlist>', methods=['GET', 'POST'])
def products(num_key, wishlist):
    search_form = searchForm()
    search_form_list = []
    drone_display_list = []
    lst = []
    error = ""

    rows = database_script.view_userinfo()
    for row in rows:
        if number_crypt.encrypt(str(row[0])) == num_key:
            num_key = str(row[0])

    if wishlist != "false":
        wishlist_update_command_str = "UPDATE userinfo SET wishlist='%s' WHERE id=%s" % (wishlist, num_key)
        database_script.dosomething(wishlist_update_command_str)

    drone_display_list = drone_list

    if search_form.validate_on_submit and search_form.search.data != None:
        drone_display_list = []
        for name in drone_name_list:
            lst = []
            for pos, letter in enumerate(name):
                if search_form.search.data.lower()[0] == letter.lower():
                    lst.append(pos)
            for pos in lst:
                    string = str(name[pos:pos + len(search_form.search.data)])
                    if string.lower() == search_form.search.data.lower():
                        x = 0
                        if search_form_list != []:
                            for item in search_form_list:
                                if item != name:
                                    x = x+1
                        if x == len(search_form_list):
                            search_form_list.append(name)

        for name in search_form_list:
            for drone in drone_list:
                if drone[1] == name:
                    drone_display_list.append(drone)

        if drone_display_list == []:
            error = "Sorry, we don't have this product. We appreciate your feedback and will try to add it in future."

    rows = database_script.view_userinfo()
    for row in rows:
        if row[0] == num_key:
            wishlist = row[4]

    if wishlist != "false":
        wishlist = wishlist
    else:
        wishlist="false"

    return render_template("products.html", drone_list=drone_display_list, search_form = search_form, error=error, num_key = number_crypt.encrypt(num_key), wishlist = wishlist)
    
@app.errorhandler(404) 
def error_404(e):
    return render_template("404.html", num_key = "false", wishlist = "false")

if __name__ == "__main__":
    app.run(debug=True)