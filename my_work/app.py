from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'  # Використовуйте іншу базу даних, якщо потрібно
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

class FeedbackForm(FlaskForm):  # Зміний імпорт
    name = StringField('Ваше ім\'я', validators=[DataRequired()])
    feedback = TextAreaField('Ваш відгук', validators=[DataRequired()])
    submit = SubmitField('Надіслати')

@app.route('/', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        feedback_text = form.feedback.data
        feedback_entry = Feedback(name=name, feedback=feedback_text)
        db.session.add(feedback_entry)
        db.session.commit()
        flash('Ваш відгук був успішно збережений', 'success')
        return redirect(url_for('feedback'))
    
    feedback_entries = Feedback.query.all()
    return render_template('feedback.html', form=form, feedback_entries=feedback_entries)

if __name__ == '__main__':
    with app.app_context():  # Встановлюємо контекст додатку
        db.create_all()  # Створюємо таблицу
    app.run(debug=True)