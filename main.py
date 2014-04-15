import bottle
from bottle import view, route, run, Bottle, install, static_file, post, request,redirect
from bottle_sqlite import SQLitePlugin
from beaker.middleware import SessionMiddleware

plugin = SQLitePlugin(dbfile='baza.db', keyword='db')
install(plugin)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './session',
    'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)
root = '/home/jureslak/bottle/'

@route('/skin/css/style.css')
def style():
    return static_file('skin/css/style.css', root=root)

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
    result = db.execute('SELECT * FROM uporabniki WHERE username=? AND password=?',(username,password));
    print (result)
    if result is None:
        redirect('/login/')
    else:
        s = bottle.request.environ.get('beaker.session')
        s['login'] = True
        s.save()
        redirect('/')

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
def index(): return

run(app=app)
