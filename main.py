import bottle
from bottle import view, route, run, Bottle, install
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


@route('/anketa/<uid:int>/', template='anketa')
#  @view('anketa')
def show_anketa(uid, db):
    result = list(db.execute("SELECT text FROM vprasanja WHERE anketa=?",uid))
#      result = list(db.execute("SELECT * FROM vprasanja"))
    if result == []:
        abort(404)
    return {'vprasanja': list(result)}

@route('/count/')
def count():
    s = bottle.request.environ.get('beaker.session')
    s['test'] = s.get('test',0) + 1
    s.save()
    return 'Test counter: %d' % s['test']

@route('/')
@view('index')
def index(): return

run(app=app)
