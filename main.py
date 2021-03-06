import bottle
from bottle import view, route, run, Bottle, install, static_file, post, request,redirect
from bottle_sqlite import SQLitePlugin
from beaker.middleware import SessionMiddleware
from os import getcwd
import os.path
from os.path import join


#za lazji setup
if not os.path.isfile("baza.db"):
  import baza


plugin = SQLitePlugin(dbfile='baza.db', keyword='db')
install(plugin)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3000,
    'session.data_dir': './session',
    'session.auto': True
}

tipi_vprasanj = [
    "text",
    "radiobutton",
    "checkbox"
]

root = getcwd()
app = SessionMiddleware(bottle.app(), session_opts)

@route('/skin/css/style.css')
def style():
    return static_file('skin/css/style.css', root=root)

@route('/skin/js/script.js')
def js():
    return static_file('skin/js/script.js', root=root)


@route("/login/")
@view("login")
def login():
    s = bottle.request.environ.get('beaker.session')
    if s.get('login', False):
        redirect('/')
        return {"loggedin":True}
    return {"loggedin":False}   


@post("/do_login/")
def login(db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    result = db.execute('SELECT * FROM uporabniki WHERE username=? AND password=?',(username,password))
    data = result.fetchall()
    
    if len(data) == 0:
        redirect('/login/')
    else:
        s = bottle.request.environ.get('beaker.session')
        s['login'] = True
        s['username'] = username
        s.save()
        redirect('/')

@route("/logout/")
def logout():
    request.environ["beaker.session"].delete()
    redirect("/login/")
    return

#zaradi neznanih razlogov funkcija ne sprejme db parametra, ce uporabimo view,
#vendar pa dela pa s templatom
@route('/moje_ankete/', template="moje_ankete")
#@view('moje_ankete')
def moje_ankete(db):
    if bottle.request.environ.get('beaker.session').get("login") == None:
        redirect("/login/")
        return {"loggedin":False}

    s = bottle.request.environ.get('beaker.session')
    
    result = db.execute("""SELECT id, naslov, uvod FROM ankete
    INNER JOIN uporabniki
    ON ankete.uporabnik = uporabniki.username
    WHERE ankete.uporabnik = ? """, (s['username'],) )

    return {"loggedin":True, "data":result.fetchall()}

@route("/moje_ankete/<uid:int>/", template="anketa")
def izbrana_anketa(uid, db):
    if bottle.request.environ.get('beaker.session').get("login", False) == False:
        redirect("/login/")
        return {"loggedin":False}
    
    s = bottle.request.environ.get('beaker.session')
    result = db.execute("""SELECT
    vprasanja.id, vprasanja.naslov, vprasanja.vprasanja, vprasanja.tip
    FROM vprasanja
    INNER JOIN ankete
    ON vprasanja.anketa = ankete.id
    INNER JOIN uporabniki
    ON ankete.uporabnik = uporabniki.username
    WHERE ankete.uporabnik = ?  AND vprasanja.anketa = ? """, (s['username'], uid) )

    
    return {"loggedin":True, "data": result.fetchall(), "tipi":tipi_vprasanj}

@route('/anketa/<uid:int>', template='anketa')
#  @view('anketa')
def show_anketa(uid, db):
    result = list(db.execute("SELECT text, tip FROM vprasanja WHERE anketa=?",str(uid)))
    if result == []:
        abort(404)
    return {'vprasanja': map(list, result)}

@post("/anketa_shrani/<uid:int>/")
def save_anketa(uid, db):
    data = request.forms.get("seznam_vprasanj")
    print (data)
    db.execute("UPDATE vprasanja SET vprasanja=? WHERE id=?",(data,uid))
    db.commit()
    redirect("/moje_ankete/1/")
    
@route("/count")
def count():
    s = bottle.request.environ.get('beaker.session')
    s['visits'] = s.get('visits', 0) + 1
    s.save()
    return "{} obiskov".format(s['visits'])

#  @route('/count/')
#  def count():
#      s = bottle.request.environ.get('beaker.session')
#      s['test'] = s.get('test',0) + 1
#      s.save()
#      return 'Test counter: %d' % s['test']

@route('/')
@view('index')
def index():
    if bottle.request.environ.get('beaker.session').get("login") == None:
        redirect("/login/")
        return {"loggedin":False}
    return {"loggedin":True}
run(app=app)
