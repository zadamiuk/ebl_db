from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route('/image')
def image():
    return app.send_static_file("image.jpg")


@app.route('/clubs/')
def get_clubs():
    conn = sqlite3.connect('EnergaBasketLiga.db')
    cursor = conn.cursor()
    query = "SELECT * FROM EnergaBasketLiga"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template('clubs.html', data=data)


@app.route('/update-club/<int:id>', methods=["GET"])
def get_update_club_form(id):
        try:
            conn = sqlite3.connect('EnergaBasketLiga.db')
            cursor = conn.cursor()
            query = "SELECT * FROM EnergaBasketLiga WHERE Id=?"
            cursor.execute(query, (id, ))
            data = cursor.fetchall()
            conn.commit()
            conn.close()
            return render_template('update-club.html', data=data[0])
        except Exception as err:
            return "Error! " + str(err), 500


@app.route('/update-club', methods=["POST"])
def get_update_club():
        try:
            Id = int(request.form['id'])
            Name = request.form['team-name']
            City = request.form['city-name']
            Wins = int(request.form['wins'])
            Loses = int(request.form['loses'])

            conn = sqlite3.connect('EnergaBasketLiga.db')
            cursor = conn.cursor()
            query = "UPDATE EnergaBasketLiga SET Name=?, City=?, Wins=?, Loses=? WHERE Id=?"
            cursor.execute(query, (Name, City, Wins, Loses, Id))
            conn.commit()
            conn.close()

            return redirect(url_for('get_clubs'))
        except Exception as err:
            return "Error! " + str(err), 500


@app.route('/delete-club/<int:id>', methods=["GET"])
def delete_record(id):
        try:
            conn = sqlite3.connect('EnergaBasketLiga.db')
            cursor = conn.cursor()
            query = "DELETE FROM EnergaBasketLiga WHERE Id=?"
            cursor.execute(query, (id, ))
            conn.commit()
            conn.close()
            return redirect(url_for('get_clubs'))
        except Exception as err:
            return "Error! " + str(err), 500


@app.route('/add-club', methods=["GET"])
def get_add_club_form():
        try:
            conn = sqlite3.connect('EnergaBasketLiga.db')
            cursor = conn.cursor()
            query = "SELECT Id FROM EnergaBasketLiga"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.commit()
            conn.close()
            last_id = int(data[-1][0])
            return render_template('add-club.html', id = last_id + 1)
        except Exception as err:
            return "Error! " + str(err), 500


@app.route('/add-club', methods=["POST"])
def add_record():
        try:
            conn = sqlite3.connect('EnergaBasketLiga.db')
            cursor = conn.cursor()

            Id = int(request.form['new-id'])
            Name = request.form['new-team-name']
            City = request.form['new-city-name']
            Wins = int(request.form['new-wins'])
            Loses = int(request.form['new-loses'])

            query = "INSERT INTO EnergaBasketLiga(Name, City, Wins, Loses)" + \
            "VALUES(?,?,?,?)"

            ret = cursor.execute(query, (Name, City, Wins, Loses))
            conn.commit()
            conn.close()

            return redirect(url_for('get_clubs'))
        except Exception as err:
            return "Error! " + str(err), 500


if __name__ == "__main__":
    app.run()
