from bottle import route, run, template, get, post, request, static_file
import sqlite3
# import pandas

def initDatabase():
    print("Initializing database...")
    conn = sqlite3.connect('data/mood.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS mood (
        id INTEGER PRIMARY KEY,
        date_time DATETIME NOT NULL,
        depression INT,
        mania INT,
        irritability INT,
        anxiety INT,
        weight INT,
        drugs BOOLEAN,
        alcohol BOOLEAN,
        psychotic BOOLEAN,
        notes,
        waking_up_time TIME,
        waking_up_p INT,
        first_contact_time TIME,
        first_contact_p INT,
        start_work_time TIME,
        start_work_p INT,
        dinner_time TIME,
        dinner_p INT,
        bedtime_time TIME,
        bedtime_p INT
    )""")
    conn.commit()
    cur.close()

# def checkToday(field): # TODO Fix this, it doesn't work well
#     # Check if an entry has been added today
#     conn = sqlite3.connect('data/mood.db')
#     cur = conn.cursor()
#     result = cur.execute("""SELECT """ + field + """ FROM mood WHERE date_time >= DATETIME(DATE('now')) AND date_time < DATETIME(DATE('now', '+1 day'))""")
#     results = result.fetchall()
#     cur.close()
#     print(results)
#     if not results:
#         return False
#     else:
#         if results[0][0] is '':
#             return False
#         else:
#             return True



# Static Routes
@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/css")

@get("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="static/font")

@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

@get("/static/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/js")

# @route('/<filename:path>')
# def send_static(filename):
#     return static_file(filename, root='static/')

@get('/table') # TODO Make a pretty table template and fill it
def show_table():
    conn = sqlite3.connect('data/mood.db')
    cur = conn.cursor()
    result = cur.execute("""SELECT * FROM mood""")
    results = result.fetchall()

    result_columns = cur.execute("""PRAGMA table_info(mood)""")
    columns = result_columns.fetchall()

    cur.close()

    # Column names
    gen_column_data = ""
    for row in columns:
        gen_column_data += "<th>" + str(row[1]) + "</th>"

    # Table data
    gen_table_data = ""
    for row in results:
        gen_table_data += "<tr>"
        for item in row:
            gen_table_data += "<td>" + str(item) + "</td>"
        gen_table_data += "</tr>"

    return template('view/table.tpl', column_data = gen_column_data, table_data = gen_table_data)

@post('/return')
def form():
    return template('view/form.tpl')

@get('/')
def form():
    return template('view/form.tpl')

@post('/submit')
def send_form():
    # Radio buttons
    depression = request.forms.get('depression')
    mania = request.forms.get('mania')
    irritability = request.forms.get('irritability')
    anxiety = request.forms.get('anxiety')

    # Numbers
    weight = request.forms.get('weight')

    # Checkboxes
    drugs = request.forms.get('drugs')
    alcohol = request.forms.get('alcohol')
    psychotic = request.forms.get('psychotic')

    if drugs is None:
        drugs = False
    else:
        drugs = True

    if alcohol is None:
        alcohol = False
    else:
        alcohol = True

    if psychotic is None:
        psychotic = False
    else:
        psychotic = True

    # Strings
    notes = request.forms.get('notes')

    # Social tracker
    waking_up_time = request.forms.get('waking_up_time')
    waking_up_p = request.forms.get('waking_up_p')

    first_contact_time = request.forms.get('first_contact_time')
    first_contact_p = request.forms.get('first_contact_p')

    start_work_time = request.forms.get('start_work_time')
    start_work_p = request.forms.get('start_work_p')

    dinner_time = request.forms.get('dinner_time')
    dinner_p = request.forms.get('dinner_p')

    bedtime_time = request.forms.get('bedtime_time')
    bedtime_p = request.forms.get('bedtime_p')

    # Open database connection
    print("Connecting to database...")
    conn = sqlite3.connect('data/mood.db')
    cur = conn.cursor()

    # Insert values into database
    print("Inserting values into database...")
    cur.execute("""INSERT INTO mood VALUES (NULL, DATETIME('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    (depression, mania, irritability, anxiety, weight, drugs, alcohol, psychotic, notes, waking_up_time, waking_up_p, first_contact_time, first_contact_p, start_work_time, start_work_p, dinner_time, dinner_p, bedtime_time, bedtime_p))

    # Commit changes and close connection
    conn.commit()
    cur.close()
    print("Done.")

    return template('view/submitted.tpl')

initDatabase()
run(host='0.0.0.0', port=8080, debug=True, reloader=True)
