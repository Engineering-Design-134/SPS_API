from flask import Flask, request
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

if os.getenv("ENV") == "dev":
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'sps_db'
else:
    app.config['MYSQL_HOST'] = os.getenv("HOST")
    app.config['MYSQL_USER'] = os.getenv("USERNAME")
    app.config['MYSQL_PASSWORD'] = os.getenv("PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("DB")

mysql = MySQL(app)

@app.route('/device_on', methods=['PATCH'])
def device_on():
    cursor = mysql.connection.cursor()
    device_id = request.json['device_id']
    device_on = request.json['device_on']
    cursor.execute(
        "UPDATE device_settings SET device_on = %s WHERE device_id = %s",
        (device_on, device_id))
    mysql.connection.commit()
    cursor.close()
    return 'success'

@app.route('/settings', methods=['GET', 'POST', "PATCH"])
def settings():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        device_id = request.json['device_id']
        vibration_strength = request.json['vibration_strength']
        flex_sensitivity = request.json['flex_sensitivity']
        vibration_duration = request.json['vibration_duration']
        cursor.execute(
            "INSERT INTO device_settings(device_id, vibration_strength, flex_sensitivity, vibration_duration, device_on) VALUES (%s, %s, %s, %s, %s)",
            (device_id, vibration_strength, flex_sensitivity, vibration_duration, 0))
        mysql.connection.commit()
        cursor.close()
        return 'success'

    if request.method == 'GET':
        device_id = request.args["device_id"]
        cursor.execute(
            "SELECT * FROM device_settings WHERE device_id = %s",
            (device_id,))
        device_settings = cursor.fetchone()
        cursor.close()
        json = ('{"device_id": "%s", "vibration_strength": "%s", "flex_sensitivity": "%s", "vibration_duration": "%s", "device_on": "%s"}')
        print(json % device_settings)
        return json % device_settings

    if request.method == 'PATCH':
        device_id = request.json['device_id']
        vibration_strength = request.json['vibration_strength']
        flex_sensitivity = request.json['flex_sensitivity']
        vibration_duration = request.json['vibration_duration']
        cursor.execute(
            "UPDATE device_settings SET vibration_strength = %s, flex_sensitivity = %s, vibration_duration = %s WHERE device_id = %s",
            (vibration_strength, flex_sensitivity, vibration_duration, device_id))
        mysql.connection.commit()
        cursor.close()
        return 'success'


if __name__ == '__main__':
    app.run()
