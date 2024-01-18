
from flask import Flask , request 
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from jose import JWTError, jwt



app = Flask(__name__)
app.config.from_pyfile('config.py')  # Завантаження конфігурації
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db' 
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route('/')
def home():
    return "Welcome to the Car API"


class CarModel:
    def __init__(self, car_id, brand, model, year):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.year = year
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password_hash = Bcrypt().generate_password_hash(password).decode('utf-8')
        self.role = role


# Приклад бази даних
cars_db = {
    1: CarModel(1, 'Toyota', 'Camry', 2022),
    2: CarModel(2, 'Honda', 'Civic', 2021),
    3: CarModel(3, 'Ford', 'Mustang', 2020),
}

# Приклад користувачів і їхніх ролей
users = {
    'user1': {'password': 'password1', 'role': 'user'},
    'admin': {'password': 'adminpassword', 'role': 'admin'}
}

# Функції для роботи з JWT
def authenticate(username, password):
    user = users.get(username, None)
    if user and user['password'] == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return {'username': user_id}

# Парсер для обробки вхідних даних
parser = reqparse.RequestParser()
parser.add_argument('brand', type=str, required=True, help='Brand is required')
parser.add_argument('model', type=str, required=True, help='Model is required')
parser.add_argument('year', type=int, required=True, help='Year is required')

# Приклад ресурсу
class CarResource(Resource):
    def get(self, car_id):
        car = cars_db.get(car_id)
        if car:
            return {'car_id': car.car_id, 'brand': car.brand, 'model': car.model, 'year': car.year}
        return {'message': 'Car not found'}, 404

    def put(self, car_id):
        args = parser.parse_args()
        if car_id not in cars_db:
            return {'message': 'Car not found'}, 404

        # Перевірка токену для оновлення
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'message': 'Unauthorized'}, 401
        token = auth_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if decoded_token['username'] != 'admin':
                return {'message': 'Unauthorized'}, 403
        except JWTError:
            return {'message': 'Unauthorized'}, 401

        car = cars_db[car_id]
        car.brand = args['brand']
        car.model = args['model']
        car.year = args['year']
        return {'car_id': car.car_id, 'brand': car.brand, 'model': car.model, 'year': car.year}

    def delete(self, car_id):
        if car_id not in cars_db:
            return {'message': 'Car not found'}, 404

        # Перевірка токену для видалення
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'message': 'Unauthorized'}, 401
        token = auth_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if decoded_token['username'] != 'admin':
                return {'message': 'Unauthorized'}, 403
        except JWTError:
            return {'message': 'Unauthorized'}, 401

        del cars_db[car_id]
        return {'message': 'Car deleted successfully'}
    
    def post(self, car_id):
        args = parser.parse_args()
        new_car_id = max(cars_db.keys()) + 1
        new_car = CarModel(new_car_id, args['brand'], args['model'], args['year'])
        cars_db[new_car_id] = new_car
        return {'car_id': new_car.car_id, 'brand': new_car.brand, 'model': new_car.model, 'year': new_car.year}, 201

# Додаємо ресурс до API
api.add_resource(CarResource, '/cars/<int:car_id>')

if __name__ == '__main__':
    app.run(debug=True)
