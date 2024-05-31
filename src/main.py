from app import MyServer
from view_users import router as router_user

app = MyServer(__name__)
app.set_config()
app.register_blueprint(router_user, url_prefix="/api/users")

if __name__ == "__main__":
    app.run(debug=True)
