from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import tempfile
import json
from datetime import datetime
import random
import openpyxl
import string
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Включаем CORS для всех маршрутов

# Функция для генерации случайных имен, фамилий и отчеств
def generate_random_name():
    first_names = [
        'Александр', 'Максим', 'Дмитрий', 'Сергей', 'Алексей', 'Андрей', 'Павел', 'Иван',
        'Николай', 'Владимир', 'Виктор', 'Юрий', 'Константин', 'Олег', 'Роман', 'Антон',
        'Евгений', 'Леонид', 'Георгий', 'Тимофей', 'Кирилл', 'Игорь', 'Станислав', 'Фёдор',
        'Григорий', 'Борис', 'Виталий', 'Артём', 'Артур', 'Арсений', 'Вадим', 'Даниил',
        'Тимур', 'Семён', 'Михаил'
    ]
    last_names = [
        'Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Семенов', 'Соловьев', 'Малышев', 'Николаев',
        'Смирнов', 'Попов', 'Васильев', 'Михайлов', 'Новиков', 'Федоров', 'Морозов', 'Волков',
        'Алексеев', 'Лебедев', 'Егоров', 'Павлов', 'Козлов', 'Степанов', 'Никитин', 'Орлов',
        'Андреев', 'Макаров', 'Никифоров', 'Захаров', 'Зайцев', 'Борисов', 'Яковлев', 'Григорьев',
        'Романов', 'Воробьев', 'Сергеев', 'Фролов', 'Александров', 'Дмитриев', 'Королев', 'Гусев',
        'Киселев', 'Ильин', 'Максимов', 'Поляков', 'Сорокин', 'Виноградов', 'Ковалев', 'Белов',
        'Медведев', 'Антонов', 'Тарасов', 'Жуков', 'Поляков', 'Комаров', 'Сафонов', 'Быков',
        'Сидоренко', 'Титов', 'Федотов', 'Голубев', 'Калинин', 'Карпов', 'Чернов', 'Афанасьев',
        'Максименко', 'Баранов', 'Миронов', 'Фролов', 'Журавлев', 'Селезнев', 'Пономарев', 'Герасимов',
        'Богданов', 'Осипов', 'Кудрявцев', 'Матвеев', 'Савельев', 'Марков', 'Назаров', 'Данилов',
        'Сорокин', 'Белкин', 'Суханов', 'Руднев', 'Яшин', 'Соколов', 'Тихонов', 'Булгаков'
    ]
    patronymics = ['Алексеевич', 'Дмитриевич', 'Сергеевич', 'Александрович', 'Николаевич', 'Владимирович', 'Петрович']

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    patronymic = random.choice(patronymics)

    return first_name, last_name, patronymic

# Функция для генерации случайного телефона
def generate_random_phone():
    # Российский формат: +7 (XXX) XXX-XX-XX
    area_codes = ['495', '812', '343', '383', '473', '351', '381', '401', '472', '485']
    area_code = random.choice(area_codes)
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"+7 ({area_code}) {number[:3]}-{number[3:5]}-{number[5:]}"

# Функция для генерации случайного Telegram username
def generate_random_telegram():
    username_length = random.randint(5, 12)
    username_chars = string.ascii_lowercase + string.digits + '_'
    username = ''.join(random.choice(username_chars) for _ in range(username_length))
    return f"@{username}"

# Функция для генерации случайной IT-компании и должности (Россия)
def generate_random_it_job():
    companies = [
        'Яндекс', 'VK', 'СберТех', 'Тинькофф', 'Лаборатория Касперского', '1С', 'Авито', 'Озон',
        'Рамблер', 'Ростелеком-Солар', 'МТС', 'МегаФон', 'Positive Technologies', 'JetBrains',
        'Альфа-Банк', 'ВТБ', 'Газпром Нефть Цифровые Решения', 'Скайэнг', 'СКБ Контур',
        'Яндекс Практикум', 'HeadHunter', 'Циан', 'Skyeng', 'Skillbox'
    ]
    positions = [
        'Разработчик Python', 'Разработчик Java', 'Frontend-разработчик', 'Backend-разработчик',
        'Fullstack-разработчик', 'DevOps-инженер', 'SRE-инженер', 'QA-инженер', 'Тестировщик',
        'Аналитик данных', 'Data Engineer', 'Data Scientist', 'Системный администратор',
        'Инженер по информационной безопасности', 'Product Manager', 'Project Manager',
        'Бизнес-аналитик', 'Архитектор ПО', 'Mobile-разработчик (iOS)', 'Mobile-разработчик (Android)'
    ]

    company = random.choice(companies)
    position = random.choice(positions)
    return company, position

# Функция для генерации случайных зарплатных ожиданий
def generate_salary_expectations():
    # Зарплаты в тысячах рублей для IT-специалистов в России
    base_salaries = {
        'Разработчик Python': (120, 300),
        'Разработчик Java': (130, 320),
        'Frontend-разработчик': (110, 280),
        'Backend-разработчик': (120, 300),
        'Fullstack-разработчик': (140, 350),
        'DevOps-инженер': (130, 320),
        'SRE-инженер': (140, 350),
        'QA-инженер': (90, 220),
        'Тестировщик': (70, 180),
        'Аналитик данных': (100, 250),
        'Data Engineer': (120, 300),
        'Data Scientist': (130, 320),
        'Системный администратор': (80, 200),
        'Инженер по информационной безопасности': (110, 280),
        'Product Manager': (120, 300),
        'Project Manager': (110, 280),
        'Бизнес-аналитик': (100, 250),
        'Архитектор ПО': (150, 400),
        'Mobile-разработчик (iOS)': (120, 300),
        'Mobile-разработчик (Android)': (110, 280)
    }
    
    position = random.choice(list(base_salaries.keys()))
    min_salary, max_salary = base_salaries[position]
    salary = random.randint(min_salary, max_salary)
    return f"{salary} тыс. руб."

# Функция для генерации случайной даты рождения
def generate_random_birth_date():
    # Генерируем дату рождения для людей 22-55 лет
    start_date = datetime.now() - timedelta(days=55*365)
    end_date = datetime.now() - timedelta(days=22*365)
    
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    
    return random_date.strftime("%d.%m.%Y")

# Функция для генерации случайного e-mail (RU-домены)
def generate_random_email():
    domains = ['yandex.ru', 'mail.ru', 'bk.ru', 'inbox.ru', 'list.ru', 'rambler.ru']
    username_length = random.randint(8, 12)
    username_chars = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(username_chars) for _ in range(username_length))
    domain = random.choice(domains)
    return f"{username}@{domain}"

# Функция для генерации случайного комментария о работнике
def generate_random_comment():
    comments = [
        'Ответственный и пунктуальный специалист',
        'Быстро обучается и инициативен',
        'Отличные коммуникативные навыки',
        'Сильные аналитические способности',
        'Хорошо работает в команде',
        'Внимателен к деталям',
        'Проактивен и ориентирован на результат',
        'Стремится к постоянному развитию',
        'Надежный и исполнительный сотрудник',
        'Успешно внедрял улучшения в проектах',
        'Отличный командный игрок',
        'Высокая работоспособность',
        'Креативный подход к решению задач',
        'Сильные лидерские качества',
        'Отличные навыки презентации'
    ]
    return random.choice(comments)

# Функция для генерации резюме на основе должности и длины
def generate_resume_for_position(position: str, length: str = 'long') -> str:
    # Базовые шаблоны для каждой должности
    base_templates = {
        'Разработчик Python': 'Опыт разработки на Python, Django/FastAPI, SQL, тестирование и CI/CD.',
        'Разработчик Java': 'Коммерческий опыт Java, Spring, микросервисы, Kafka, PostgreSQL.',
        'Frontend-разработчик': 'React/Vue, TypeScript, адаптивная верстка, оптимизация производительности.',
        'Backend-разработчик': 'Проектирование API, микросервисы, базы данных, мониторинг и логирование.',
        'Fullstack-разработчик': 'Опыт фронта и бэка, React, Node.js/Python, DevOps-практики.',
        'DevOps-инженер': 'CI/CD, Docker, Kubernetes, Terraform, мониторинг и безопасность.',
        'SRE-инженер': 'Надежность сервисов, SLO/SLA, алертинг, инфраструктура как код.',
        'QA-инженер': 'Функциональное и автоматизированное тестирование, тест-дизайн, отчётность.',
        'Тестировщик': 'Ручное тестирование, составление чек-листов, баг-трекинг, регресс.',
        'Аналитик данных': 'SQL, Python, визуализация данных, A/B тесты, продуктовая аналитика.',
        'Data Engineer': 'ETL/ELT, Airflow, Spark, хранилища данных, качество данных.',
        'Data Scientist': 'ML-модели, sklearn/pyTorch, фичеинжиниринг, валидация и деплой.',
        'Системный администратор': 'Администрирование Linux/Windows, сети, мониторинг, безопасность.',
        'Инженер по информационной безопасности': 'Threat modeling, SOC, SIEM, pentest, политики ИБ.',
        'Product Manager': 'Дискавери, приоритизация, метрики, гипотезы и гипотез-тестирование.',
        'Project Manager': 'Планирование, риски, коммуникации, отчётность, Agile/Scrum/Kanban.',
        'Бизнес-аналитик': 'Сбор требований, BPMN/UML, постановка задач, acceptance критерии.',
        'Архитектор ПО': 'Архитектура систем, интеграции, NFR, выбор технологий, ревью дизайна.',
        'Mobile-разработчик (iOS)': 'Swift, UIKit/SwiftUI, архитектуры MVVM/VIPER, App Store релизы.',
        'Mobile-разработчик (Android)': 'Kotlin, Jetpack, архитектуры MVVM/MVI, релизы в Google Play.'
    }
    
    base_text = base_templates.get(position, f'Опыт по направлению: {position}. Успешная работа в проектах и командное взаимодействие.')
    
    if length == 'short':
        return base_text
    
    # Дополнительные детали для увеличения размера
    additional_details = [
        "В процессе работы активно использовал современные методологии разработки, включая Agile, Scrum и Kanban. Применял принципы SOLID, DRY и KISS для написания чистого и поддерживаемого кода. Имею опыт работы с системами контроля версий Git, включая создание веток, слияние изменений и разрешение конфликтов. Участвовал в code review процессах, как в роли ревьюера, так и в роли автора кода. Опыт работы с различными системами сборки и развертывания, включая Jenkins, GitLab CI/CD, GitHub Actions и Azure DevOps.",
        
        "Принимал участие в планировании спринтов, оценке задач и составлении технических заданий. Работал с системами управления проектами Jira, Confluence, Trello и Asana. Имею опыт интеграции различных API и сервисов, включая REST, GraphQL, gRPC и WebSocket. Работал с базами данных SQL (PostgreSQL, MySQL, SQL Server) и NoSQL (MongoDB, Redis, Cassandra). Применял принципы микросервисной архитектуры и работал с контейнеризацией Docker и оркестрацией Kubernetes.",
        
        "Опыт работы с облачными платформами AWS, Google Cloud Platform и Microsoft Azure. Знание принципов безопасности при разработке, включая OWASP Top 10, аутентификацию и авторизацию, шифрование данных и защиту от SQL-инъекций. Опыт работы с системами мониторинга и логирования: Prometheus, Grafana, ELK Stack, Splunk. Применял принципы автоматизированного тестирования, включая unit-тесты, интеграционные тесты и end-to-end тесты. Работал с фреймворками тестирования JUnit, TestNG, PyTest, Jest и Cypress."
    ]
    
    # Создаем длинный текст резюме
    long_resume = base_text + "\n\n" + "\n\n".join(additional_details)
    
    if length == 'medium':
        return long_resume
    
    # Для длинного резюме добавляем еще больше контента
    extra_content = [
        "В рамках профессионального развития постоянно изучаю новые технологии и подходы к разработке. Посещаю конференции, вебинары и технические митапы для расширения кругозора и обмена опытом с коллегами. Участвую в open-source проектах и вношу свой вклад в развитие технологического сообщества. Веду технический блог и делюсь знаниями через статьи и презентации.",
        
        "Имею сертификации по различным технологиям и платформам, что подтверждает высокий уровень компетенций. Регулярно прохожу обучение и повышаю квалификацию в соответствии с современными требованиями рынка. Участвую в программах менторства и помогаю коллегам в развитии их навыков. Активно участвую в технических дискуссиях и помогаю принимать обоснованные решения по выбору технологий."
    ]
    
    long_resume += "\n\n" + "\n\n".join(extra_content)
    
    # Добавляем повторяющиеся блоки для максимального увеличения размера
    repeat_blocks = [
        "Технические навыки включают глубокое знание языков программирования, фреймворков и библиотек. Опыт работы с различными архитектурными паттернами и принципами проектирования. Знание принципов работы с базами данных, включая проектирование схем, оптимизацию запросов и управление транзакциями. Опыт работы с системами контроля версий и управления исходным кодом.",
        
        "Проектный опыт включает участие в разработке крупных корпоративных систем и высоконагруженных приложений. Работа с международными командами и проектами в различных часовых поясах. Опыт управления техническими командами и координации работы разработчиков. Применение принципов agile и lean в управлении проектами и продуктами.",
        
        "Коммуникативные навыки позволяют эффективно взаимодействовать с заказчиками, менеджерами проектов и техническими специалистами. Опыт проведения технических презентаций и демонстраций для различных аудиторий. Умение объяснять сложные технические концепции простым языком. Опыт работы с документацией и техническими спецификациями."
    ]
    
    # Добавляем повторяющиеся блоки несколько раз для максимального увеличения размера
    for _ in range(10):
        long_resume += "\n\n" + "\n\n".join(repeat_blocks)
    
    # Добавляем еще больше технических деталей
    technical_details = [
        "В области разработки веб-приложений имею глубокие знания HTML5, CSS3, JavaScript ES6+, TypeScript, React, Vue.js, Angular, Node.js, Express.js, Next.js, Nuxt.js. Опыт работы с современными инструментами сборки: Webpack, Vite, Rollup, Parcel. Знание принципов Progressive Web Apps (PWA), Service Workers, Web Components. Опыт работы с CSS-препроцессорами: Sass, Less, Stylus. Применение CSS-in-JS решений: styled-components, emotion, CSS Modules.",
        
        "В области backend разработки опыт работы с Python (Django, Flask, FastAPI, Pyramid), Java (Spring Boot, Spring Framework, Hibernate, Maven, Gradle), C# (.NET Core, ASP.NET, Entity Framework), Go (Gin, Echo, Gorilla Mux), Node.js (Express, Koa, Hapi). Знание принципов REST API, GraphQL, gRPC, WebSocket. Опыт работы с ORM: SQLAlchemy, Hibernate, Entity Framework, GORM. Применение принципов Domain-Driven Design (DDD), Event Sourcing, CQRS.",
        
        "В области баз данных опыт работы с реляционными СУБД: PostgreSQL, MySQL, SQL Server, Oracle, SQLite. NoSQL базы данных: MongoDB, Redis, Cassandra, CouchDB, Neo4j. Опыт работы с системами управления миграциями: Alembic, Flyway, Liquibase, Entity Framework Migrations. Знание принципов проектирования схем баз данных, нормализации, денормализации, индексирования. Опыт работы с репликацией, шардингом, партиционированием."
    ]
    
    # Добавляем технические детали
    for _ in range(5):
        long_resume += "\n\n" + "\n\n".join(technical_details)
    
    return long_resume

# Функция для создания Excel файла
def create_excel_file(row_count, file_name, resume_length):
    # Создание новой рабочей книги и активного листа
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Контакты"

    # Заголовки столбцов согласно требованиям
    headers = [
        "Фамилия", "Имя", "Отчество", "Телефон", "Электронная почта", 
        "Telegram", "Должность", "Компания", "Зарплатные ожидания", 
        "Дата рождения (ДД.ММ.ГГГГ)", "Комментарий (личные заметки)", "Текст резюме"
    ]
    ws.append(headers)

    # Генерация данных
    for _ in range(row_count):
        first_name, last_name, patronymic = generate_random_name()
        phone = generate_random_phone()
        email = generate_random_email()
        telegram = generate_random_telegram()
        company, position = generate_random_it_job()
        salary = generate_salary_expectations()
        birth_date = generate_random_birth_date()
        comment = generate_random_comment()
        resume = generate_resume_for_position(position, resume_length)
        
        # Добавляем строку с данными в правильном порядке
        ws.append([
            last_name, first_name, patronymic, phone, email, telegram,
            position, company, salary, birth_date, comment, resume
        ])

    # Сохранение файла во временную директорию
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"{file_name}.xlsx")
    wb.save(file_path)
    
    return file_path

# Маршруты Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_file():
    try:
        data = request.get_json()
        
        # Валидация данных
        row_count = data.get('rowCount', 10000)
        file_name = data.get('fileName', 'contacts')
        resume_length = data.get('resumeLength', 'long')
        
        if not isinstance(row_count, int) or row_count < 100 or row_count > 50000:
            return jsonify({'error': 'Количество записей должно быть от 100 до 50,000'}), 400
        
        if not file_name or not file_name.strip():
            return jsonify({'error': 'Имя файла не может быть пустым'}), 400
        
        if resume_length not in ['short', 'medium', 'long']:
            return jsonify({'error': 'Неверная длина резюме'}), 400
        
        # Создание файла
        file_path = create_excel_file(row_count, file_name, resume_length)
        
        # Отправка файла
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"{file_name}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
