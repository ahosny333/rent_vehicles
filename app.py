# app.py
import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
os.environ.get("TOKEN_NAME","")
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST","localhost")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER","root") 
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD","") 
app.config['MYSQL_DB'] =  os.environ.get("MYSQL_DB","rent_cars") 

mysql = MySQL(app)

def not_found():

    resp = jsonify("NOT FOUND")
    resp.status_code = 404
    return resp

@app.route("/customers",methods=['GET'])
def get_customers():
    try:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM customers ')
            customer = cursor.fetchall()
            return jsonify(customer),200
    except Exception as e:
        # print(e)
        return not_found()
    finally:
        cursor.close()

@app.route("/customers/<id>",methods=['GET'])
def get_customer(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM customers WHERE custID=%s',id)
        customer = cursor.fetchone()
        return jsonify(customer),200
    except Exception as e:
        # print(e)
        return not_found()
    finally:
        cursor.close()

@app.route("/customers",methods=['POST'])
def add_customer():
    try:
        if not request.is_json:
            return {"error": "Request must be JSON"}, 415
        request_params = request.json
        fname = request_params['first_name']
        lname = request_params['last_name']
        contact_no = request_params['contact_no']
        driving_licence = request_params['driving_licence']
        if fname and lname and contact_no and driving_licence:
            sql = "INSERT INTO customers(first_name,last_name,contact_no,driving_licence) VALUES(%s,%s,%s,%s)"
            data = (fname,lname,contact_no,driving_licence)
            cursor = mysql.connection.cursor()
            cursor.execute(sql,data)
            mysql.connection.commit()
            return jsonify(data),200
        else:
            return not_found()
    except:
        return not_found()
    finally:
        cursor.close()


@app.route("/customers/<id>",methods=['PUT'])
def update_customer(id):
    try:
        if not request.is_json:
            return {"error": "Request must be JSON"}, 415
        request_params = request.json
        fname = request_params['first_name']
        lname = request_params['last_name']
        contact_no = request_params['contact_no']
        driving_licence = request_params['driving_licence']
        if fname and lname and contact_no and driving_licence:
            sql = "UPDATE customers SET first_name = %s,last_name = %s,contact_no=%s,driving_licence=%s WHERE custID= %s"
            data = (fname,lname,contact_no,driving_licence,id)
            cursor = mysql.connection.cursor()
            cursor.execute(sql,data)
            mysql.connection.commit()
            return jsonify(data),200
        else:
            return not_found()
    except Exception as e:
        print(e)
        return not_found()
    finally:
        cursor.close()

@app.route("/customers/<id>",methods=['DELETE'])
def delete_customer(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM customers where custID=%s',(id,))
        mysql.connection.commit()
        resp = jsonify('customer deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        # print(e)
        return not_found()
    finally:
        cursor.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)