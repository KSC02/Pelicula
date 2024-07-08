from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '123456'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biblioteca'

mysql = MySQL(app)

# Rutas
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM peliculas")
    if result_value > 0:
        movies = cur.fetchall()
        return render_template('index.html', movies=movies)
    return render_template('index.html')

# Consulta de Usuario (Arreglado)
@app.route('/consul_usuario')
def index_usuario():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM usuarios")
    if result_value > 0:
        users = cur.fetchall()
        return render_template('usuarios_consulta.html', users=users)
    return render_template('usuarios_consulta.html')

# Agregar peliculas (arreglado)
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie_details = request.form
        title = movie_details.get('title')
        director = movie_details.get('director')
        anio = movie_details.get('anio')
        genero = movie_details.get('genero')
        quantity = movie_details.get('quantity')
        image_url = movie_details.get('image_url')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO peliculas (titulo, director, anio, genero, cantidad_disponible, imagen_url) VALUES (%s, %s, %s, %s, %s, %s)",
                    (title, director, anio, genero, quantity, image_url))
        mysql.connection.commit()
        cur.close()
        flash('Película agregada satisfactoriamente')
        return redirect(url_for('index'))
    return render_template('add_movie.html')

# Agrega Usuario (Arreglado)
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_details = request.form
        ape = user_details['apellido']
        nomb = user_details['nombre']
        correo = user_details['correo']
        fono = user_details['fono']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(nombre, apellido, correo, telefono) VALUES(%s, %s, %s, %s)", (nomb, ape, correo, fono))
        mysql.connection.commit()
        cur.close()
        flash('Usuario Agregado Satisfactoriamente')
        return redirect(url_for('index_usuario'))
    return render_template('usuarios_add.html')

# Editar datos de la peliculas (Arreglado)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM peliculas WHERE id = %s", [id])
    movie = cur.fetchone()
    if request.method == 'POST':
        movie_details = request.form
        title = movie_details['titulo']  # Asegúrate de que los nombres coincidan con los de la plantilla
        director = movie_details['director']
        anio = movie_details['anio']
        genero = movie_details['genero']
        quantity = movie_details['cantidad_disponible']
        image_url = movie_details['image_url']  # Asegúrate de incluir esto en el formulario si lo estás editando
        cur.execute("UPDATE peliculas SET titulo = %s, director = %s, anio = %s, genero = %s, cantidad_disponible = %s, imagen_url = %s WHERE id = %s", (title, director, anio, genero, quantity, image_url, id))
        mysql.connection.commit()
        cur.close()
        flash('Película actualizada satisfactoriamente')
        return redirect(url_for('index'))
    return render_template('edit_movie.html', movie=movie)  # Cambia 'pelicula' por 'movie'

# edita Usuarios (Arreglado)
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, apellido, nombre, correo, telefono FROM usuarios WHERE id = %s", [id])
    user = cur.fetchone()
    if request.method == 'POST':
        user_details = request.form
        ape = user_details['apellido']
        nomb = user_details['nombre']
        correo = user_details['correo']
        fono = user_details['fono']
        
        cur.execute("UPDATE usuarios SET apellido = %s, nombre = %s, correo = %s, telefono = %s WHERE id = %s", (ape, nomb, correo, fono, id))
        mysql.connection.commit()
        cur.close()
        flash('Usuario actualizado satisfactoriamente')
        return redirect(url_for('index_usuario'))
    return render_template('usuarios_edit.html', user=user) 

# Elimina Las peliculas -- Funciona --
@app.route('/delete/<int:id>', methods=['POST'])
def delete_movie(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM peliculas WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Película eliminada satisfactoriamente')
    return redirect(url_for('index'))

# Elimina los Usuarios -- Funciona --
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Usuario eliminado satisfactoriamente')
    return redirect(url_for('index_usuario'))

# 
@app.route('/alquileres', methods=['GET'])
def alquileres():
    cur = mysql.connection.cursor()
    cur.execute("SELECT a.id, p.titulo as pelicula_titulo, u.nombre as usuario_nombre, a.fecha_alquiler, a.fecha_devolucion "
                "FROM alquileres a "
                "JOIN peliculas p ON a.id_pelicula = p.id "
                "JOIN usuarios u ON a.id_usuario = u.id")
    alquileres1 = cur.fetchall()

    cur.execute("SELECT id, titulo FROM peliculas")
    peliculas1 = cur.fetchall()

    cur.execute("SELECT id, concat(apellido,' ', nombre) as nombre FROM usuarios")
    usuarios1 = cur.fetchall()

    cur.close()
    return render_template('alquileres.html', alquileres=alquileres1, peliculas=peliculas1, usuarios=usuarios1)

#Agregar alquiler (Arreglado)
@app.route('/alquileres/agregar', methods=['GET', 'POST'])
def agregar_alquiler():
    if request.method == 'POST':
        id_pelicula = request.form['id_pelicula']
        id_usuario = request.form['id_usuario']
        fecha_alquiler = request.form['fecha_alquiler']
        fecha_devolucion = request.form.get('fecha_devolucion')  # Usar .get() para manejar campos opcionales

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO alquileres (id_pelicula, id_usuario, fecha_alquiler, fecha_devolucion) VALUES (%s, %s, %s, %s)", 
                    (id_pelicula, id_usuario, fecha_alquiler, fecha_devolucion))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('alquileres'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, titulo FROM peliculas")
    peliculas1 = cur.fetchall()

    cur.execute("SELECT id, concat(apellido,' ', nombre) as nombre FROM usuarios")
    usuarios1 = cur.fetchall()
    
    cur.close()
    return render_template('alquileres_add.html', peliculas=peliculas1, usuarios=usuarios1)

# Editar Datos de alquileres (Arreglado)
@app.route('/edit_alquiler/<int:id>', methods=['GET', 'POST'])
def edit_alquiler(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM alquileres WHERE id = %s", [id])
    alquiler = cur.fetchone()

    cur.execute("SELECT id, titulo FROM peliculas")
    peliculas1 = cur.fetchall()

    cur.execute("SELECT id, concat(apellido,' ', nombre) as nombre FROM usuarios")
    usuarios1 = cur.fetchall()

    if request.method == 'POST':
        alquiler_details = request.form
        id_pelicula = alquiler_details['id_pelicula']
        id_usuario = alquiler_details['id_usuario']
        fecha_alquiler = alquiler_details['fecha_alquiler']
        fecha_devolucion = alquiler_details.get('fecha_devolucion')  # Usar .get() para manejar campos opcionales
        
        cur.execute("UPDATE alquileres SET id_pelicula = %s, id_usuario = %s, fecha_alquiler = %s, fecha_devolucion = %s WHERE id = %s", 
                    (id_pelicula, id_usuario, fecha_alquiler, fecha_devolucion, id))
        mysql.connection.commit()
        cur.close()
        flash('Alquiler actualizado satisfactoriamente')
        return redirect(url_for('alquileres'))

    return render_template('alquileres_edit.html', alquiler=alquiler, peliculas=peliculas1, usuarios=usuarios1)

# Eliminar Datos de usurios que han alquilado (Alquileres) -- Si Funciona --
@app.route('/delete_alquiler/<int:id>', methods=['POST'])
def delete_alquiler(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM alquileres WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Alquiler eliminado satisfactoriamente')
    return redirect(url_for('alquileres'))

if __name__ == '__main__':
    app.run(debug=True)