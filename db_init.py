from app import db
from models import Task, Reminder

if __name__ == '__main__':
    db.create_all()
    print('Banco inicializado (pomodoro.db)')
