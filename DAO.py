import sqlite3


def generate_db():
    conn = sqlite3.connect('brightkite.db')
    print ("Opened database successfully")
    c = conn.cursor()
    # create table if it is not exist
    try:
        c.execute('''CREATE TABLE CHECKIN
            (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
            user        INT NOT NULL,
            location_id        INT NOT NULL,
            checkin_time    TEXT    NOT NULL,
            longitude        REAL NOT NULL,
            latitude        REAL NOT NULL);''')
        print ("Brightkite table created successfully")
    except:
        print("Brightkite table already exist")
    conn.commit()



def insert_checkin(record):
    conn = sqlite3.connect('brightkite.db')
    c = conn.cursor()
    statement = "INSERT INTO CHECKIN (user,location_id,checkin_time) values ('{}','{}','{}');".format(record.user,record.location_id,record.checkin_time)
    c.execute(statement)
    conn.commit()
def execute_checkin(cursor,record):
    statement = "INSERT INTO CHECKIN (user,location_id,checkin_time,longitude,latitude) values ('{}','{}','{}','{}','{}');".format(record.user,record.location_id,record.checkin_time,record.longitude,record.latitude)
    cursor.execute(statement)


def build_sql(id,interval):
    statement = "select b.user, count(*) from checkin as a, checkin as b where datetime(a.checkin_time)<datetime(b.checkin_time,'+{} minutes') and datetime(a.checkin_time)>datetime(b.checkin_time,'-{} minutes') and a.location_id==b.location_id and a.user=={} and a.user!=b.user and a.location_id!='0' group by b.user;".format(interval,interval,id)
    return statement


def query_database(sql):
    conn = sqlite3.connect('brightkite.db')
    c = conn.cursor()
    statement = sql
    result = c.execute(statement)
    return result


def add_index():
    query_database("CREATE INDEX location_id_index ON CHECKIN (location_id);")
    query_database("CREATE INDEX user_id ON CHECKIN (user);")
    return


if __name__ == '__main__':
    result = query_database(build_sql(217,5))
    for i in result:
        print(i)


# query_result = query_database("select * from food")
# for i in query_result:
#     print(i)
