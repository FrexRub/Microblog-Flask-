from flask import Flask
from src.view_users import router as router_user

from database import db, db_url

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db.init_app(app=app)
app.register_blueprint(router_user, url_prefix="/api/users")

@app.route('/page_primer')
def welcome_text():
    return '<h1>Мне кажется, или я реально уже в браузере?!</h1>'

if __name__ == "__main__":
    app.run(debug=True)
