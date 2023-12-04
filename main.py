from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from ski_history_scraper import SkiHistory
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alta_web_scrapper.db"
db = SQLAlchemy()
db.init_app(app)


class Users(db.Model):
    userId = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    userName = db.Column(db.String, unique=True)
    web_id = db.Column(db.String, unique=True)
    yearly_elevation = db.Column(db.Integer)
    days_skied = db.Column(db.Integer)
    average_ft = db.Column(db.Integer)
    collins = db.Column(db.Integer)
    wildcat = db.Column(db.Integer)
    sunnyside = db.Column(db.Integer)
    supreme = db.Column(db.Integer)
    sugarloaf = db.Column(db.Integer)
    
class DailySkiData(db.Model):
    dailyDataId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    daily_elevation = db.Column(db.Integer, nullable=False)
    daily_runs = db.Column(db.Integer, nullable=False)
    
class runSkiData(db.Model):
    runDataId = db.Column(db.Integer, primary_key=True)
    dailyDataId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    chairlift = db.Column(db.String, nullable=False)
    time = db.Column(db.Time, nullable=False)
    userId = db.Column(db.String, nullable=False)
    
@app.route('/api/login', methods=["POST"])
def login():
    body = request.get_json()
    with app.app_context():
        db.create_all()
        userCheck = db.session.execute(db.select(Users).where(Users.userId == body['userId'])).scalar()
        if not userCheck: 
            user = Users(
                userId = body['userId'], 
                email = body['email']
            )
            db.session.add(user)
            db.session.commit()
        return {
        "response": "success"
        }
        
@app.route('/api/saveWebId', methods=["POST"])
async def createWebId():
    body = request.get_json()
    with app.app_context():
        userCheck = db.session.execute(db.select(Users).where(Users.web_id == body['web_id'])).scalar()
        if not userCheck:
            db.create_all()
            user_to_update = db.session.execute(db.select(Users).where(Users.userId == body['userId'])).scalar()
            user_to_update.web_id = body['web_id']
            db.session.commit()
            initial_sync_res = await initial_user_ski_data_sync(body['userId'], body['web_id'])
            if initial_sync_res == False:
                return {"response": "Web ID Not Valid. Try Again"}  
            return {"response": "success"}
        else:
            return {"response": "Web ID Already Used"}
        
@app.route('/api/saveUsername', methods=["POST"])
async def createUsername():
    body = request.get_json()
    with app.app_context():
        userCheck = db.session.execute(db.select(Users).where(Users.userName == body['userName'])).scalar()
        if not userCheck:
            db.create_all()
            user_to_update = db.session.execute(db.select(Users).where(Users.userId == body['userId'])).scalar()
            user_to_update.userName = body['userName']
            db.session.commit()
            return {"response": "success"}
        else:
            return {"response": "Username Already Used"}


async def initial_user_ski_data_sync(userId, web_id):
    # Start Web Scraper
    ski_history = SkiHistory()
    cookies = ski_history.login()
    seasonIds = ski_history.getSeasonId(web_id, cookies["cookieString"], cookies["xsrf_token"])
    seasonId = seasonIds["transactions"][0]
    season_ski_history = ski_history.getSkiHistory(seasonId["NPOSNO"], seasonId["NPROJNO"], seasonId["NSERIALNO"], seasonId["SZVALIDFROM"], cookies["cookieString"], cookies["xsrf_token"])
    
    
    # Yearly Totals
    yearly_elevation = 0
    yearly_runs = 0
    yearly_collins = 0
    yearly_sunnyside = 0
    yearly_wildcat = 0
    yearly_supreme = 0
    yearly_sugarloaf = 0
    yearly_days_skied = 0
    
    for day in season_ski_history["rides"]:
        yearly_days_skied += 1
        daily_elevation = int(day[0]["total"])
        daily_runs = len(day)
        dataObj = datetime.strptime(day[0]["SZDATEOFRIDE"], '%Y-%m-%d')
        dailyDataId = await save_daily_totals(date=dataObj, feet=daily_elevation, total_runs=daily_runs, userId=userId)
        for ride in day:
            yearly_elevation += int(ride["NVERTICALFEET"])
            daily_elevation += int(ride["NVERTICALFEET"])
            daily_runs += 1
            yearly_runs += 1
            
            if ride["SZPOENAME"] == "Wildcat":
                yearly_wildcat += 1
            elif ride["SZPOENAME"] == "Collins":
                yearly_collins += 1
            elif ride["SZPOENAME"] == "Sunnyside":
                yearly_sunnyside += 1
            elif ride["SZPOENAME"] == "Supreme":
                yearly_supreme += 1
            else:
                yearly_sugarloaf += 1
                
            time_object = datetime.strptime(ride["SZTIMEOFRIDE"], '%H:%M:%S')
            sqlalchemy_time = time_object.time()
            await save_run(dailyDataId=dailyDataId, lift=ride["SZPOENAME"], time=sqlalchemy_time, userId=userId, date=dataObj)
            
    average_ft_per_day = yearly_elevation / yearly_days_skied
    user_to_update = db.session.execute(db.select(Users).where(Users.userId == userId)).scalar()
    user_to_update.yearly_elevation = yearly_elevation
    user_to_update.average_ft = int(average_ft_per_day)
    user_to_update.days_skied = yearly_days_skied
    user_to_update.collins = yearly_collins
    user_to_update.wildcat = yearly_wildcat
    user_to_update.sunnyside = yearly_sunnyside
    user_to_update.supreme = yearly_supreme
    user_to_update.sugarloaf = yearly_sugarloaf
    db.session.commit()
    return True

async def save_daily_totals(date, feet, total_runs, userId):
    dayCheck = db.session.execute(db.select(DailySkiData).where((DailySkiData.date == date.strftime('%Y-%m-%d')) and (DailySkiData.userId == userId))).scalar()
    if dayCheck == None:
        dailyData = DailySkiData(
            userId = userId,
            date = date,
            daily_elevation = feet,
            daily_runs = total_runs
        )
        db.session.add(dailyData)
        db.session.commit()
        return dailyData.dailyDataId
    return dayCheck.dailyDataId
    
async def save_run(dailyDataId, lift, time, userId, date):
    runCheck = db.session.execute(db.select(runSkiData).where((runSkiData.time == time) and (DailySkiData.userId == userId))).scalar()
    if runCheck == None:
        runData = runSkiData(
            dailyDataId = dailyDataId,
            date = date,
            chairlift = lift,
            time = time,
            userId = userId
        )
        db.session.add(runData)
        db.session.commit()
    return


@app.route('/api/getUserSnowData/<userId>', methods=["GET"])
async def getUserSnowData(userId):
    user = db.session.execute(db.select(Users).where(Users.userId == userId)).scalar()
    print(user)
    return {
        "userId": user.userId,
        "email": user.email,
        "userName": user.userName,
        "web_id": user.web_id,
        "yearly_elevation": user.yearly_elevation,
        "days_skied": user.days_skied,
        "average_ft": user.average_ft,
        "collins": user.collins,
        "wildcat": user.wildcat,
        "sugarloaf": user.sugarloaf,
        "sunnyside": user.sunnyside,
        "supreme": user.supreme
    }
    
@app.route('/api/lastDay/<userId>', methods=["GET"])
async def getUserMostRecentDay(userId):
    lastDay = db.session.execute(db.select(DailySkiData).where(DailySkiData.userId == userId).order_by(DailySkiData.date.desc())).scalar()
    print(lastDay)
    return {
        "dailyDataId": lastDay.dailyDataId,
        "userId": lastDay.userId,
        "date": lastDay.date.strftime('%m/%d/%Y'),
        "daily_elevation": lastDay.daily_elevation,
        "daily_runs": lastDay.daily_runs
    }
                
if __name__ == "__main__":
    app.run(debug=True)
