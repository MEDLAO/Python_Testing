import os
from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory

COMPETITIONS_FILE = "competitions.json"
CLUBS_FILE = "clubs.json"


def loadClubs(c_f):
    with open(c_f) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions(comp_f):
    with open(comp_f) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions(COMPETITIONS_FILE)
clubs = loadClubs(CLUBS_FILE)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    clbs = [club for club in clubs if club['email'] == request.form['email']]
    if len(clbs) >= 1:
        club = clbs[0]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        return "Unknown email"


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return "Sorry it was a server error", 500


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        datetime_str = foundCompetition['date']
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        competition_date = datetime_object.date()
        today = datetime.today().date()
        if today >= competition_date:
            return 'Sorry you cannot book past competitions', 422
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if int(club['points']) >= 0 and placesRequired <= int(club['points']):
        if placesRequired <= 12:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            index_comp = competitions.index(competition)
            competitions[index_comp]['numberOfPlaces'] = str(competition['numberOfPlaces'])
            a_file = open(COMPETITIONS_FILE, 'w')
            json.dump({"competitions": competitions}, a_file, indent=4)
            a_file.close()

            club['points'] = int(club['points']) - placesRequired
            index_club = clubs.index(club)
            clubs[index_club]['points'] = str(club['points'])
            b_file = open(CLUBS_FILE, 'w')
            json.dump({"clubs": clubs}, b_file, indent=4)
            b_file.close()

            placesRequired += placesRequired
            flash('Great-booking complete!')
        else:
            flash('You cannot book more than 12 places per competition')
    else:
        flash('You do not have enough points')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/pointsDisplayBoard')
def pointsDisplayBoard():
    return render_template('pointsdisplayboard.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run()
