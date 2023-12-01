from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from ski_history_scraper import SkiHistory

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alta_web_scrapper.db"
db = SQLAlchemy()
db.init_app(app)


class Users(db.Model):
    userId = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    userName = db.Column(db.String, nullable=False, unique=True)
    web_id = db.Column(db.String, unique=True)
    yearly_elevation = db.Column(db.Integer)
    days_skied = db.Column(db.Integer)
    average_ft = db.Column(db.Integer)
    
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
    run_elevation = db.Column(db.Integer, nullable=False)
    chairlift = db.Column(db.String, nullable=False)
    time = db.Column(db.Time, nullable=False)
    
@app.route('/api/login', methods=["POST"])
def login():
    body = request.get_json()
    with app.app_context():
        db.create_all()
        userCheck = db.session.execute(db.select(Users).where(Users.userId == body['userId'])).scalar()
        if not userCheck: 
            user = Users(
                userId = body['userId'], 
                email = body['email'],
                userName = body['email']
            )
            db.session.add(user)
            db.session.commit()
        return {
        "response": "success"
        }
        
@app.route('/api/saveWebId', methods=["POST"])
def createWebId():
    body = request.get_json()
    with app.app_context():
        userCheck = db.session.execute(db.select(Users).where(Users.web_id == body['web_id'])).scalar()
        if not userCheck:
            db.create_all()
            user_to_update = db.session.execute(db.select(Users).where(Users.userId == body['userId'])).scalar()
            user_to_update.web_id = body['web_id']
            db.session.commit()
            initial_user_ski_data_sync(body['userId'], body['web_id'])
            return {"response": "success"}
        else:
            return {"response": "Web ID Already Used"}


def initial_user_ski_data_sync(userId, web_id):
    ski_history = SkiHistory()
    ski_history.login()
    ski_history.enter_web_id(web_id)
    total_ft_and_days = ski_history.get_ski_history()
    

    # Yearly Totals
    total_days = total_ft_and_days.text.split("SKIED: ")[1]
    total_ft = total_ft_and_days.text.split("TOTAL VERTICAL FEET ")[1].split(", NUMBER")[0]
    average_ft_per_day = int(total_ft.replace(",", "")) / int(total_days)
    

    
    
    user_to_update = db.session.execute(db.select(Users).where(Users.userId == userId)).scalar()
    user_to_update.yearly_elevation = int(total_ft.replace(",", ""))
    user_to_update.average_ft = int(average_ft_per_day)
    user_to_update.days_skied = int(total_days)
    db.session.commit()



    day_list = ski_history.get_each_day()
        
    # Runs Each Day
    day_list = ski_history.get_runs_each_day(day_list)
    print(day_list)
    ski_history.driver.quit()
                
if __name__ == "__main__":
    app.run(debug=True)
