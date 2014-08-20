# −*−coding:utf−8−*−   
# Autor: Mina Habsaoui, Maria Henkel, Fabian Pegel
# Mai 2014
# Projektseminar Angewandte Informationswissenschaft   # 25 jähriger geist eines 6 jährigen walkie talkie autounfall tot betrunken
# Codeteile übernommen vom "Mega-Flask-Tutorial" http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world                   
from flask import Flask, render_template, g, flash, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, desc
import hashlib, os, re, random, string
import operator
from flask_wtf import Form 
from flask.ext.login import LoginManager
from wtforms import TextField, BooleanField, PasswordField, HiddenField, TextAreaField
from wtforms.validators import Required, EqualTo, Length, ValidationError
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from time import time
from flask.ext.babel import Babel
from flask.ext.babel import gettext
_ = gettext
LANGUAGES = {
    'en': 'English',
    'de': 'Deutsch'
}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jHgFtjjGFdE5578ijbDDegh'
app.config['CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite'
db = SQLAlchemy(app)
babel = Babel(app)
lm = LoginManager()
lm.init_app(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

def nl2br(value): 
    return value.replace('\n','<br>\n')
app.jinja_env.globals.update(nl2br=nl2br)

def link_url(value): 
    if value.startswith('http://') or value.startswith('https://'):
        re = "<a href='"
    else:
        re = "<a href='http://"
    return re
app.jinja_env.globals.update(link_url=link_url)


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
  salt = db.Column(db.String(200))
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
      self.salt = salt

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
      


'''
# Datums-Format checken bei Formularen 
def is_german_date(form, field):
    datearray = field.data.split('.')
    if len(datearray) == 3:
        if len(datearray[0])!=2 or int(datearray[0])>31:
             raise ValidationError(_('Geburtsdatum entspricht nicht dem vorgegebenem Format!'))
        if len(datearray[1])!=2 or int(datearray[1])>12:
            raise ValidationError(_('Geburtsdatum entspricht nicht dem vorgegebenem Format!'))
        if len(datearray[2])!=4:
            raise ValidationError(_('Geburtsdatum entspricht nicht dem vorgegebenem Format!'))
        for element in datearray:
            if element.isdigit() == False:
                raise ValidationError(_('Geburtsdatum entspricht nicht dem vorgegebenem Format!'))
    else: 
        raise ValidationError(_('Geburtsdatum entspricht nicht dem vorgegebenem Format!'))
'''

# EditForm-Klasse zum Bearbeiten und Anlegen von Eintragsdaten
class EditForm(Form):
    titel = TextField('name', validators = [Required(_(u"Bitte Feld ausfüllen!"))])
    text = TextAreaField('text', validators = [Required(_(u"Bitte Feld ausfüllen!"))])
    url_titel = TextField('url_titel')
    datum = TextField('datum')

class CommentForm(Form):
    name = TextField('name', validators = [Required(_(u"Bitte Feld ausfüllen!"))])
    email = TextField('email', validators = [Required(_(u"Bitte Feld ausfüllen!"))])
    url = TextField('url')
    text = TextAreaField('text', validators = [Required(_(u"Bitte Feld ausfüllen!"))])
    blogeintragid = HiddenField('blogeintragid')
    
class BlogentryForm(Form):
    titel = TextField('name', validators = [Required(_(u"Bitte Feld ausfüllen!"))])
    text = TextAreaField('text', validators = [Required(_(u"Bitte Feld ausfüllen!"))])
    url_titel = TextField('url_titel')
    datum = TextField('datum')


# Suchfeld-Klasse
class SearchForm(Form): 
    searchfield = TextField('searchfield', validators = [Required(_(u"Bitte Feld ausfüllen!"))])


# Login-Formular-Klasse
class LoginForm(Form):
    enteruser = gettext('Bitte einen Benutzernamen eingeben!')
    username = TextField('username', validators = [Required(enteruser)])
    password = PasswordField('password', validators = [Required(_("Bitte ein Passwort eingeben!"))]) 
    remember_me = BooleanField('remember_me', default = False)
    
# Login-Formular-Klasse
class RegisterForm(Form):
    username = TextField('username', validators = [Required(_("Bitte einen Usernamen eingeben!"))])
    password1 = PasswordField('password', validators = [Required(_("Bitte ein Passwort eingeben!")), Length(min=8, message=u"Passwort muss mindestens 8 Zeichen lang sein!")])
    password2 = PasswordField('password', validators = [Required(_("Bitte ein Passwort eingeben!")), EqualTo('password1', message=u'Passwörter müssen übereinstimmen!')]) 
    vorname = TextField('vorname', validators = [Required(_("Bitte einen Vornamen eingeben!"))])
    nachname = TextField('nachname', validators = [Required(_("Bitte einen Nachnamen eingeben!"))])
    


# Passwort-Formular-Klasse
class ChangePassForm(Form):
    password_old = PasswordField('password_old', validators = [Required(_("Bitte altes Passwort eingeben!"))])
    password1    = PasswordField('password1', validators = [Required(_("Bitte ein neues Passwort eingeben!")), Length(min=8, message=u"Passwort muss mindestens 8 Zeichen lang sein!")]) 
    password2    = PasswordField('password2', validators = [Required(_("Bitte ein neues Passwort eingeben!")), EqualTo('password1', message=u'Passwörter müssen übereinstimmen!')]) 

class ChangeProfileForm(Form):
    vorname = TextField('vorname', validators = [Required(_("Bitte einen Vornamen eingeben!"))])
    nachname = TextField('nachname', validators = [Required(_("Bitte einen Nachnamen eingeben!"))])


# Startseite
@app.route('/seite/<seite_von>')
@app.route('/', defaults={'seite_von': 0})
def hello_world(seite_von):
    eintraege_auf_seite = 5
    seite_von = int(seite_von)
    seite_von = seite_von * eintraege_auf_seite
    seite_bis = seite_von + eintraege_auf_seite
    
    searchform = SearchForm(csrf_enabled=False)
    entries=Entry.query.with_entities(Entry.id,Entry.titel, Entry.text, Entry.url_titel, Entry.datum, Entry.geschriebenvonbenutzername).order_by(desc(Entry.id)).slice(seite_von,seite_bis)
    number_of_results = db.engine.execute(text("SELECT count(id) as anzahl from blogeintrag"))
    for line in number_of_results:
        anzahl = line['anzahl']
    if anzahl>eintraege_auf_seite:    
        seiten = (anzahl/eintraege_auf_seite)
        if anzahl%eintraege_auf_seite!=0:
            seiten = seiten+1
    else:
        seiten = 1
    return render_template('anzeige.htm', entries=entries, searchform=searchform, anzahl=anzahl, seiten=seiten, seite_von=seite_von, eintraege_auf_seite=eintraege_auf_seite, isactive='blog')   
	
    
@app.route('/artikel/<url_titel>', methods = ['GET', 'POST'])
def artikel(url_titel):
    form = CommentForm()
    
    if form.validate_on_submit():
        query = text("INSERT INTO kommentar ('name','email','url','text','datum', 'blogeintragid') VALUES ( :name,:email,:url,:text,:datum,:blogeintragid);")
        db.engine.execute(query, name=form.name.data, email=form.email.data, url=form.url.data, text=form.text.data, datum=str(datetime.now().strftime('%d.%m.%Y - %H:%M Uhr')), blogeintragid=form.blogeintragid.data)
        flash(_("Kommentar wurde angelegt!"), 'accept')
        return redirect('/artikel/'+ url_titel)
    else:
        if request.method=='POST':
            flash(_("Kommentar nicht gepostet! <a href='#kommentar_schreiben'>Zum Formular</a>"),'error')
       
            
    highlight=''
    if request.args.get('highlight'):
        highlight = request.args.get('highlight')
    searchform = SearchForm(csrf_enabled=False)
    entry = Entry.query.filter_by(url_titel=url_titel).with_entities(Entry.titel, Entry.text, Entry.url_titel, Entry.datum, Entry.geschriebenvonbenutzername).first()
    
    blogeintragid_res = db.engine.execute(text("SELECT id FROM blogeintrag WHERE url_titel = :url_titel"), url_titel=url_titel)
    for line in blogeintragid_res:
        blogeintragid=line['id']

    kommentare = db.engine.execute(text("SELECT * FROM kommentar WHERE blogeintragid = (SELECT id FROM blogeintrag WHERE url_titel = :url_titel)"), url_titel=url_titel)
    
    return render_template('anzeige_single.htm', entry=entry, searchform=searchform, highlight=highlight,kommentare=kommentare, form=form, blogeintragid=blogeintragid, isactive='blog', title=entry.titel)


# Profilseite, bisher zum Passwort ändern
@app.route('/register', methods = ['GET', 'POST'])
def register(): 
    searchform = SearchForm(csrf_enabled=False)
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        liste_usernamen = db.engine.execute(text("SELECT username FROM benutzer"))
        for line in liste_usernamen:
            if registerform.username.data == line['username']:
                flash(_("Dieser Benutzername ist schon vergeben!"),'error')
                return render_template('register.htm', searchform=searchform, registerform=registerform)  
        salt = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(32))

        
        
        query = text("INSERT INTO benutzer ('id', 'username', 'passwort', 'vorname', 'nachname', 'salt') VALUES (NULL, :username, :passwort, :vorname, :nachname, :salt);")
        db.engine.execute(query, username=registerform.username.data, passwort=hashlib.md5(registerform.password1.data+salt).hexdigest(), vorname=registerform.vorname.data, nachname=registerform.nachname.data, salt=salt)
        
        flash(_("Benutzer wurde registriert!"),'accept')
    return render_template('register.htm', searchform=searchform, registerform=registerform, isactive='register')   



# Profilseite, bisher zum Passwort ändern
@app.route('/password', methods = ['GET', 'POST'])
@login_required
def password(): 
    searchform = SearchForm(csrf_enabled=False)
    passwordform = ChangePassForm()
    if passwordform.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        # Überprüfen ob md5-gehashtes Passwort in der DB mit md5 gehashtem Formular-Passwort übereinstimmt
        if user is not None and user.passwort == hashlib.md5(passwordform.password_old.data+user.salt).hexdigest():
            neues_pw = hashlib.md5(passwordform.password1.data+user.salt).hexdigest()
            # neues Passwort hashen und in die DB eintragen, text()-Funktion gegegn SQL-Injections
            query = text("UPDATE benutzer SET passwort=:passwort WHERE username=:username")
            db.engine.execute(query, username=session['username'], passwort=neues_pw)
            flash(_(u"Passwörter geändert!"), 'accept')
        else:
            flash(_("Altes Passwort ist falsch!"),'error')
        
    return render_template('password.htm', searchform=searchform, passwordform=passwordform, isactive='profile')   
    
@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile(): 
    searchform = SearchForm(csrf_enabled=False)
    profileform = ChangeProfileForm()
    if profileform.validate_on_submit():
        query = text("UPDATE benutzer SET vorname=:vorname, nachname=:nachname WHERE username=:username")
        db.engine.execute(query, vorname=profileform.vorname.data, nachname=profileform.nachname.data, username=session['username'])
        flash(_(u"Profil geändert!"), 'accept')
    userdata = User.query.filter_by(username=session['username']).with_entities(User.vorname,User.nachname).first()
   
        
    return render_template('profile.htm', searchform=searchform, profileform=profileform, userdata=userdata, isactive='profile')   



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
    form = BlogentryForm()
    searchform = SearchForm(csrf_enabled=False)
    entries = Entry.query.filter_by(geschriebenvonbenutzername=session['username']).with_entities(Entry.id,Entry.titel, Entry.text, Entry.url_titel, Entry.datum, Entry.geschriebenvonbenutzername).order_by(desc(Entry.id))
    te = Entry.query.filter_by(id=id).with_entities(Entry.text).first()
    # wenn id gegeben ist, zeige nicht alle Einträge, sondern einen zum bearbeiten
    if id is not None:
        if not form.validate_on_submit():
            form.text.data=te[0]
        
        if form.validate_on_submit():
            liste_urls = db.engine.execute(text("SELECT url_titel FROM blogeintrag WHERE url_titel = :url_titel"), url_titel=form.url_titel.data)
            for line in liste_urls:
                if form.url_titel.data == line['url_titel']:
                    form.url_titel.data = form.url_titel.data+"_"+str(time())
            
            # text()-Funktion escapet den string
            query = text("UPDATE blogeintrag SET id=:id, titel=:titel, text=:text, url_titel=:url_titel, datum=:datum, geschriebenvonbenutzername=:geschriebenvonbenutzername where id=:id ;")
            flash(_("Eintrag bearbeitet!"), 'accept')
            # Daten ändern
            db.engine.execute(query, titel=form.titel.data, url_titel=form.url_titel.data, datum=form.datum.data, text=form.text.data, geschriebenvonbenutzername=session['username'], id=id)
            
        entries = Entry.query.filter_by(id=id).with_entities(Entry.id,Entry.titel, Entry.text, Entry.url_titel, Entry.datum, Entry.geschriebenvonbenutzername).first()
    return render_template('edit.htm', entries=entries, id=id , form=form, searchform=searchform, isactive='edit')  


# Neuen Eintrag anlegen
@app.route('/new', methods = ['GET', 'POST'])
@login_required
def new():
    searchform = SearchForm(csrf_enabled=False)
    form = BlogentryForm()
    if form.validate_on_submit():
        liste_urls = db.engine.execute(text("SELECT url_titel FROM blogeintrag WHERE url_titel = :url_titel"), url_titel=form.url_titel.data)
        for line in liste_urls:
            if form.url_titel.data == line['url_titel']:
                form.url_titel.data = form.url_titel.data+"_"+str(time())
        
        query = text("INSERT INTO blogeintrag ('titel', 'url_titel', 'datum', 'text', 'geschriebenvonbenutzername') VALUES (:titel, :url_titel, :datum, :text, :geschriebenvonbenutzername);")
        db.engine.execute(query, titel=form.titel.data, url_titel=form.url_titel.data, datum=form.datum.data, text=form.text.data, geschriebenvonbenutzername=session['username'])
        flash(_("Eintrag wurde angelegt!"), 'accept')
        return redirect('/new')
    else:
        return render_template('new.htm', form=form, searchform=searchform, zeit=str(datetime.now().strftime('%d.%m.%Y')), isactive='new')
    
    
# Eintrag löschen
@app.route('/delete/<id>')
@login_required
def delete(id):
    if id is not None:
        query = text("DELETE FROM blogeintrag WHERE id = :id;")
        db.engine.execute(query, id=id)
        flash(_(u"Eintrag mit der ID ") + str(id) + _(u" gelöscht!"), 'accept')
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
        if user is not None and user.passwort == hashlib.md5(p_password+user.salt).hexdigest():
            session['username']=user.username
            login_user(user, remember = remember_me)
            flash(_('Herzlich Willkommen, ')+session['username']+'!', 'accept')
            return redirect('/')
        else:
            flash(_('Benutzername oder Passwort falsch!'), 'error')

    return render_template('login.htm', 
        form = form, searchform=searchform, isactive='login')

# Ausloggen
@app.route('/logout')
def logout():
    if session['username']:
        session.pop('username', None)
    logout_user()
    flash(_('Du wurdest erfolgreich ausgeloggt!'),'accept')
    return redirect('/login')

        
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')     
