from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///pomodoro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

db = SQLAlchemy(app)

from models import Task, Reminder

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    reminders = Reminder.query.filter(Reminder.when >= datetime.utcnow()).order_by(Reminder.when).all()
    return render_template('index.html', tasks=tasks, reminders=reminders)

# Tasks CRUD
@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.form.get('title')
    if not title:
        flash('Título é obrigatório', 'error')
        return redirect(url_for('index'))
    t = Task(title=title)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    t = Task.query.get_or_404(task_id)
    t.done = not t.done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('index'))

# Reminders
@app.route('/reminders', methods=['POST'])
def create_reminder():
    title = request.form.get('title')
    when = request.form.get('when')
    if not title or not when:
        flash('Título e data/hora obrigatórios', 'error')
        return redirect(url_for('index'))
    dt = datetime.fromisoformat(when)
    r = Reminder(title=title, when=dt)
    db.session.add(r)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/reminders/next')
def api_next_reminder():
    r = Reminder.query.filter(Reminder.when >= datetime.utcnow()).order_by(Reminder.when).first()
    if not r:
        return jsonify({}), 204
    return jsonify({
        'id': r.id,
        'title': r.title,
        'when': r.when.isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
