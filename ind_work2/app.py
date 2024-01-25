from flask import Flask, request, render_template, redirect, url_for, Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()

cars_bp = Blueprint('cars', __name__)
api_cars = Api(cars_bp)


class CarResource(Resource):
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        return {'id': car.id, 'brand': car.brand, 'model': car.model, 'year': car.year}

    def put(self, car_id):
        parser = reqparse.RequestParser()
        parser.add_argument('brand', type=str, required=True, help='Brand cannot be blank')
        parser.add_argument('model', type=str, required=True, help='Model cannot be blank')
        parser.add_argument('year', type=int, required=True, help='Year cannot be blank')

        args = parser.parse_args()
        car = Car.query.get_or_404(car_id)
        car.brand = args['brand']
        car.model = args['model']
        car.year = args['year']
        db.session.commit()
        return {'message': 'Car updated successfully'}

    def delete(self, car_id):
        car = Car.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        return {'message': 'Car deleted successfully'}


class CarsResource(Resource):
    def get(self):
        cars = Car.query.all()
        cars_data = [{'id': car.id, 'brand': car.brand, 'model': car.model, 'year': car.year} for car in cars]
        return jsonify(cars_data)

    def post(self):
        try:
            if request.content_type == 'application/json':
                data = request.get_json()
            else:
                data = request.form
            if 'brand' not in data or 'model' not in data or 'year' not in data:
                return {'message': 'Missing required data'}, 400
            new_car = Car(brand=data['brand'], model=data['model'], year=data['year'])
            db.session.add(new_car)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return {'message': str(e)}, 500


api_cars.add_resource(CarResource, '/car/<int:car_id>')
api_cars.add_resource(CarsResource, '/cars', endpoint='cars')


@cars_bp.route('/')
def get_cars():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)


@cars_bp.route('/delete/<int:car_id>', methods=['GET'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('cars.get_cars'))


@cars_bp.route('/update/<int:car_id>', methods=['GET', 'POST'])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)

    if request.method == 'POST':
        car.brand = request.form['brand']
        car.model = request.form['model']
        car.year = request.form['year']
        db.session.commit()
        return redirect(url_for('cars.get_cars'))

    return render_template('edit_car.html', car=car)


app.register_blueprint(cars_bp)

if __name__ == '__main__':
    app.run(debug=True)
