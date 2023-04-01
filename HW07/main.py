import argparse
from src.crud import create_data, list_data, update_data, remove_data
from src.models import Teacher, Student, Discipline, Group

parser = argparse.ArgumentParser(description='Todo APP')
parser.add_argument('--action', help='Command: create, update, list, remove')
parser.add_argument('-m', help='Command: Teacher, Student, Discipline, Group')
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--grade')

arguments = parser.parse_args()

my_arg = vars(arguments)

action = my_arg.get('action')
model = my_arg.get('m')
_id = my_arg.get('id')
name = my_arg.get('name')


def main():
    data_model = None
    match model:
        case 'Student':
            data_model = Student
        case 'Teacher':
            data_model = Teacher
        case 'Discipline':
            data_model = Discipline
        case 'Group':
            data_model = Group

    match action:
        case 'create':
            create_data(data_model, name)
        case 'list':
            list_data(data_model)
        case 'update':
            update_data(data_model, _id, name)
        case 'remove':
            remove_data(data_model, _id)


if __name__ == '__main__':
    main()
