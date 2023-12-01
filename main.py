from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ski_history_scraper import SkiHistory

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alta_web_scrapper.db"
db = SQLAlchemy()
db.init_app(app)

class Users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    userName = db.Column(db.String, nullable=False, unique=True)
    web_id = db.Column(db.String, nullable=False, unique=True)
    yearly_elevation = db.Column(db.Integer, nullable=False)
    days_skied = db.Column(db.Integer, nullable=False)
    average_ft = db.Column(db.Integer, nullable=False)
    
class DailySkiData(db.Model):
    dailyDataId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    daily_elevation = db.Column(db.Integer, nullable=False)
    daily_runs = db.Column(db.Integer, nullable=False)
    
class DailySkiData(db.Model):
    runDataId = db.Column(db.Integer, primary_key=True)
    dailyDataId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    run_elevation = db.Column(db.Integer, nullable=False)
    chairlift = db.Column(db.String, nullable=False)
    time = db.Column(db.Time, nullable=False)
    


ski_history = SkiHistory()
ski_history.login()
ski_history.enter_web_id()
total_ft_and_days = ski_history.get_ski_history()

# Yearly Totals
total_days = total_ft_and_days.text.split("SKIED: ")[1]
total_ft = total_ft_and_days.text.split("TOTAL VERTICAL FEET ")[1].split(", NUMBER")[0]
average_ft_per_day = int(total_ft.replace(",", "")) / int(total_days)

day_list = ski_history.get_each_day()
    
# Runs Each Day
day_list = ski_history.get_runs_each_day(day_list)
print(day_list)
            
        