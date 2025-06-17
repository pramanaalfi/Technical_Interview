from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = 'user'
mysql = MySQL(app)

@app.route('/user', methods=['GET', 'POST'])
def user():
  if request.method == 'GET':
    cursor = mysql.connection.cursor()
    #cursor.execute("SELECT * FROM DATA_USER")
    cursor.execute("SELECT nama, umur, alamat FROM DATA_USER") #tidak menampilkan user_id
    column_names = [i[0] for i in cursor.description]
    
    data=[]
    for row in cursor.fetchall():
      data.append(dict(zip(column_names,row)))
    
    cursor.close()
    return jsonify(data)
  
  elif request.method == 'POST':
    nama = request.json['nama']
    umur = request.json['umur']
    alamat = request.json['alamat']

    if not nama or not umur or not alamat:
      return jsonify({'error': 'data harus diisi semua'})

    try:
      umur = int(umur)
    except ValueError:
      return jsonify({'error': 'data umur harus diisi dengan angka'})
    
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO DATA_USER(nama, umur, alamat) VALUES (%s, %s, %s)"
    cursor.execute(sql,(nama, umur, alamat))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'data berhasil dimasukkan'})
  
@app.route('/updateuser', methods = ['PUT'])
def updateuser():
  if 'id' in request.args:
    user_id = request.args['id']
    data = request.get_json()
    cursor = mysql.connection.cursor()
    sql = "UPDATE data_user SET nama=%s, umur=%s, alamat=%s where user_id=%s"
    val = (data['nama'], data['umur'], data['alamat'], user_id)
    cursor.execute(sql,val)
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'data berhasil di perbaharui'})

@app.route('/deleteuser', methods=['DELETE'])
def deleteuser():
    if 'id' in request.args:
        user_id = request.args['id']
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM DATA_USER WHERE user_id=%s", (user_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'data berhasil dihapus'})
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=50, debug=True)