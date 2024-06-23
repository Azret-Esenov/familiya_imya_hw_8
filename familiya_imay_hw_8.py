import sqlite3


def create_connection(db_name):
    connection = None
    try:
        conn = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


def insert_country(connection, country):
    sql = 'INSERT INTO countries(title) VALUES (?)'
    try:
        cursor = connection.cursor()
        cursor.execute(sql, country)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def insert_city(connection, city):
    sql = '''INSERT INTO cities(title, area, country_id) VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, city)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def insert_student(connection, students):
    sql = '''INSERT INTO students (first_name,last_name, city_id) VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, students)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def show_cities(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT id, title FROM cities')
        cities = cursor.fetchall()
        for city in cities:
            print(f"{city[0]}. {city[1]}")
    except sqlite3.Error as e:
        print(e)


def show_students_by_city(connection, city_id):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT students.first_name, students.last_name, countries.title, cities.title, cities.area
            FROM students
            JOIN cities ON students.city_id = cities.id
            JOIN countries ON cities.country_id = countries.id
            WHERE cities.id = ?
        ''', (city_id,))
        students = cursor.fetchall()
        if students:
            print("\nСтуденты в выбранном городе:")
            for student in students:
                print(f"Имя: {student[0]} {student[1]}, Страна: {student[2]}, Город: {student[3]}, Площадь: {student[4]}")
        else:
            print("В выбранном городе нет студентов.")
    except sqlite3.Error as e:
        print(e)


sql_create_countries_table = '''CREATE TABLE countries(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(200) NOT NULL)'''

sql_create_cities_table = '''CREATE TABLE cities(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(200) NOT NULL,
area FLOAT DEFAULT 0,
country_id INTEGER REFERENCES countries(id) ON DELETE CASCADE)'''

sql_create_students_table = '''CREATE TABLE students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name VARCHAR(200) NOT NULL ,
last_name VARCHAR(200) NOT NULL ,
city_id INTEGER REFERENCES cities(id) ON DELETE CASCADE
)'''

my_connection = create_connection("hw8.db")

if my_connection:
    print("Connected to SQLite successfully!")
    # create_table(my_connection, sql_create_countries_table)
    # create_table(my_connection, sql_create_cities_table)
    # create_table(my_connection, sql_create_students_table)

    insert_country(my_connection, ('США',))
    insert_country(my_connection, ('Кыргызстан',))
    insert_country(my_connection, ('Германия',))

    insert_city(my_connection, ('Бишкек', 234.5, 2))
    insert_city(my_connection, ('Ош', 250.5, 1))
    insert_city(my_connection, ('Иссык-куль', 264.5, 3))
    insert_city(my_connection, ('Бостон', 224.5, 2))
    insert_city(my_connection, ('Чикаго', 214.5, 2))
    insert_city(my_connection, ('Берлин', 239.5, 1))
    insert_city(my_connection, ('Гамбург', 284.5, 3))

    insert_student(my_connection, ('Макс', 'Адамс', 1))
    insert_student(my_connection, ('Нурсултан', '1', 2))
    insert_student(my_connection, ('Джон', 'Хейз', 3))
    insert_student(my_connection, ('Крис', 'Адамс', 4))
    insert_student(my_connection, ('Омурбек', 'Абакиров', 5))
    insert_student(my_connection, ('Дмитрий', 'Одинцов', 6))
    insert_student(my_connection, ('Саша', 'Копылов', 7))
    insert_student(my_connection, ('Смит', 'Митчелл', 3))
    insert_student(my_connection, ('Дэвис', 'Кэмпбелл', 7))
    insert_student(my_connection, ('Урсула', 'Альцгеймер', 1))
    insert_student(my_connection, ('Ингрид', 'Альцгеймер', 1))
    insert_student(my_connection, ('Томас', 'Митчелл', 2))
    insert_student(my_connection, ('Гарсия', 'Лопес', 3))
    insert_student(my_connection, ('Азрет', 'Эсенов', 4))
    insert_student(my_connection, ('Алексей', 'Кузнецов', 7))

    while True:
        print("\nВы можете отобразить список студентов, выбрав ID города:")
        show_cities(my_connection)
        try:
            city_id = int(input("Введите ID города (0 для выхода): "))
            if city_id == 0:
                break
            elif 1 <= city_id <= 7:
                show_students_by_city(my_connection, city_id)
            else:
                print("Неверный ID города. Пожалуйста, повторите попытку.")
        except ValueError:
            print("Неверный ввод. Введите корректный ID города.")

    my_connection.close()
