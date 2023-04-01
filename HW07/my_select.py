from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Discipline, Group, Grade
from src.db import session


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    result = session.query(Student.fullname,
                           func.round(func.avg(Grade.grade), 2) \
                           .label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()

    return result


# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(discipline_id: int):
    result = session.query(Discipline.name,
                           Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')
                           ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return result


# Знайти середній бал у групах з певного предмета.
def select_3(discipline_id: int):
    result = session.query(Group.name,
                           Discipline.name,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')
                           ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Group.name, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .all()
    return result


# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).scalar() \

    return result


# найти які курси читає певний викладач.
def select_5(teacher_id: int):
    result = session.query(Teacher.fullname,
                           Discipline.name
                           ) \
        .select_from(Discipline) \
        .join(Teacher) \
        .filter(Teacher.id == teacher_id)\
        .all()
    return result


# Знайти список студентів у певній групі.
def select_6(group_id: int):
    result = session.query(Student.fullname,
                           Group.name) \
        .select_from(Student) \
        .join(Group) \
        .filter(Group.id == group_id) \
        .order_by(Student.fullname.asc()).all()
    return result


# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(discipline_id: int, group_id: int):
    result = session.query(Student.fullname,
                           Group.name,
                           Discipline.name,
                           Grade.grade,
                           Grade.date_of) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id)) \
        .order_by(Student.fullname.asc(), Grade.date_of.asc()).all()
    return result


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id: int):
    result = session.query(Teacher.fullname,
                           Discipline.name,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')
                           ) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(Teacher.id == teacher_id) \
        .group_by(Teacher.fullname, Discipline.name) \
        .order_by(desc('avg_grade')).all()
    return result


# Знайти список курсів, які відвідує певний студент.
def select_9(student_id: int):
    result = session.query(Student.fullname,
                           Discipline.name) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Student.id == student_id) \
        .group_by(Student.fullname, Discipline.name) \
        .order_by(Student.fullname.asc(), Discipline.name.asc()).all()
    return result


# Список курсів, які певному студенту читає певний викладач.
def select_10(student_id: int, teacher_id: int):
    result = session.query(Student.fullname,
                           Teacher.fullname,
                           Discipline.name) \
        .select_from(Grade) \
        .join(Student) \
        .join(Group) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(and_(Student.id == student_id, Teacher.id == teacher_id)) \
        .group_by(Student.fullname, Teacher.fullname, Discipline.name).all()
    return result


# Середній бал, який певний викладач ставить певному студентові.
def select_11(teacher_id: int, student_id: int):
    result = session.query(Teacher.fullname,
                           Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')
                           ) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .join(Student) \
        .filter(and_(Teacher.id == teacher_id, Student.id == student_id))\
        .group_by(Student.fullname, Teacher.fullname, Discipline.name).all()
    return result


# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12(discipline_id: int, group_id: int):
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    result = session.query(Discipline.name,
                           Student.fullname,
                           Group.name,
                           Grade.date_of,
                           Grade.grade
                           ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)) \
        .order_by(desc(Grade.date_of)) \
        .all()
    return result


if __name__ == '__main__':
    print(select_12(17, 21))
