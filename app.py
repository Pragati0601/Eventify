from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = "eventify_secret_key_2026"


# =========================
# DATABASE
# =========================

def create_database():

    conn = sqlite3.connect("eventify.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Event registrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            event TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_database()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# EVENTS
# =========================

@app.route("/events")
def events():
    return render_template("events.html")


# =========================
# CALENDAR
# =========================

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")


# =========================
# COMMUNITY
# =========================

@app.route("/community")
def community():
    return render_template("community.html")


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():
    return render_template("about.html")

# =========================
# CONTACT
# =========================

@app.route("/contact")
def contact():
    return render_template("contact.html")

# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_email = session.get("user_email")

    conn = sqlite3.connect("eventify.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, email, phone, event
        FROM event_registrations
        WHERE email = ?
    """, (user_email,))

    registered_events = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        registered_events=registered_events
    )

# =========================
# EVENT DETAILS
# =========================

@app.route("/event-details")
def event_details():

    event = request.args.get("event", "music")

    events = {

        "music": {
            "name": "Music Festival",
            "date": "15 October 2026",
            "time": "6:00 PM - 10:00 PM",
            "location": "Kolhapur",
            "organizer": "Eventify Team",
            "seats": "100",
            "icon": "🎤"
        },

        "tech": {
            "name": "Tech Conference",
            "date": "20 October 2026",
            "time": "10:00 AM - 4:00 PM",
            "location": "Pune",
            "organizer": "Eventify Team",
            "seats": "150",
            "icon": "💻"
        },

        "creative": {
            "name": "Creative Workshop",
            "date": "25 October 2026",
            "time": "11:00 AM - 3:00 PM",
            "location": "Mumbai",
            "organizer": "Eventify Team",
            "seats": "50",
            "icon": "🎨"
        },

        "sports": {
            "name": "Sports Tournament",
            "date": "30 October 2026",
            "time": "9:00 AM - 5:00 PM",
            "location": "Kolhapur",
            "organizer": "Eventify Team",
            "seats": "200",
            "icon": "🏆"
        }
    }

    selected_event = events.get(event)

    if selected_event is None:
        event = "music"
        selected_event = events["music"]

    return render_template(
        "event-details.html",
        event=selected_event,
        event_key=event
    )


# =========================
# EVENT REGISTRATION
# =========================

@app.route("/register-event", methods=["GET", "POST"])
def register_event():

    events = {
        "music": "Music Festival",
        "tech": "Tech Conference",
        "creative": "Creative Workshop",
        "sports": "Sports Tournament"
    }

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        event_name = request.form["event"]

        conn = sqlite3.connect("eventify.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO event_registrations
            (name, email, phone, event)
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, event_name))

        conn.commit()
        conn.close()

        return "Event Registration Successful!"

    event = request.args.get("event", "music")

    event_name = events.get(event, "Music Festival")

    return render_template(
        "register-event.html",
        event_name=event_name
    )


# =========================
# ACCOUNT REGISTRATION
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        conn = sqlite3.connect("eventify.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users
            (name, email, phone, password)
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, password))

        conn.commit()
        conn.close()

        return "Registration Successful!"

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("eventify.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email
            FROM users
            WHERE email = ? AND password = ?
        """, (email, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_email"] = user[2]

            return redirect(url_for("dashboard"))

        else:

            return "Invalid Email or Password!"

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)