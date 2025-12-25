from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'

albums = [
    {"id": 0, "name": "The Dark Side of the Moon", "year": "1973"},
    {"id": 1, "name": "The Wall", "year": "1979"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/history')
def history():
    return render_template('history.html', albums=albums)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('history'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_album():
    if session.get('logged_in'):
        new_album = {
            "id": len(albums),
            "name": request.form['name'],
            "year": request.form['year']
        }
        albums.append(new_album)
    return redirect(url_for('history'))

@app.route('/delete/<int:album_id>')
def delete_album(album_id):
    if session.get('logged_in'):
        global albums
        albums = [a for a in albums if a['id'] != album_id]
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)