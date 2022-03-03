import mysql.connector as mysql


def db_connect():
    return mysql.connect(host="localhost", user="root", password="root", database="mycontactsapp")

def create_schema():
    sql = '''CREATE '''
    sql1 = '''CREATE TABLE IF NOT EXISTS `mycontactsapp`.`user`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(30) NULL,
    `password` TEXT(128) NULL,
    PRIMARY KEY (`id`));'''

    sql2 = '''CREATE TABLE IF NOT EXISTS `mycontactsapp`.`mycontacts`(
    `contact_id` INT NOT NULL AUTO_INCREMENT,
    `id_refer` INT NOT NULL,
    `contact_name` VARCHAR(30) NULL,
    `contact_email` VARCHAR(30) NULL,
    `contact_phone` VARCHAR(40) NULL,
    PRIMARY KEY (`contact_id`),
    FOREIGN KEY (`id_refer`) REFERENCES user (`id`));'''

    connection = db_connect()
    cursor = connection.cursor()

    cursor.execute(sql1)
    cursor.execute(sql2)

    connection.commit()
    connection.close()

def write_to_database(cmd):
    conn =db_connect()
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()
    conn.close()

def read_from_database(cmd):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(cmd)
    val = cur.fetchall()
    conn.close()
    return val

create_schema()


