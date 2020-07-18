import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

# create Student


@app.route('/create', methods=['POST'])
def create_student():
    try:
        _json = request.json
        _roll_no = _json['roll_no']
        _first_name = _json['first_name']
        _last_name = _json['last_name']
        _class = _json['class']
        _age = _json['age']
        _address = _json['address']
        _status = _json['status']

        # insert record in database
        sqlQuery = "INSERT INTO student(roll_no, first_name, last_name, class, age, address, status) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        data = (_roll_no, _first_name, _last_name,
                _class, _age, _address, _status,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sqlQuery, data)
        conn.commit()
        res = jsonify('Student created successfully.')
        res.status_code = 200

        return res

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/student')
def student():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200

        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/student/<int:student_id>')
def get_student(student_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM student WHERE id=%s", student_id)
        row = cursor.fetchone()
        res = jsonify(row)
        res.status_code = 200

        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['PUT'])
def update_student():
    try:
        _json = request.json
        _student_id = _json['id']
        _first_name = _json['first_name']
        _last_name = _json['last_name']
        _class = _json['class']
        _age = _json['age']
        _address = _json['address']

        # update record in database
        sql = "UPDATE student SET first_name=%s, last_name=%s, class=%s, age=%s, address=%s WHERE id=%s"
        data = (_first_name, _last_name, _class,
                _age, _address, _student_id,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        res = jsonify('Student updated successfully.')
        res.status_code = 200

        return res

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# delete student record from database


@app.route('/delete/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id=%s", (student_id,))
        conn.commit()
        res = jsonify('Student deleted successfully.')
        res.status_code = 200
        return res

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@ app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'There is no record: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 404

    return res


@app.route('/login', methods=['POST'])
def login():
    try:
        _json = request.json
        _login = _json['login']
        _password = _json['password']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM user where login = %s and password = %s"
        data = (_login, _password)
        cursor.execute(sqlQuery, data)
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200

        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(port=3000)
