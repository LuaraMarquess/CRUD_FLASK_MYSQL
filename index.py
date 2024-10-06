from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from functions.db_cliente import *

app = Flask(__name__)

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'registercontactsdb'

mysql = MySQL(app)

@app.route("/")
def home():
    contacts = get_all(mysql)

    page = {
        'title': 'Agenda de contatos',
        'contacts': contacts    
    }
    
    return render_template('home.html', page=page)

@app.route("/insertUser", methods=["GET", "POST"])
def add_contacts():
    contacts = get_all(mysql)  
    
    page = {
        'title': 'Inserir Usuário',
        'contacts': contacts,
        'success_message': None  
    }
    
    if request.method == "POST":
        nome = request.form["nome"]
        tel_residencial = request.form["telefone_residencial"]
        tel_celular = request.form["telefone_celular"]
        email = request.form["email"]

        if not all([nome, tel_residencial, tel_celular, email]):
            return render_template("insertUser.html", page=page, success=False, error="Preencha todos os campos.")

        
        insert_contact(mysql, nome, tel_residencial, tel_celular, email)

        
        page['success_message'] = "Usuário inserido com sucesso!"
        
  
        return render_template("insertUser.html", page=page)

   
    return render_template("insertUser.html", page=page)




@app.route("/update_contact/<int:id>", methods=["POST"])
def update_contact_route(id):
    nome = request.form["nome"]
    tel_residencial = request.form["tel_residencial"]
    tel_celular = request.form["tel_celular"]
    email = request.form["email"]

   
    if update_contact(mysql, id, nome, tel_residencial, tel_celular, email):
        return redirect("/")  
    else:
        return "Erro ao atualizar contato.", 500  

@app.route("/edit/<int:id>")
def edit(id):
    
     page = {
        'title': 'Inserir contatos',
        'contacts': get_all(mysql)  
    }
    
     contact = get_contact_by_id(mysql, id)  
     if contact: 
        return render_template('edit_contacts.html', contact=contact)
     else:
        return "Contato não encontrado.", 404  
    
# Função para buscar contatos por nome
def search_contacts_by_name(mysql, name):
    sql = "SELECT * FROM contacts WHERE nome LIKE %s;"
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (f"%{name}%",))  
    contacts = cur.fetchall()
    cur.close()
    return contacts

@app.route("/search", methods=["GET", "POST"])
def search():
    contacts = []  

    if request.method == "POST":
        nome = request.form.get("name")  
        
    
        print(f"Nome recebido no formulário: {nome}")
        
        if nome:
            contacts = search_contacts_by_name(mysql, nome)
            print(f"Contatos encontrados na busca: {contacts}")
        else:
            contacts = get_all(mysql)

    page = {
        'title': 'Agenda de Contatos',
        'contacts': contacts
    }

    return render_template("home.html", page=page)

if __name__ == '__main__':
    app.run(debug=True)
