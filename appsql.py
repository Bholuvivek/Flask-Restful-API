from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "margedarshan"

mysql = MySQL(app)


@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM course")
    fetchdata = cur.fetchall()
    return render_template('index.html', data=fetchdata)

@app.route('/', methods=['POST'])
def addcourse():
    if request.method == 'POST':
        course_id = request.form['courseid']
        course_name = request.form['title']
        course_description = request.form['description']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `course` (`id`, `course`, `course_description`) VALUES (%s,%s, %s)",
                    (course_id, course_name, course_description))
        mysql.connection.commit()

        return redirect(url_for('index'))



@app.route('/updatecourse', methods=['GET', 'POST'])
def updatecourse():
    if request.method == 'POST':
        new_course_id = request.form['courseid']
        new_course_name = request.form['title']
        new_course_description = request.form['description']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE `course` SET `id`= %s, `course` = %s, `course_description` = %s WHERE `id` = %s",
                    (new_course_id,new_course_name, new_course_description))
        mysql.connection.commit()

        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `course` WHERE `id` = %s", (id,))
    course = cur.fetchone()

    return render_template('index.html', course=course)

@app.route('/deletecourse', methods=['GET', 'POST'])
def deletecourse(id):
    if request.method == 'POST':
        id = request.form['courseid']
        cur = mysql.connection.cursor()
    
        cur.execute("DELETE FROM `course` WHERE `id` = %s",
                     (id,))
        mysql.connection.commit()

        return redirect('index.html')




if __name__ == "__main__":
    app.run(debug=True)
