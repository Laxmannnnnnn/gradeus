from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'school_management'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
        return jsonify(students)
    elif request.method == "POST":
        data = request.json
        name = data['name']
        email = data['email']
        phone = data['phone']
        address = data['address']
        dob = data['dob']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO students (name, email, phone, address, dob) VALUES (%s, %s, %s, %s, %s)",
            (name, email, phone, address, dob)
        )
        mysql.connection.commit()
        return jsonify({"message": "Student added successfully"}), 201

@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT students.name, attendance.date, attendance.status
            FROM attendance
            JOIN students ON attendance.student_id = students.student_id
        """)
        attendance_records = cur.fetchall()
        return jsonify(attendance_records)
    elif request.method == "POST":
        data = request.json
        student_id = data['student_id']
        date = data['date']
        status = data['status']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
            (student_id, date, status)
        )
        mysql.connection.commit()
        return jsonify({"message": "Attendance recorded successfully"}), 201

@app.route("/grades", methods=["GET", "POST"])
def grades():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT students.name, subjects.name AS subject, grades.grade, grades.assessment_type
            FROM grades
            JOIN students ON grades.student_id = students.student_id
            JOIN subjects ON grades.subject_id = subjects.subject_id
        """)
        grades_records = cur.fetchall()
        return jsonify(grades_records)
    elif request.method == "POST":
        data = request.json
        student_id = data['student_id']
        subject_id = data['subject_id']
        grade = data['grade']
        assessment_type = data['assessment_type']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO grades (student_id, subject_id, grade, assessment_type) VALUES (%s, %s, %s, %s)",
            (student_id, subject_id, grade, assessment_type)
        )
        mysql.connection.commit()
        return jsonify({"message": "Grade added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
