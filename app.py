import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///weather.db'
db = SQLAlchemy(app)

class City(db.Model):
  id= db.Column(db.Integer, primary_key= True)
  name= db.Column(db.String(50),nullable = False)

@app.route('/',methods= ['GET','POST'])
def index():
  if request.method == 'POST':
    newCity= request.form.get('city')

    if newCity:
      new_city_obj=City(name=newCity)
      db.session.add(new_city_obj)
      db.session.commit()

  cities = City.query.all()

  url= "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=f736811e918ca981c13e61311f520686"
  
  weather_data= []
  for city in cities:
    r = requests.get(url.format(city.name)).json()

    weather = {
      'city':r['name'],
      'temperature': r['main']['temp'],
      'description': r['weather'][0]['main'],
    }

    weather_data.append(weather)

  return render_template("weather.html", weather_data = weather_data)

if __name__ == "__main__":
	app.run(debug=True)