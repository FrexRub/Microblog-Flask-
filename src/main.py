from app import MyServer
from view_users import router as router_user

app = MyServer(__name__)
app.set_config()
app.register_blueprint(router_user, url_prefix="/api/users")


@app.route('/page_primer')
def welcome_text():
    return '<h1>Мне кажется, или я реально уже в браузере?!</h1>'


if __name__ == "__main__":
    app.run(debug=True)
