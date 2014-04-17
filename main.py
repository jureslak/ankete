import bottle
from bottle import view, route, run, Bottle, install, static_file, post, request,redirect
from bottle_sqlite import SQLitePlugin
from beaker.middleware import SessionMiddleware

plugin = SQLitePlugin(dbfile='baza.db', keyword='db')
install(plugin)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3000,
    'session.data_dir': './session',
    'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)

@route('/skin/css/style.css')
def style():
    return static_file('style.css', root="skin/css/")

@route("/login/")
@view("login")
def login():
    s = bottle.request.environ.get('beaker.session')
    if s.get('login', False):
        redirect('/')
    return {}

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

@route('/anketa/<uid:int>/', template='anketa')
#  @view('anketa')
def show_anketa(uid, db):
    result = list(db.execute("SELECT text FROM vprasanja WHERE anketa=?",str(uid)))
    if result == []:
        abort(404)
    return {'vprasanja': map(list, result)}

@route("/count/")
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
    return

run(app=app)
