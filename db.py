from flask_sqlalchemy import SQLAlchemy

class SkiDb:
    def __init__(self):
        self.db = SQLAlchemy()
        
        
class Users(SkiDb.db.Model):
    userId = SkiDb.db.Column(SkiDb.db.Integer, primary_key=True)
    email = SkiDb.db.Column(SkiDb.db.String, unique=True, nullable=False)
    userName = SkiDb.db.Column(SkiDb.db.String, nullable=False, unique=True)
    web_id = SkiDb.db.Column(SkiDb.db.String, unique=True)
    yearly_elevation = SkiDb.db.Column(SkiDb.db.Integer)
    days_skied = SkiDb.db.Column(SkiDb.db.Integer)
    average_ft = SkiDb.db.Column(SkiDb.db.Integer)
    
# class DaySummaryData(skiDb.db.Model):
#     dailyDataId = db.Column(db.Integer, primary_key=True)
#     userId = db.Column(db.Integer, nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     daily_elevation = db.Column(db.Integer, nullable=False)
#     daily_runs = db.Column(db.Integer, nullable=False)
    
# class DailySkiData(skiDb.db.Model):
#     runDataId = db.Column(db.Integer, primary_key=True)
#     dailyDataId = db.Column(db.Integer, nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     run_elevation = db.Column(db.Integer, nullable=False)
#     chairlift = db.Column(db.String, nullable=False)
#     time = db.Column(db.Time, nullable=False)