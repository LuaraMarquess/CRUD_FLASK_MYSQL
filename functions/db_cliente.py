from flask_mysqldb import MySQLdb

def get_all(mysql):
    sql = '''
    SELECT * FROM contacts 
     ORDER BY ID
      LIMIT 20 ;
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    contacts = cur.fetchall()
    cur.close()
    return contacts

def get_contact_by_id(mysql, id): #Funçao para obeter o ID do contato
    sql = "SELECT * FROM contacts WHERE id = %s;"
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (id,))
    contact = cur.fetchone()
    cur.close()
    return contact

def update_contact(mysql, id, nome, tel_residencial, tel_celular, email):
        sql = "UPDATE contacts SET nome = %s, tel_residencial = %s, tel_celular = %s, email = %s WHERE id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(sql, (nome, tel_residencial, tel_celular, email, id))
        mysql.connection.commit()
        cur.close()
        return True  

def insert_contact(mysql, nome, tel_residencial, tel_celular, email):
    sql = '''
    INSERT INTO contacts (nome, tel_residencial, tel_celular, email)
    VALUES (%s, %s, %s, %s)
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (nome, tel_residencial, tel_celular, email))
    mysql.connection.commit()  # Confirma a transação
    cur.close()

    return True
