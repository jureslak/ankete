from bottle import view, route, run, Bottle, install
from bottle_sqlite import SQLitePlugin

plugin = SQLitePlugin(dbfile='baza.db', keyword='db')
install(plugin)

@route('/anketa/<uid:int>/', template='anketa')
#  @view('anketa')
def show_anketa(uid, db):
    result = list(db.execute("SELECT text FROM vprasanja WHERE anketa=?",uid))
#      result = list(db.execute("SELECT * FROM vprasanja"))
    if result == []:
        abort(404)
    return {'vprasanja': list(result)}

@route('/')
@view('index')
def index(): return

run()
