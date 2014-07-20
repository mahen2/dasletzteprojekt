# −*−coding:utf−8−*−   
# Autor: Giulia Kirstein, Daniel Gros, Fabian Pegel
# Mai 2014
# Projektseminar Angewandte Informationswissenschaft   
# Codeteile übernommen vom "Mega-Flask-Tutorial" http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world                   
from flask import Flask, render_template, g, flash, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, desc
import hashlib, os, re
from flask_wtf import Form
from flask.ext.login import LoginManager
from wtforms import TextField, BooleanField, PasswordField, HiddenField
from wtforms.validators import Required, EqualTo, Length, ValidationError
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import timedelta, date
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('main', 'templates'))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jHgFtjjGFdE5578ijbDDegh'
app.config['CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite'
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)


def nl2br(value): 
    return value.replace('\n','<br>\n')
app.jinja_env.globals.update(nl2br=nl2br)

def teile_text_zum_weiterlesen(text):
    text_teile = text.split('[weiterlesen]')
    return text_teile
app.jinja_env.globals.update(teile_text_zum_weiterlesen=teile_text_zum_weiterlesen)

def entferne_weiterlesen_marker(text):
    return text.replace('[weiterlesen]','')
app.jinja_env.globals.update(entferne_weiterlesen_marker=entferne_weiterlesen_marker)

def highlight_word(text, word):
    if word:
        text_list = text.split(" ")
        text_list_neu = []
        for element in text_list:
            if element.lower().startswith(word.lower()):
                text_list_neu.append('<span style="background-color:yellow;">'+element+'</span>')
            else:
                text_list_neu.append(element)
        
        return " ".join(text_list_neu)
    else:
        print 22222
        return text
app.jinja_env.globals.update(highlight_word=highlight_word)

# Userklasse definieren
class User(db.Model):
  # Setting the table name and
  # creating columns for various fields
  __tablename__ = 'benutzer' 
  id = db.Column('id', db.Integer, primary_key=True)
  passwort = db.Column(db.String(100))
  username = db.Column(db.String(200))
  vorname = db.Column(db.String(200))
  nachname = db.Column(db.String(200))
  def is_authenticated(self):
      return True

  def is_active(self):
      return True

  def is_anonymous(self):
      return False

  def get_id(self):
      return unicode(self.id)

  def __repr__(self):
      return '<User %r>' % (self.username)
  
  def __init__(self, id, passwort, username):
      # Initializes the fentered data
      # and sets the published date to the current time
      self.id = id
      self.passwort = passwort
      self.username = username
      self.vorname = vorname
      self.nachname = nachname

# User-Loader für den Login
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# Entry-Klasse für die Einträge
class Entry(db.Model):
  # Setting the table name and
  # creating columns for various fields
  __tablename__ = 'blogeintrag' 
  id = db.Column('id', db.Integer, primary_key=True)
  titel = db.Column(db.String(200))
  text = db.Column(db.String(200000))
  url_titel = db.Column(db.String(200))
  datum = db.Column(db.String(200))
  geschriebenvonbenutzername = db.Column(db.String(200))
  def __init__(self, id, vorname, nachname, titel, strasse, plz, ort, geburtsdatum, festnetz, mobil, email, homepage, twitter):
      # Initializes the fields with entered data
      # and sets the published date to the current time
      self.id = id
      self.titel = titel
      self.text = text
      self.url_titel = url_titel
      self.datum = datum
      self.geschriebenvonbenutzername = geschriebenvonbenutzername
      



# Suchfeld-Klasse
class SearchForm(Form): 
    searchfield = TextField('searchfield', validators = [Required(u"Bitte Feld ausfüllen!")])


# Login-Formular-Klasse
class LoginForm(Form):
    username = TextField('username', validators = [Required("Bitte einen Benutzernamen eingeben!")])
    password = PasswordField('password', validators = [Required("Bitte ein Passwort eingeben!")]) 
    remember_me = BooleanField('remember_me', default = False)

# Passwort-Formular-Klasse
class ChangePassForm(Form):
    password_old = PasswordField('password_old', validators = [Required("Bitte altes Passwort eingeben!")])
    password1    = PasswordField('password1', validators = [Required("Bitte ein neues Passwort eingeben!"), Length(min=8, message=u"Passwort muss mindestens 8 Zeichen lang sein!")]) 
    password2    = PasswordField('password2', validators = [Required("Bitte ein neues Passwort eingeben!"), EqualTo('password1', message=u'Passwörter müssen übereinstimmen!')]) 



# Startseite
@app.route('/')
def hello_world(): 
    searchform = SearchForm(csrf_enabled=False)
    entries=Entry.query.with_entities(Entry.titel, Entry.text, Entry.url_titel, Entry.datum, Entry.geschriebenvonbenutzername) 
    return render_template('anzeige.htm', entries=entries, searchform=searchform)   
	
    
@app.route('/artikel/<url_titel>', methods = ['GET', 'POST'])
def artikel(url_titel):
    highlight=''
    if request.args.get('highlight'):
        highlight = request.args.get('highlight')
    print "hughlight: "+highlight
    searchform = SearchForm(csrf_enabled=False)
    entries = Entry.query.filter_by(url_titel=url_titel).with_entities(Entry.titel, Entry.text, Entry.url_titel, Entry.datum, Entry.geschriebenvonbenutzername)
    
    k_query = text("SELECT * FROM kommentar WHERE blogeintragid = (SELECT id FROM blogeintrag WHERE url_titel = 'witness_to_a_shelling:_first-hand_account_of_deadly_strike_on_gaza_port'")
    kommentare = db.engine.execute(text("SELECT * FROM kommentar WHERE blogeintragid = (SELECT id FROM blogeintrag WHERE url_titel = :url_titel)"), url_titel=url_titel)
    
    return render_template('anzeige_single.htm', entries=entries, searchform=searchform, highlight=highlight,kommentare=kommentare)



# Profilseite, bisher zum Passwort ändern
@app.route('/profile', methods = ['GET', 'POST'])
def profile(): 
    searchform = SearchForm(csrf_enabled=False)
    passwordform = ChangePassForm()
    if passwordform.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        # Überprüfen ob md5-gehashtes Passwort in der DB mit md5 gehashtem Formular-Passwort übereinstimmt
        if user is not None and user.passwort == hashlib.md5(passwordform.password_old.data).hexdigest():
            neues_pw = hashlib.md5(passwordform.password1.data).hexdigest()
            # neues Passwort hashen und in die DB eintragen, text()-Funktion gegegn SQL-Injections
            query = text("UPDATE benutzer SET passwort=:passwort WHERE username=:username")
            db.engine.execute(query, username=session['username'], passwort=neues_pw)
            flash(u"Passwörter geändert!", 'accept')
        else:
            flash("Altes Passwort ist falsch!",'error')
        
    return render_template('profile.htm', searchform=searchform, passwordform=passwordform)   
 
   
# Suchformular
@app.route('/search', methods = ['GET', 'POST'])
def search(): 
    searchform = SearchForm(csrf_enabled=False)
    if request.args['searchfield']:
        begriff = request.args['searchfield']
        begriff_trunk = '%'+begriff+'%'
        # in allen Feldern suchen, auch Bestandteil-Suche erlauben (deshalb Anfang und Ende mit % trunkiert)
        query = text("SELECT titel,text,url_titel FROM blogeintrag WHERE titel like :begriff_trunk or text like :begriff_trunk group by id; ")
        searchentries = db.engine.execute(query, begriff_trunk=begriff_trunk)
        number_of_results = db.engine.execute(text("SELECT count(id) as anzahl from blogeintrag where text like :begriff_trunk or titel like :begriff_trunk"), begriff_trunk=begriff_trunk)
    else:
        return redirect('/')
    return render_template('search.htm', searchform=searchform, begriff=begriff, searchentries=searchentries, number_of_results=number_of_results)    
 

# Einloggen
@app.route('/login', methods = ['GET', 'POST']) 
def login():
    searchform = SearchForm(csrf_enabled=False)
    form = LoginForm()
    if form.validate_on_submit():
        p_username = form.username.data
        p_password = form.password.data
        remember_me = False
        # An Login erinnern, wenn Checkbox geklickt wurde
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        user = User.query.filter_by(username=p_username).first()
        # wenn Passwort aus dem Formular und aus der DB übereinstimmen, logge User ein
        if user is not None and user.passwort == hashlib.md5(p_password).hexdigest():
            session['username']=user.username
            login_user(user, remember = remember_me)
            flash('Herzlich Willkommen, '+session['username']+'!', 'accept')
            return redirect('/')
        else:
            flash('Benutzername oder Passwort falsch!', 'error')

    return render_template('login.htm', 
        title = 'Sign In',
        form = form, searchform=searchform)

# Ausloggen
@app.route('/logout')
def logout():
    if session['username']:
        session.pop('username', None)
    logout_user()
    flash('Du wurdest erfolgreich ausgeloggt!','accept')
    return redirect('/login')

        
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')     