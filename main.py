# 1. Создать таблицу countries (страны) c колонками id первичный ключ автоинкрементируемый и колонка title с текстовым не пустым названием страны.
# 2. Добавить 3 записи в таблицу countries
# 3. Добавить таблицу cities (города) c колонками id первичный ключ автоинкрементируемый, колонка title с текстовым не пустым названием города и колонка area площадь города не целочисленного типа данных со значением по умолчанием 0, а также колонка country_id с внешним ключом на таблицу countries.
# 4. Добавить 7 городов различных стран
# 5. Создать таблицу employees (сотрудники) c колонками id первичный ключ автоинкрементируемый, колонка first_name (имя) с текстовым не пустым значением,  колонка last_name (фамилия) с текстовым не пустым значением, а также колонка city_id с внешним ключом на таблицу cities.
# 6. Добавить 15 сотрудников проживающих в разных городах.
# В пунктах с 1го по 6й можно использовать любой вариант для работы в СУБД SqlLite (Из кода в Python или SQL запросами или через любую программу с графическим интерфейсом для управления БД).
# 7. Написать программу в Python, которая при запуске бы отображала фразу “Вы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:”
# 8. Ниже фразы программа должна распечатывать список городов из вашей базы данных следующим образом
# Бишкек
# Ош
# Берлин
# Пекин
# и тд…
# 9. После ввода определенного id города программа должна найти всех сотрудников из вашей базы данных проживающих в городе выбранного пользователем и отобразить информацию о них в консоли (Имя, фамилия, страна и город проживания)

import sqlite3


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
                    CREATE TABLE countries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL
                    );
                    ''')

    cursor.execute("""
                CREATE TABLE cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    area REAL DEFAULT 0,
                    country_id INTEGER,
                    FOREIGN KEY (country_id) REFERENCES countries (id)
                );
                """)

    cursor.execute("""
                CREATE TABLE employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    city_id INTEGER,
                    FOREIGN KEY (city_id) REFERENCES cities (id)
                );
                """)

    connection.commit()
    print("Done!")


def insert_data(connection):
    cursor = connection.cursor()

    cursor.execute("""
                    INSERT INTO countries (title) 
                    VALUES ('Kyrgyzstan'), 
                        ('Kazakstan'), 
                        ('Uzbekstan');
                    """)

    cursor.execute("""
                    INSERT INTO cities (title, area, country_id)
                    VALUES ("London", 42001, 1),
                        ("Manchester city", 43002, 1),
                        ("Tottenham", 44003, 1),
                        ("Chelsi", 45004, 1),
                        ("Liverpool", 46005, 1),
                        ("Oxford", 47006, 1),
                        ("Nottingham", 48007, 1),

                        ("NURSULTAN", 999999, 2),
                        ("Almaty", 12000, 2),
                        ("Astana", 34555, 2),
                        ("Shymkent", 22000, 2),
                        ("Atyrau", 92000, 2),

                        ("Pekin", 92000, 3),
                        ("Urumchi", 34, 3),
                        ("NEZNAU_CHTO_DALSHE", 4233, 3);
                    """)

    cursor.execute("""
                    INSERT INTO employees (first_name, last_name, city_id)
                    VALUES  ("NURSULTAN", "SABIRZHANOV", 7),
                            ("Atynay", "Toktorova", 7),
                            ("John", "Doe", 1),
                            ("Jane", "Smith", 2),
                            ("Bob", "Johnson", 1),
                            ("Alice", "Brown", 2),
                            ("Tom", "Wilson", 13),
                            ("Sara", "Garcia", 2),
                            ("Mike", "Martinez", 3),
                            ("Emily", "Davis", 3),
                            ("David", "Lee", 8),
                            ("Karen", "Taylor", 8),
                            ("Brian", "Miller", 12),
                            ("Lisa", "Anderson", 9),
                            ("Paul", "Clark", 7),
                            ("Amy", "Scott", 7),
                            ("Mark", "Robinson", 5);
                    """)

    connection.commit()
    print("Done!")


def program(connection):
    while True:
        print("""
            You can display a list of employees by the selected city id 
            from the list of cities below, to exit the program enter 0 
        _________________________________
        """)

        cursor = connection.cursor()

        cursor.execute("""SELECT id, title FROM cities;""")
        for id, city in cursor.fetchall():
            print(f"{city} - {id}")

        id = int(input("\nEnter id: "))

        if id == 0:
            print("Goodbye!")
            break
        else:
            cursor.execute("""
                SELECT e.first_name, e.last_name, ci.title, co.title
                FROM employees e 
                INNER JOIN cities ci
                ON e.city_id = ci.id and e.city_id == {id}
                INNER JOIN countries co
                ON ci.country_id = co.id;
            """.format(id=id))
            employees = cursor.fetchall()
            if employees:
                print()
                for name, surname, city, country in employees:
                    print(f"Fullname: {surname} {name}\nCity: {city}\nCountry: {country}\n")

                question = input("Are you want to continue?(y/n)")
                if question == "y":
                    continue
                else:
                    print("GoodBye!")
                    break
            else:
                print("There are not employees from this city!")
                question = input("Are you want to continue?(y/n)")
                if question == "y":
                    continue
                else:
                    print("GoodBye!")
                    break


def main():
    connect = sqlite3.connect("altinay_db.db")

    #create_tables(connection=connect)
    #insert_data(connection=connect)

    program(connection=connect)


if __name__ == "__main__":
    main()
