import sqlite3
from flask import Flask, jsonify, request
import os
from flask_cors import CORS 

app = Flask(__name__)

CORS(app)

def get_db_connection():
    db_dir = 'backend/db'
    db_file = 'appointments.db'

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)  

    conn = sqlite3.connect(os.path.join(db_dir, db_file))
    conn.row_factory = sqlite3.Row  
    return conn


def init_db():
    conn = get_db_connection() 
    conn.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# slots
available_slots = [
    "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM",
    "12:30 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
    "04:00 PM", "04:30 PM"
]

# routes
@app.route('/')
def home():
    return "Welcome to the Appointment Booking System!"

@app.route('/api/slots', methods=['GET'])
def get_available_slots():
    return jsonify(available_slots)

@app.route('/api/book', methods=['POST'])
def book_appointment():
    data = request.json
    name = data['name']
    phone = data['phone']
    date = data['date']
    time_slot = data['time_slot']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments WHERE time_slot = ? AND date = ?', (time_slot, date))
    existing_appointment = cursor.fetchone()

    if existing_appointment:
        conn.close()
        return jsonify({"error": "Slot already booked"}), 400

    cursor.execute('INSERT INTO appointments (name, phone, date, time_slot) VALUES (?, ?, ?, ?)',
                   (name, phone, date, time_slot))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Appointment booked successfully!"}), 200

if __name__ == '__main__':
    init_db() 
    app.run(debug=True)
