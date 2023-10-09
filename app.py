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
    app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
    app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

mysql = MySQL(app)


@app.route('/settings', methods=['GET', 'POST', "PATCH"])
def settings():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        device_id = request.json['device_id']
        vibration_strength = request.json['vibration_strength']
        flex_sensitivity = request.json['flex_sensitivity']
        cursor.execute(
            "INSERT INTO device_settings(device_id, vibration_strength, flex_sensitivity) VALUES (%s, %s, %s)",
            (device_id, vibration_strength, flex_sensitivity))
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
        json = '{"device_id": "%s", "vibration_strength": "%s", "flex_sensitivity": "%s"}'
        return json % device_settings

    if request.method == 'PATCH':
        device_id = request.json['device_id']
        vibration_strength = request.json['vibration_strength']
        sensor_sensitivity = request.json['sensor_sensitivity']
        cursor.execute(
            "UPDATE device_settings SET vibration_strength = %s, sensor_sensitivity = %s WHERE device_id = %s",
            (vibration_strength, sensor_sensitivity, device_id))
        mysql.connection.commit()
        cursor.close()
        return 'success'


if __name__ == '__main__':
    app.run()
