from datetime import date, datetime, timedelta
from random import randint, choice

from sqlalchemy import select
from faker import Faker
from src.db import session

from src.models import Student, Teacher, Discipline, Group, Grade

disciplines = [
    'Астрологія',
    'Заклинання',
    'Захист від темних мистецтв',
    'Зілляваріння',
    'Історія Магії',
    'Травологія',
    'Пророцтва',
    'Польоти на мітлах'
]

groups = ['Гріффіндор', 'Слізерін', 'Пуффендуй', 'Когтевран']

teachers = [
    'Северус Снейп',
    'Аластор Грюм',
    'Мінерва МакГонагал',
    'Рубеус Хагрід',
    'Роланда Трюк'
]

NUMBER_STUDENTS = 50
fake = Faker('uk_UA')


def fill_data():
    def date_range(start: date, end: date) -> list:
        result = []
        current_date = start
        while current_date <= end:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result

    def seed_teachers():
        for teacher in teachers:
            session.add(Teacher(name=teacher))
        session.commit()

    def seed_disciplines():
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for discipline in disciplines:
            session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(NUMBER_STUDENTS):
            student = Student(name=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        start_date = datetime.strptime('2020-09-01', '%Y-%m-%d')
        end_date = datetime.strptime('2021-06-30', '%Y-%m-%d')
        d_range = date_range(start=start_date, end=end_date)
        discipline_ids = session.scalars(select(Discipline.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for d in d_range:
            random_id_discipline = choice(discipline_ids)
            random_ids_student = [choice(student_ids) for _ in range(len(disciplines))]

            for student_id in random_ids_student:
                grade = Grade(
                    grade=randint(1, 12),
                    date_of=d,
                    student_id=student_id,
                    discipline_id=random_id_discipline
                )
                session.add(grade)
        session.commit()

    seed_groups()
    seed_teachers()
    seed_disciplines()
    seed_students()
    seed_grades()


if __name__ == '__main__':
    fill_data()
