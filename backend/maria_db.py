import pymysql
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import bus_line_data as bus_line

def dbconnect():
    conn = pymysql.connect (host='bus-gps-system.ctawiea6yhnu.ap-northeast-2.rds.amazonaws.com', user='root', password='!es9830297', db='Bus_GPS_system', charset='utf8')
    return conn

def save_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    with open("encryption_key.key", "rb") as key_file:
        key = key_file.read()
    return key

def insert_coordinate(conn, gps_id, x, y, gps_time):
    sql = "INSERT INTO Coordinate(gps_id, x, y, time) VALUES (%s, %s, %s, %s)"
    cur = conn.cursor()
    key = b'TKphz5uD2HERhXEY8wRRDg_Eye9TRvfgnAX6z1ja2TA='
    suite = Fernet(key)
    datas = (suite.encrypt(gps_id.encode()), suite.encrypt(x.encode()), suite.encrypt(y.encode()), gps_time)
    cur.execute(sql, datas)
    conn.commit()
    sql = "SELECT coordinate_id FROM Coordinate ORDER BY coordinate_id DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchall()[0][0]
    insert_collect_history(conn, result, 'GPS', 'EunsungTrasys', gps_time)
    insert_usage_history(conn, result, 'GPS', 'APP', gps_time)

def insert_access_history(conn, user_id, ip, access_time, name):
    sql = "INSERT INTO AccessHistory(user_id, ip, access_time, name) VALUES (%s, %s, %s, %s)"
    cur = conn.cursor()
    datas = (user_id, ip, access_time, name)
    cur.execute(sql, datas)
    conn.commit()
    
def insert_collect_history(conn, coordinate_id, collect_method, collect_requester, collect_time):
    sql = "INSERT INTO CollectHistory(coordinate_id, collect_method, collect_requester, collect_time) VALUES (%s, %s, %s, %s)"
    cur = conn.cursor()
    datas = (coordinate_id, collect_method, collect_requester, collect_time)
    cur.execute(sql, datas)
    conn.commit()
    
def insert_usage_history(conn, coodinate_id, collect_method, recipient, usage_time):
    sql = "INSERT INTO UsageHistory(coordinate_id, collect_method, recipient, usage_time) VALUES (%s, %s, %s, %s)"
    cur = conn.cursor()
    datas = (coodinate_id, collect_method, recipient, usage_time)
    cur.execute(sql, datas)
    conn.commit()
    
def delete_old_data(conn):
    cur = conn.cursor()
    delete_date = datetime.today() - timedelta(days = 30*6)
    delete_access_date = datetime.today() - timedelta(days = 30*12)
    sql = "DELETE FROM UsageHistory WHERE usage_time < %s"
    cur.execute(sql, delete_date)
    sql = "DELETE FROM CollectHistory WHERE collect_time < %s"
    cur.execute(sql, delete_date)
    sql = "DELETE FROM Coordinate WHERE time < %s"
    cur.execute(sql, delete_date)
    sql = "DELETE FROM AccessHistory WHERE access_time < %s"
    cur.execute(sql, delete_access_date)
    conn.commit()
    
def search_access_history(conn):
    sql = "SELECT * FROM AccessHistory ORDER BY access_time DESC"
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    column_name = ("access_history_id", "user_id", "ip", "access_time", "name")
    column_names_list = []
    for i in datas:
        column_names_list.append(column_name)
    results = []
    for i,j in zip(tuple(column_names_list), datas):
        results.append(dict(zip(i, j)))
    for i in results:
        i['access_time'] = i['access_time'].strftime("%Y-%m-%d %H:%M:%S")
    print(results)
    return results

def search_access_history_date(conn, first_date:datetime, last_date:datetime):
    sql = "SELECT ah.access_history_id, u.id AS user_id_in_user_table, ah.ip, ah.access_time, ah.name AS access_name FROM AccessHistory ah JOIN User u ON ah.user_id = u.user_id ORDER BY access_time DESC"
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    column_name = ("access_history_id", "user_id", "ip", "access_time", "name")
    column_names_list = []
    for i in datas:
        column_names_list.append(column_name)
    results = []
    for i,j in zip(tuple(column_names_list), datas):
        results.append(dict(zip(i, j)))
    def check(data):
        return (data["access_time"] >= first_date and data["access_time"] <= last_date + timedelta(days=1))
    results = list(filter(check, results))
    for i in results:
        i['access_time'] = i['access_time'].strftime("%Y-%m-%d %H:%M:%S")
    return results

def search_coordinate(conn):
    sql = "SELECT * FROM Coordinate ORDER BY time DESC"
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    column_name = ("coordinate_id", "gps_id", "x", "y", "time")
    column_names_list = []
    for i in datas:
        column_names_list.append(column_name)
    results = []
    for i,j in zip(tuple(column_names_list), datas):
        results.append(dict(zip(i, j)))
    key = b'TKphz5uD2HERhXEY8wRRDg_Eye9TRvfgnAX6z1ja2TA='
    suite = Fernet(key)
    for i in results:
        i['gps_id'] = suite.decrypt(i['gps_id']).decode()
        i['x'] = suite.decrypt(i['x']).decode()
        i['y'] = suite.decrypt(i['y']).decode()
        i['time'] = i['time'].strftime("%Y-%m-%d %H:%M:%S")
    return results

def search_coordinate_date(conn, first_date:datetime, last_date:datetime):
    sql = "SELECT * FROM Coordinate ORDER BY time DESC"
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    column_name = ("coordinate_id", "gps_id", "x", "y", "time")
    column_names_list = []
    for i in datas:
        column_names_list.append(column_name)
    results = []
    for i,j in zip(tuple(column_names_list), datas):
        results.append(dict(zip(i, j)))
    key = b'TKphz5uD2HERhXEY8wRRDg_Eye9TRvfgnAX6z1ja2TA='
    suite = Fernet(key)
    for i in results:
        i['gps_id'] = suite.decrypt(i['gps_id']).decode()
        i['x'] = suite.decrypt(i['x']).decode()
        i['y'] = suite.decrypt(i['y']).decode()
    def check(data):
        return (data["time"] >= first_date & data["time"] <= last_date + timedelta(days=1))
    results = list(filter(check, results))
    for i in results:
        i['time'] = i['time'].strftime("%Y-%m-%d %H:%M:%S")
    return results

def search_collect_history(conn):
    sql = "SELECT * FROM CollectHistory"
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    column_name = ("collect_history_id", "coordinate_id", "collect_method", "collect_requester", "collect_time")
    column_names_list = []
    for i in datas:
        column_names_list.append(column_name)
    results = []
    for i,j in zip(tuple(column_names_list), datas):
        results.append(dict(zip(i, j)))
    for i in results:
        i['collect_time'] = i['collect_time'].strftime("%Y-%m-%d %H:%M:%S")
    print(results)
    return results

def search_collect_history_date(conn, first_date:datetime, last_date:datetime):
    sql = "SELECT * FROM CollectHistory"
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    column_name = ("collect_history_id", "coordinate_id", "collect_method", "collect_requester", "collect_time")
    column_names_list = []
    for i in datas:
        column_names_list.append(column_name)
    results = []
    for i,j in zip(tuple(column_names_list), datas):
        results.append(dict(zip(i, j)))
    def check(data):
        return (data["collect_time"] >= first_date and data["collect_time"] <= last_date + timedelta(days=1))
    results = list(filter(check, results))
    for i in results:
        i['collect_time'] = i['collect_time'].strftime("%Y-%m-%d %H:%M:%S")
    return results

def search_usage_history(conn):
    sql = "SELECT * FROM UsageHistory"
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    column_name = ("usage_history_id", "coordinate_id", "collect_method", "recipient", "usage_time")
    column_names_list = []
    for i in datas:
        column_names_list.append(column_name)
    results = []
    for i,j in zip(tuple(column_names_list), datas):
        results.append(dict(zip(i, j)))
    for i in results:
        i['usage_time'] = i['usage_time'].strftime("%Y-%m-%d %H:%M:%S")
    print(results)
    return results

def search_usage_history_date(conn, first_date:datetime, last_date:datetime):
    sql = "SELECT * FROM UsageHistory"
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    column_name = ("usage_history_id", "coordinate_id", "collect_method", "recipient", "usage_time")
    column_names_list = []
    for i in datas:
        column_names_list.append(column_name)
    results = []
    for i,j in zip(tuple(column_names_list), datas):
        results.append(dict(zip(i, j)))
    def check(data):
        return (data["usage_time"] >= first_date and data["usage_time"] <= last_date + timedelta(days=1))
    results = list(filter(check, results))
    for i in results:
        i['usage_time'] = i['usage_time'].strftime("%Y-%m-%d %H:%M:%S")
    return results

def login_check(conn, id, pw):
    cur = conn.cursor()
    sql = "SELECT * FROM User WHERE id=%s AND password=%s"
    cur.execute(sql, (id, pw))
    data = cur.fetchall()
    if len(data) != 0:
        result = True
    else:
        result = False
    return result
    
def search_user(conn, id):
    cur = conn.cursor()
    sql = "SELECT * FROM User WHERE id=%s"
    cur.execute(sql, (id))
    data = cur.fetchall()
    return data
    

if __name__=="__main__" :
    
    conn = dbconnect()
    
    while(True):
        word = input()
        match word:
            case "input coordinate now":
                line = bus_line.line_23
                time = datetime.now()
                for i in line:
                    time += timedelta(seconds=20)
                    insert_coordinate(conn, "135648", i[0], i[1], time)
                print("input complete")
            case "search access":
                search_access_history(conn)
            case "search collect":
                search_collect_history(conn)
            case "search usage":
                search_usage_history(conn)
            case "end":
                break
    
    # login_check(conn, "admin", "!es9830297")
        
    # insert_coordinate(conn, "testgps", "35.184685", "126.870906", datetime(2024,1,23,11,11,11))

    # search_collect_history_date(conn, datetime(2024,11,20,11,11,11), datetime(2024,12,31,11,11,11))

    # search_user_name(conn, "admin")
    
    # insert_access_history(conn, 1, "1234", datetime(2025,1,2,11,11,11), "cjs")

    # delete_old_data(conn)
