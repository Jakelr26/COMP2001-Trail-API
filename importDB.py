import pyodbc

'''
Making the table/ dbo
''
#pre databse issues login
server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_JLear'
username = 'JLear'
password = 'SkcY333+'
driver = '{ODBC Driver 17 for SQL Server}'

server = 'localhost'
database = 'COMP2001_test'
'''
#my server details
#should be a single use file - I use to copy and paste different parts into the python comand line
server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_JLear'
username = 'JLear'
password = 'LekP847*'
driver = '{ODBC Driver 17 for SQL Server}'
conn_str = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=Yes;'
    'TrustServerCertificate=Yes;'
    'Connection Timeout=30;'
    'Trusted_Connection=No'
 )
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

columns = [
    'id INT IDENTITY(1,1) PRIMARY KEY',
    'fname VARCHAR(25)',
    'lname VARCHAR(25) UNIQUE',
    'timestamp DATETIME',
]

create_table_cmd = f"CREATE TABLE person ({','.join(columns)})"
cursor.execute(create_table_cmd)
cursor.commit()

'''___________________________Adding data_____________________________________________'''

people = [
    "'Grace', 'Hopper', '2024-11-19 16:15:10'",
    "'Tim', 'Berners-Lee', '2024-11-19 16:15:13'",
    "'Ada', 'Lovelace', '2024-11-19 16:15:27'",
]

for person_data in people:
    insert_cmd = f"INSERT INTO person VALUES ({person_data})"
    cursor.execute(insert_cmd)

cursor.commit()

'''___________________________ Viewing data_____________________________________________'''

cursor.execute("SELECT * FROM person")

people = cursor.fetchall()
for person in people:
    print(person)
