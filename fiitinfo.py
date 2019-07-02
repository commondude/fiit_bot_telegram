# Расписание
"""
Словари с расписанием по
верхней schedule_up
нижней schedule_down
неделе. Дни недели пн-птн по номерам 0-4
"""
schedule_up = {
      0:['Непрерывная математика','Непрерывная математика'],
      1:['Основы программирования(практикум)','Основы программирования(практикум)'],
      2:['Математическая логика','Математическая логика'],
      3:['Основы программирования','Язык программирования C%2B%2B'],
      4:['Самостоятельная работа','Самостоятельная работа'],
      }
schedule_down = {
      0:['Непрерывная математика','-'],
      1:['Иностранный язык','Иностранный язык'],
      2:['Математическая логика','Математическая логика'],
      3:['Основы программирования','Язык программирования C%2B%2B'],
      4:['Самостоятельная работа','Самостоятельная работа'],
      }
week_days = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
]
# Список группы
"""
Список со словарями с информацией о студентах
имя - firstname
фамилия - surname
отчество - patronymic
номер телефона - phone
номер в журнале - journal_number

"""
students = [
    {
        'firstname' : 'Бабенко' , 'surname' : 'Виктор', 'patronymic' : 'Петрович',
         'phone' : '+7 950 861 08 74', 'journal_number' : '1',

    },
    {
        'firstname' : 'Баев', 'surname' : 'Александр', 'patronymic' : 'Дмитриевич',
         'phone' : '+7 960 450 50 59', 'journal_number' : '2',

    },
    {
        'firstname' : 'Белкин', 'surname' : 'Александр', 'patronymic' : 'Игоревич',
         'phone' : '+7 908 179 54 80', 'journal_number' : '3',

    },
    {
        'firstname' : 'Воротий', 'surname' : 'Сергей', 'patronymic' : 'Олегович',
         'phone' : '+7 918 588 43 44', 'journal_number' : '4',

    },
    {
        'firstname' : 'Грошевой', 'surname' : 'Сергей', 'patronymic' : 'Владимирович',
         'phone' : '+7 918 511 54 16', 'journal_number' : '5',

    },
    {
        'firstname' : 'Кубышкин', 'surname' : 'Александр', 'patronymic' : 'Николаевич',
         'phone' : '', 'journal_number' : '7',

    },
    {
        'firstname' : 'Опимах', 'surname' : 'Александр', 'patronymic' : 'Сергеевич',
         'phone' : '+7 989 532 36 19', 'journal_number' : '8',

    },
    {
        'firstname' : 'Рябов', 'surname' : 'Алексей', 'patronymic' : 'Дмитриевич',
         'phone' : '+7 988 535 94 69', 'journal_number' : '9',

    },
    {
        'firstname' : 'Самойленко', 'surname' : 'Григорий', 'patronymic' : 'Павлович',
         'phone' : '+7 908 179 51 66', 'journal_number' : '10',

    },
    {
        'firstname' : 'Супрунов', 'surname' : 'Юрий', 'patronymic' : 'Владимирович',
         'phone' : '', 'journal_number' : '11',

    },
    {
        'firstname' : 'Сюндюков', 'surname' : 'Вадим', 'patronymic' : 'Ильдарович',
         'phone' : '+7 961 277 37 85', 'journal_number' : '12',

    },
    {
        'firstname' : 'Тарасов', 'surname' : 'Александр', 'patronymic' : 'Игоревич',
         'phone' : '+7 989 500 99 45', 'journal_number' : '13',

    },
    {
        'firstname' : 'Шаповалов', 'surname' : 'Александр', 'patronymic' : 'Сергеевич',
         'phone' : '+7 988 565 15 54', 'journal_number' : '14',

    },
    {
        'firstname' : 'Ярцев', 'surname' : 'Илья', 'patronymic' : 'Александрович',
         'phone' : '+7 928 129 36 18 ', 'journal_number' : '16',

    },
    {
        'firstname' : 'Ткаченко', 'surname' : 'Сергей', 'patronymic' : '',
         'phone' : '+7 929 815 31 92 ', 'journal_number' : '17',

    },

]


# Список словарей предметов и преподователей
"""
Список словарей предметов и преподователей
наименование дисциплины - name
фио учителя - teacher
номер телефона учителя - phone
"""
disciplines = [
    {
        'name' : 'Непрерывная математика',
        'teacher' : 'Шубарин Михаил Александрович',
        'phone' : '+7-938-103-62-19',
    },
    {
        'name' : 'Основы программирования',
        'teacher' : 'Гетман Вероника Андреевна',
        'phone' : '+7-928-103-95-81',
    },
    {
        'name' : 'Иностранный язык',
        'teacher' : 'Гурова Валентина Александровна ',
        'phone' : '+7-919-880-52-63',
    },
    {
        'name' : 'Язык программирования C++',
        'teacher' : 'Гетман Вероника Андреевна',
        'phone' : '+7-928-103-95-81',
    },
    {
        'name' : 'Философия',
        'teacher' : 'Новохатько Александр Григорьевич',
        'phone' : '+79281519572',
    },
    {
        'name' : 'Математическая логика',
        'teacher' : 'Ячменёва Наталья Николаевна',
        'phone' : '',
    },
    {
        'name' : 'Теория Алгоритмов',
        'teacher' : 'Брагилевский Виталий Николаевич',
        'phone' : '',
    },
    {
        'name' : 'Математические основы защиты информации',
        'teacher' : 'Брагилевский Виталий Николаевич',
        'phone' : '',
    },
]


"""
Информация о сессии
"""

session_info = 'Пока нет информации о сессии'



"""
Информация о деканате
"""

dean_info ='Александра деканат - 8(905) 486-86-92'
