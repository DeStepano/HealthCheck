from flask import Flask, request, render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospitals.db"
db.init_app(app)


class Hospital(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    disease: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    adress: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
    coord_x: Mapped[float] = mapped_column()
    coord_y: Mapped[float] = mapped_column()


with app.app_context():
    db.create_all()


@app.route('/pneumonia')
def get_data_pneumonia():
    results = db.session.execute(db.select(Hospital).filter_by(city='Saint Petersburg', disease='pneumonia'))
    def to_dict(hospital):
        return {"name": hospital[0].name, "disease": hospital[0].disease, "city": hospital[0].city, "adress": hospital[0].adress, "link": hospital[0].link ,"coord_x": hospital[0].coord_x, "coord_y": hospital[0].coord_y}
    results = tuple(map(to_dict, results))
    return jsonify(results)


@app.route('/diabetes')
def get_data_diabetes():
    results = db.session.execute(db.select(Hospital).filter_by(city='Saint Petersburg', disease='diabetes'))
    def to_dict(hospital):
        return {"name": hospital[0].name, "disease": hospital[0].disease, "city": hospital[0].city, "adress": hospital[0].adress, "link": hospital[0].link ,"coord_x": hospital[0].coord_x, "coord_y": hospital[0].coord_y}
    results = tuple(map(to_dict, results))
    return jsonify(results)


@app.route('/web_app')
def web_app():
    name_disease = request.args.get('name_disease')
    return render_template('map.html', data=name_disease)


@app.route('/create_hospital', methods = ['POST', 'GET'])
def create_hospital():
    if request.method == "POST":
        new_hospital = Hospital(
            name = request.form["name"],
            disease = request.form["disease"],
            city = request.form["city"],
            adress = request.form["adress"],
            link = request.form["link"],
            coord_x = request.form["coord_x"],
            coord_y = request.form["coord_y"],
        )
        try:
            db.session.add(new_hospital)
            db.session.commit()
            return render_template('create_hospital.html')
        except:
            return "При добавлении больницы произошла ошибка"
    else:
        return render_template('create_hospital.html')


if __name__ == "__main__":
    app.run(debug=True)