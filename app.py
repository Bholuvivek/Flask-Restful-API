from flask import Flask, jsonify, request, render_template
import sqlite3
from flask_mysqldb import MySQL



app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "margedarshan"

# Function to create a new connection to the SQLite database
def get_db_connection():
    return sqlite3.connect('courses.db')

# Create a SQLite database file and define a courses table
conn = sqlite3.connect('courses.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses')
        courses = cursor.fetchall()
        conn.close()
        return jsonify(courses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
        course = cursor.fetchone()
        conn.close()

        if course:
            return jsonify(course)
        else:
            return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/course', methods=['POST'])
def create_course():
    data = request.get_json()
    if 'title' in data and 'description' in data:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO courses (title, description) VALUES (?, ?)', (data['title'], data['description']))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Course created successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Title and description are required'}), 400

@app.route('/course/<int:course_id>', methods=['PUT', 'DELETE'])
def update_or_delete_course(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
        course = cursor.fetchone()

        if not course:
            conn.close()
            return jsonify({'error': 'Course not found'}), 404

        if request.method == 'PUT':
            data = request.get_json()
            cursor.execute('UPDATE courses SET title=?, description=? WHERE id=?',
                           (data['title'], data['description'], course_id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Course updated successfully'})

        elif request.method == 'DELETE':
            cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Course deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
