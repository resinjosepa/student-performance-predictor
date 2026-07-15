from flask import Flask, render_template, request
import sqlite3
import pickle
app = Flask(__name__)
with open("random_forest.pkl", "rb") as file:
    model = pickle.load(file)

with open("label_encoders.pkl", "rb") as file:
    encoders = pickle.load(file)
# Login Page
@app.route("/")
def home():
    return render_template("login.html")
# Login Button
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return render_template("home.html")
    else:
        return "Invalid Username or Password"
# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO users(fullname, email, username, password)
        VALUES (?, ?, ?, ?)
        """, (fullname, email, username, password))
        connection.commit()
        connection.close()
        return """
        <h2>User Registered Successfully!</h2>
        <br>
        <a href="/">Go to Login</a>
        """
    return render_template("register.html")
@app.route("/home")
#Home page
def home_page():
    return render_template("home.html")
#dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "GET":
        return render_template("predict.html")

    # -------- Student Information --------
    school = request.form["school"]
    sex = request.form["sex"]
    age = int(request.form["age"])
    address = request.form["address"]

    # -------- Family Information --------
    Mjob = request.form["Mjob"]
    Fjob = request.form["Fjob"]
    reason = request.form["reason"]
    guardian = request.form["guardian"]

    # -------- Academic Information --------
    traveltime = int(request.form["traveltime"])
    studytime = int(request.form["studytime"])
    failures = int(request.form["failures"])

    schoolsup = request.form["schoolsup"]
    famsup = request.form["famsup"]
    paid = request.form["paid"]
    activities = request.form["activities"]
    nursery = request.form["nursery"]
    higher = request.form["higher"]
    internet = request.form["internet"]

    # -------- Lifestyle Information --------
    famrel = int(request.form["famrel"])
    freetime = int(request.form["freetime"])
    goout = int(request.form["goout"])
    Dalc = int(request.form["Dalc"])
    Walc = int(request.form["Walc"])
    health = int(request.form["health"])
    absences = int(request.form["absences"])

    # -------- Previous Grades --------
    G1 = int(request.form["G1"])
    G2 = int(request.form["G2"])

        # Encode categorical values
    school = encoders["school"].transform([school])[0]
    sex = encoders["sex"].transform([sex])[0]
    address = encoders["address"].transform([address])[0]
    Mjob = encoders["Mjob"].transform([Mjob])[0]
    Fjob = encoders["Fjob"].transform([Fjob])[0]
    reason = encoders["reason"].transform([reason])[0]
    guardian = encoders["guardian"].transform([guardian])[0]
    schoolsup = encoders["schoolsup"].transform([schoolsup])[0]
    famsup = encoders["famsup"].transform([famsup])[0]
    paid = encoders["paid"].transform([paid])[0]
    activities = encoders["activities"].transform([activities])[0]
    nursery = encoders["nursery"].transform([nursery])[0]
    higher = encoders["higher"].transform([higher])[0]
    internet = encoders["internet"].transform([internet])[0]

    student = [[
        school,
        sex,
        age,
        address,
        Mjob,
        Fjob,
        reason,
        guardian,
        traveltime,
        studytime,
        failures,
        schoolsup,
        famsup,
        paid,
        activities,
        nursery,
        higher,
        internet,
        famrel,
        freetime,
        goout,
        Dalc,
        Walc,
        health,
        absences,
        G1,
        G2
    ]]

    prediction = model.predict(student)

    return render_template(
        "result.html",
        prediction=round(prediction[0], 2)
    )
@app.route("/history")
def history():
    return "<h2>Prediction History (Coming Soon)</h2>"
@app.route("/logout")
def logout():
    return render_template("login.html")
# Run Flask
if __name__ == "__main__":
    app.run(debug=True)