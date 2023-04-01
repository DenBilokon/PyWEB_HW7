from src.db import session


def create_data(model, name):
    data = model(name=name)
    session.add(data)
    session.commit()
    print(f"Додано: {data.name}")
    session.close()


def list_data(model):
    data = session.query(model).all()
    print("Список даних:")
    for s in data:
        print(s.id, s.name)
    return data


def update_data(model, id_, name):
    try:
        new_st = session.query(model).filter(model.id == id_).first()
        if new_st:
            new_st.fullname = name
            upd_st = session.merge(new_st)
            session.commit()
            print(f'Змінено дані {upd_st.id, upd_st.name}')
            session.close()
            return upd_st
        return None
    except Exception as e:
        print(f'Помилка: {e}')
        session.rollback()
        session.close()
        return None


def remove_data(model, id_):
    try:
        remove_st = session.query(model).filter(model.id == id_).first()
        if remove_st:
            print(f'Видалено дані: \n{remove_st.id} {remove_st.fullname}')
            r = session.query(model).filter(model.id == id_).delete()
            session.commit()
            session.close()
            return r
        return None
    except Exception as e:
        print(f'Помилка: {e}')
        session.rollback()
        session.close()
        return None

