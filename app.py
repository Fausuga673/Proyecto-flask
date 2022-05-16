from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biblioteca'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libro')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', libro = data)

@app.route('/add_libro', methods=['POST'])
def add_libro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        categoria = request.form['categoria']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO libro (titulo, autor, categoria, precio) VALUES (%s,%s,%s, %s)", (titulo, autor, categoria, precio))
        mysql.connection.commit()
        flash('Libro añadido')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_libro(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libro WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-libro.html', libro = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_libro(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        categoria = request.form['categoria']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE libro
            SET titulo = %s,
                categoria = %s,
                autor = %s,
                precio = %s
            WHERE id = %s
        """, (titulo, categoria, autor, precio, id))
        flash('Libro actualizado')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_libro(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM libro WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Libro eliminado')
    return redirect(url_for('Index'))

@app.route("/search", methods=['GET', 'POST'])
def search():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libro WHERE titulo = %s', (request.args["search"],))
    data = cur.fetchall()
    cur.close()
    return render_template('results.html', libro = data)

if __name__ == "__main__":
    app.run(port=3000, debug=True)