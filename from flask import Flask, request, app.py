from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Yeh frontend aur backend ko aapas mein baat karne ki ijazat deta hai

# Database setup karne ka function (Agar table nahi hoga toh ye khud bana dega)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            car_model TEXT NOT NULL,
            service_type TEXT NOT NULL,
            book_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Jab server start ho, database initialize kar do
init_db()

# API route jo frontend se booking data receive karega
@app.route('/api/book', methods=['POST'])
def book_service():
    data = request.json
    
    name = data.get('name')
    phone = data.get('phone')
    car_model = data.get('carModel')
    service_type = data.get('serviceType')
    book_date = data.get('bookDate')
    
    # Data ko SQLite Database mein save karna
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, phone, car_model, service_type, book_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, phone, car_model, service_type, book_date))
    conn.commit()
    conn.close()
    
    print(f"New Booking Saved -> Name: {name}, Car: {car_model}, Date: {book_date}")
    
    return jsonify({"status": "success", "message": "Booking successfully saved to server database!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)