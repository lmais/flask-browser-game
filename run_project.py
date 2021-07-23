#Laura Maisenhelder, lmm326@drexel.edu  
#CS530: Project

from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
#from passlib.hash import pbkdf2_sha256
import os
from db import Database


app = Flask(__name__, static_folder='public', static_url_path='')
#session key
app.secret_key = b'dI/9l$9[jca_3'

#Handle the index (home) page
@app.route('/')
def index():
    return render_template('index.html')


#Handle any files that begin "/course" by loading from the course directory
@app.route('/course/<path:path>')
def base_static(path):
    return send_file(os.path.join(app.root_path, '..', 'course', path))

#database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#Handle the game page
@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/api/game', methods = ['GET', 'POST'])
def api_game():
	scene = request.args.get('s', default = 's1')  
	response = {
        'game_scene': get_db().get_scene(scene),
    }
	return jsonify(response)
	
	
#Handle any unhandled filename by loading its template
@app.route('/<name>')
def generic(name):
    return render_template(name + '.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
