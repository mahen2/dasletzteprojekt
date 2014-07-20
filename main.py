# −*−coding:utf−8−*−   
# Autor: Mina Habsaoui, Maria Henkel, Fabian Pegel
# Mai 2014
# Projektseminar Angewandte Informationswissenschaft   
# Codeteile übernommen vom "Mega-Flask-Tutorial" http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world                   
from flask import Flask, render_template, g, flash, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, desc
import hashlib, os, re
import operator
from flask_wtf import Form
from flask.ext.login import LoginManager
from wtforms import TextField, BooleanField, PasswordField, HiddenField
from wtforms.validators import Required, EqualTo, Length, ValidationError
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import timedelta, date
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
      



# Datums-Format checken bei Formularen 
def is_german_date(form, field):
    datearray = field.data.split('.')
    if len(datearray) == 3:
        if len(datearray[0])!=2 or int(datearray[0])>31:
             raise ValidationError('Geburtsdatum entspricht nicht dem vorgegebenem Format!')
        if len(datearray[1])!=2 or int(datearray[1])>12:
            raise ValidationError('Geburtsdatum entspricht nicht dem vorgegebenem Format!')
        if len(datearray[2])!=4:
            raise ValidationError('Geburtsdatum entspricht nicht dem vorgegebenem Format!')
        for element in datearray:
            if element.isdigit() == False:
                raise ValidationError('Geburtsdatum entspricht nicht dem vorgegebenem Format!')
    else: 
        raise ValidationError('Geburtsdatum entspricht nicht dem vorgegebenem Format!')


# EditForm-Klasse zum Bearbeiten und Anlegen von Eintragsdaten
class EditForm(Form):
    userid =      TextField('userid')
    vorname = TextField('vorname', validators = [Required(u"Bitte Feld ausfüllen!")])
    name = TextField('name', validators = [Required(u"Bitte Feld ausfüllen!")])
    titel = TextField('titel')
    strasse = TextField('strasse')
    plz = TextField('plz')
    ort = TextField('ort')
    geburtsdatum = TextField('geburtsdatum', validators = [Required(u"Bitte Feld ausfüllen!"), is_german_date])
    festnetz = TextField('festnetz')
    mobil = TextField('mobil')
    email = TextField('email')
    homepage = TextField('homepage')
    twitter = TextField('twitter')   

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


# Textanalyse UNFERTIG
@app.route('/statistik')
def wort_statistik(): 
    searchform = SearchForm(csrf_enabled=False)
    entries=Entry.query.with_entities(Entry.titel, Entry.text) 
    blogtexte = db.engine.execute('SELECT text FROM blogeintrag;')
    stoppwort = ["ab", "aber", "abgesehen", "alle", "allein", "aller", "alles", "als", "am", "an", "andere", "anderen", "anderenfalls", "anderer", "anderes", "anstatt", "auch", "auf", "aus", "aussen", "außen", "ausser", "außer", "ausserdem", "außerdem", "außerhalb", "ausserhalb", "behalten", "bei", "beide", "beiden", "beider", "beides", "beinahe", "bevor", "bin", "bis", "bist", "bitte", "da", "daher", "danach", "dann", "darueber", "darüber", "darueberhinaus", "darüberhinaus", "darum", "das", "dass", "daß", "dem", "den", "der", "des", "deshalb", "die", "diese", "diesem", "diesen", "dieser", "dieses", "dort", "duerfte", "duerften", "duerftest", "duerftet", "dürfte", "dürften", "dürftest", "dürftet", "durch", "durfte", "durften", "durftest", "durftet", "ein", "eine", "einem", "einen", "einer", "eines", "einige", "einiger", "einiges", "entgegen", "entweder", "erscheinen", "es", "etwas", "fast", "fertig", "fort", "fuer", "für", "gegen", "gegenueber", "gegenüber", "gehalten", "geht", "gemacht", "gemaess", "gemäß", "genug", "getan", "getrennt", "gewesen", "gruendlich", "gründlich", "habe", "haben", "habt", "haeufig", "häufig", "hast", "hat", "hatte", "hatten", "hattest", "hattet", "hier", "hindurch", "hintendran", "hinter", "hinunter", "ich", "ihm", "ihnen", "ihr", "ihre", "ihrem", "ihren", "ihrer", "ihres", "ihrige", "ihrigen", "ihriges", "immer", "in", "indem", "innerhalb", "innerlich", "irgendetwas", "irgendwelche", "irgendwenn", "irgendwo", "irgendwohin", "ist", "jede", "jedem", "jeden", "jeder", "jedes", "jedoch", "jemals", "jemand", "jemandem", "jemanden", "jemandes", "jene", "jung", "junge", "jungem", "jungen", "junger", "junges", "kann", "kannst", "kaum", "koennen", "koennt", "koennte", "koennten", "koenntest", "koenntet", "können", "könnt", "könnte", "könnten", "könntest", "könntet", "konnte", "konnten", "konntest", "konntet", "machen", "macht", "machte", "mehr", "mehrere", "mein", "meine", "meinem", "meinen", "meiner", "meines", "meistens", "mich", "mir", "mit", "muessen", "müssen", "muesst", "müßt", "muß", "muss", "musst", "mußt", "nach", "nachdem", "naechste", "nächste", "nebenan", "nein", "nichts", "niemand", "niemandem", "niemanden", "niemandes", "nirgendwo", "nur", "oben", "obwohl", "oder", "oft", "ohne", "pro", "sagte", "sagten", "sagtest", "sagtet", "scheinen", "sehr", "sei", "seid", "seien", "seiest", "seiet", "sein", "seine", "seinem", "seinen", "seiner", "seines", "seit", "selbst", "sich", "sie", "sind", "so", "sogar", "solche", "solchem", "solchen", "solcher", "solches", "sollte", "sollten", "solltest", "solltet", "sondern", "statt", "stets", "tatsächlich", "tatsaechlich", "tief", "tun", "tut", "ueber", "über", "ueberall", "überll", "um", "und", "uns", "unser", "unsere", "unserem", "unseren", "unserer", "unseres", "unten", "unter", "unterhalb", "usw", "viel", "viele", "vielleicht", "von", "vor", "vorbei", "vorher", "vorueber", "vorüber", "waehrend", "während", "wann", "war", "waren", "warst", "wart", "was", "weder", "wegen", "weil", "weit", "weiter", "weitere", "weiterem", "weiteren", "weiterer", "weiteres", "welche", "welchem", "welchen", "welcher", "welches", "wem", "wen", "wenige", "wenn", "wer", "werde", "werden", "werdet", "wessen", "wie", "wieder", "wir", "wird", "wirklich", "wirst", "wo", "wohin", "wuerde", "wuerden", "wuerdest", "wuerdet", "würde", "würden", "würdest", "würdet", "wurde", "wurden", "wurdest", "wurdet", "ziemlich", "zu", "zum", "zur", "zusammen", "zwischen", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "Die", "ten", "than", "that", "The", "-", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
    wordlist = []
    wordcount = {}
    for eintrag in blogtexte:
        for text in eintrag:
            wordlist.append(text.split())
    for liste in wordlist:
        for wort in liste:
            if wort not in stoppwort:
                if wort in wordcount:
                    wordcount[wort] = wordcount[wort] + 1
                else:
                    wordcount[wort] = 1
    ranking = dict(sorted(wordcount.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
    print ranking
    return render_template('anzeige.htm', entries=entries, searchform=searchform)  


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
 
# Einträge zum bearebiten anzeigen oder Einzeleinträge bearbeiten
@app.route('/edit', defaults={'id': None})
@app.route('/edit/<id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    form = EditForm()
    searchform = SearchForm(csrf_enabled=False)
    entries = Entry.query.with_entities(Entry.id, Entry.vorname,Entry.name,Entry.titel,Entry.strasse,Entry.plz,Entry.ort, Entry.geburtsdatum, Entry.festnetz, Entry.mobil, Entry.email, Entry.homepage,Entry.twitter).order_by(desc(Entry.id))
    # wenn id gegeben ist, zeige nicht alle Einträge, sondern einen zum bearbeiten
    if id is not None:
        if form.validate_on_submit():
            # text()-Funktion escapet den string
            query = text("UPDATE daten SET vorname=:vorname, name=:name, titel=:titel,strasse=:strasse, plz=:plz, ort=:ort, geburtsdatum=:geburtsdatum, festnetz=:festnetz, mobil=:mobil, email=:email, homepage=:homepage, twitter=:twitter where id=:userid ;")
            flash("Eintrag bearbeitet!", 'accept')
            # Daten ändern
            db.engine.execute(query, vorname=form.vorname.data, name=form.name.data, titel=form.titel.data, strasse=form.strasse.data, plz=form.plz.data, ort=form.ort.data, geburtsdatum=form.geburtsdatum.data, festnetz=form.festnetz.data, mobil=form.mobil.data, email=form.email.data, homepage=form.homepage.data, twitter=form.twitter.data, userid=form.userid.data)
            
        entries = Entry.query.filter_by(id=id).with_entities(Entry.id, Entry.vorname,Entry.name,Entry.titel,Entry.strasse,Entry.plz,Entry.ort, Entry.geburtsdatum, Entry.festnetz, Entry.mobil, Entry.email, Entry.homepage,Entry.twitter).first()
    return render_template('edit.htm', entries=entries, id=id , form=form, searchform=searchform)  


# Neuen Eintrag anlegen
@app.route('/new', methods = ['GET', 'POST'])
@login_required
def new():
    searchform = SearchForm(csrf_enabled=False)
    form = EditForm()
    if form.validate_on_submit():
        query = text("INSERT INTO daten ('id','vorname','name','titel','strasse','plz','ort','geburtsdatum','festnetz','mobil','email','homepage','twitter') VALUES (NULL, :vorname,:name,:titel,:strasse,:plz,:ort,:geburtsdatum,:festnetz,:mobil,:email,:homepage,:twitter);")
        db.engine.execute(query, vorname=form.vorname.data, name=form.name.data, titel=form.titel.data, strasse=form.strasse.data, plz=form.plz.data, ort=form.ort.data, geburtsdatum=form.geburtsdatum.data, festnetz=form.festnetz.data, mobil=form.mobil.data, email=form.email.data, homepage=form.homepage.data, twitter=form.twitter.data)
        flash("Eintrag wurde angelegt!", 'accept')
        return redirect('/edit')
    else:
        return render_template('new.htm', form=form, searchform=searchform)
    
    
# Eintrag löschen
@app.route('/delete/<id>')
@login_required
def delete(id):
    if id is not None:
        query = text("DELETE FROM daten WHERE id = :id;")
        db.engine.execute(query, id=id)
        flash(u"Benutzer mit der ID " + str(id) + u" gelöscht!", 'accept')
        return redirect('/edit')

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
