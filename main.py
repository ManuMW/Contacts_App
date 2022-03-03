from flask import Flask, session, render_template, redirect, url_for, request
from utils.db_utils import write_to_database, read_from_database
from datetime import timedelta


# declaring and configuring FLask
app = Flask(__name__)
app.secret_key = 'ILikeProgramming'

# Secret key used for Signing up
secret_pass_key = "ILikeProgramming"

# Creating session
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=50)

# Checking whether the session is still active
@app.route('/', methods=['GET','POST'])
def index():
    if "username" in session:
        return render_template("/UpdateForm.html")
    return render_template("SignIn.html")

# Loading Signup page
@app.route('/SignUp', methods=['GET'])
def register_page():

    return render_template("/SignUp.html")

# Fetching data from SignUp page and writing it to our database
@app.route('/SignUp', methods=['POST'])
def register_user():
    email = request.form['UpEmail']
    passw = request.form['UpPassword']
    user_secret_key = request.form['UpSecretKey']

    result = read_from_database(f"SELECT email FROM user WHERE email='{email}'")

    if result != email and user_secret_key == secret_pass_key: # Checking whether the same email is present
        write_to_database(f"INSERT INTO user (email, password) VALUES ('{email}', '{passw}') ;")
        return render_template("SignIn.html")
    return "Failed to register"

# Loading SignIn page
@app.route('/SignIn', methods=['GET'])
def signin_page():
    return render_template("/SignIn.html")

# Fetching data from SignIn page and logging in to UpdateFormPage
@app.route('/SignIn', methods=['POST', 'GET'])
def login():
    email = request.form['InEmail']
    passw = request.form['InPass']

    result = read_from_database(f" SELECT * FROM user WHERE email='{email}' AND password='{passw}'")
    if len(result) == 0:
        return "Invalid Login Credentials"
    else:
        user = result[0][1]
        session["username"] = user
        return redirect(url_for("username"))

# To display the Contacts of the current user logged in
@app.route('/UpdateForm', methods=['GET'])
def username():
    if "username" in session:
        user = session["username"]
        headings = ("Name", "Email", "Phone Number")
        data = read_from_database(f"SELECT contact_name, contact_email, contact_phone FROM mycontacts WHERE id_refer = (SELECT id FROM user WHERE email='{user}');")
        return render_template('/UpdateForm.html', headings = headings, data = data)
    return "Session expired"

# To update the contact list
@app.route('/UpdateForm', methods=['POST'])
def updatecontacts():
    email = request.form['UEmail']
    name = request.form['UName']
    ph_number = request.form['UNumber']

    if 'username' in session:
        user = session["username"]

        user_id = read_from_database(f"SELECT id FROM user WHERE email='{user}'")
        id_user = user_id[0][0]

        write_to_database(f"INSERT INTO mycontacts( contact_name, contact_email, contact_phone, id_refer) VALUES ('{name}','{email}', '{ph_number}', '{id_user}')")
        return redirect(url_for('username'))

    return "Fail"

# Logging out
@app.route("/LogOut",)
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)