from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for, abort


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)

@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return "Unknown email", 500


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
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            club['points'] = int(club['points']) - placesRequired
            placesRequired += placesRequired
            flash('Great-booking complete!')
        else:
            flash('You cannot book more than 12 places per competition')
    else:
        flash('You do not have enough points')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
