import bottle
from bottle import view, route, run, Bottle, install, static_file, post, request,redirect
from bottle_sqlite import SQLitePlugin
from beaker.middleware import SessionMiddleware
from os import getcwd
from os.path import join

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

app = SessionMiddleware(bottle.app(), session_opts)

@route('<:re:.*>/skin/css/style.css')
def style():
    return static_file('style.css', root=join(getcwd(),"skin/css"))

@route('<:re:.*>/skin/js/script.js')
def js():
    return static_file('script.js', root=join(getcwd(),"skin/js"))


@route("/login")
@view("login")
def login():
    s = bottle.request.environ.get('beaker.session')
    if s.get('login', False):
        redirect('/')
        return {"loggedin":True}
    return {"loggedin":False}   


@post("/do_login")
def login(db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    result = db.execute('SELECT * FROM uporabniki WHERE username=? AND password=?',(username,password))
    data = result.fetchall()
    
    if len(data) == 0:
        redirect('/login')
    else:
        s = bottle.request.environ.get('beaker.session')
        s['login'] = True
        s['username'] = username
        s.save()
        redirect('/')

@route("<:re:.*>/logout")
def logout():
    request.environ["beaker.session"].delete()
    redirect("/login")
    return

#zaradi neznanih razlogov funkcija ne sprejme db parametra, ce uporabimo view,
#vendar pa dela pa s templatom
@route('/moje_ankete', template="moje_ankete")
#@view('moje_ankete')
def moje_ankete(db):
    if bottle.request.environ.get('beaker.session').get("login") == None:
        redirect("/login")
        return {"loggedin":False}

    s = bottle.request.environ.get('beaker.session')
    
    result = db.execute("""SELECT id, naslov, uvod FROM ankete
    INNER JOIN uporabniki
    ON ankete.uporabnik = uporabniki.username
    WHERE ankete.uporabnik = ? """, (s['username'],) )

    return {"loggedin":True, "data":result.fetchall()}

@route("/moje_ankete/<uid:int>", template="anketa")
def izbrana_anketa(uid, db):
    if bottle.request.environ.get('beaker.session').get("login") == None:
        redirect("/login")
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
        redirect("/login")
        return {"loggedin":False}
    return {"loggedin":True}
run(app=app)
