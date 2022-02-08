from flask import Flask
from views import auth, homepage, companies, contact, positions, shifts
from database import database
from views.auth import login_manager

app = Flask(__name__)

# config
app.config.from_object('config')
database.init_app(app)
login_manager.init_app(app)

# views
app.register_blueprint(auth.bp)
app.register_blueprint(homepage.bp)
app.register_blueprint(companies.bp)
app.register_blueprint(contact.bp)
app.register_blueprint(positions.bp)
app.register_blueprint(shifts.bp)

if __name__ == '__main__':
    app.run()
