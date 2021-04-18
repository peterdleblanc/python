__author__ = 'Peter LeBlanc'


import psycopg2

try:
    connect_str = "dbname='medtracker' user='peter' host='localhost' " + \
                  "password='peter'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    # Execute a command: this creates a new table
    cursor.execute("CREATE TABLE patients (record_id serial PRIMARY KEY, patient_id integer, patient_name varchar, doctors_id integer, date date,);")

    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    #cursor.execute("INSERT INTO patients (patient_id, patient_name) VALUES (%s, %s)",(987654, "Debbie Sabiean"))

    # Query the database and obtain data as Python objects
    cursor.execute("SELECT * FROM patients;")
    #cursor.execute("SELECT patient_id=123456 FROM patients;")
    #results = cursor.fetchone()
    results = cursor.fetchall()

    for i in results:
        print(i)
    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cursor.close()
    conn.close()


except Exception as e:
    print("Failed to connect to database. Invalid dbname, user or password?")
    print(e)