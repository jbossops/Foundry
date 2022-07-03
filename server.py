from unittest import result

from numpy import product
from user import User
from flask import Flask, redirect, url_for, render_template, jsonify, request, g, session, flash
from flask_mysql_connector import MySQL

def main():
    #App config
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = '192.168.1.47'
    app.config['MYSQL_PORT'] = '3307'
    app.config['MYSQL_USER'] = 'ProductionOrders'
    app.config['MYSQL_PASSWORD'] = '123$RFVcxzSE$'
    app.config['MYSQL_DATABASE'] = 'Foundry'
    app.secret_key = 'password74320'
    mysql = MySQL(app)

    #Users managment
    users = []
    users.append(User(id=1, username='admin', password='password'))  
    users.append(User(id=2, username='office', password='office')) 
    users.append(User(id=3, username='forming', password='forming')) 

    def query_db(query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result

    def query_db_first(query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
        return result

    def query_update(query):
        cur = mysql.new_cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True

    @app.before_request
    def before_request():
        g.user = None
        if 'user_id' in session:
            user = [x for x in users if x.id == session['user_id']][0]
            g.user = user   
   
    @app.route("/", methods=['POST', 'GET'])
    def login():
        try:
            if request.method == 'POST':
                session.pop('user_id', None)
                username = request.form['username']
                password = request.form['password']
                user = [x for x in users if x.username == username][0]
                if user and user.password == password:
                    session['user_id'] = user.id
                    session['user'] = user.username
                    if user.username == 'forming':
                        return redirect(url_for('forming'))
                    else:
                        return redirect(url_for('forming'))
                else:
                    flash(f'Wrong password or username.')
                    return redirect(url_for('login'))
            return render_template('login.html')
        except IndexError: 
            flash(f'Wrong password or username.')
            return redirect(url_for('login'))

    @app.route('/logout') 
    def logout(): 
        session.pop('user_id', None)
        return redirect(url_for('login'))

    @app.route("/forming", methods=['POST', 'GET'])
    def forming():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            query = query_db('SELECT Forming.id as id, Forming.status as status, Forming.added_by as added_by, Forming.added as added, Forming.changed as changed, Forming.changed_by as changed_by, Forming.comment as comment, Products.product_name as product_name, Products.cooling_time as cooling_time, Products.frames_quantity as frames_quantity FROM Forming LEFT JOIN Products ON Forming.product_id = Products.id')
            products = query_db('SELECT * FROM Products ORDER BY product_name DESC')
            return render_template("forming.html", items=query, products=products) 

    @app.route("/foundry", methods=['POST', 'GET'])
    def foundry():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            query = query_db('SELECT Foundry.id as id, Foundry.status_foundry as status_foundry, Foundry.added_by as added_by, Foundry.added as added, Foundry.changed as changed, Foundry.changed_by as changed_by, Foundry.comment as comment, Products.product_name as product_name, Products.cooling_time as cooling_time, Products.frames_quantity as frames_quantity FROM Foundry LEFT JOIN Products ON Foundry.product_id = Products.id')
            products = query_db('SELECT * FROM Products ORDER BY product_name DESC')
            return render_template("foundry.html", items=query, products=products) 

    @app.route("/items_completed_foundry", methods=['POST', 'GET'])
    def items_completed_foundry():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            query = query_db('SELECT Foundry.id as id, Foundry.status_foundry as status_foundry, Foundry.added_by as added_by, Foundry.added as added, Foundry.changed as changed, Foundry.changed_by as changed_by, Foundry.comment as comment, Products.product_name as product_name, Products.cooling_time as cooling_time, Products.frames_quantity as frames_quantity FROM Foundry LEFT JOIN Products ON Foundry.product_id = Products.id')
            return render_template("items_completed_foundry.html", items=query) 

    @app.route("/items_canceled_foundry", methods=['POST', 'GET'])
    def items_canceled_foundry():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            query = query_db('SELECT Foundry.id as id, Foundry.status_foundry as status_foundry, Foundry.added_by as added_by, Foundry.added as added, Foundry.changed as changed, Foundry.changed_by as changed_by, Foundry.comment as comment, Products.product_name as product_name, Products.cooling_time as cooling_time, Products.frames_quantity as frames_quantity FROM Foundry LEFT JOIN Products ON Foundry.product_id = Products.id')
            return render_template("items_canceled_foundry.html", items=query) 

    @app.route("/items_completed_forming", methods=['POST', 'GET'])
    def items_formed():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            query = query_db('SELECT Forming.id as id, Forming.status as status, Forming.added_by as added_by, Forming.added as added, Forming.changed as changed, Forming.changed_by as changed_by, Forming.comment, Products.product_name as product_name, Products.cooling_time as cooling_time, Products.frames_quantity as frames_quantity FROM Forming LEFT JOIN Products ON Forming.product_id = Products.id')
            return render_template("items_completed_forming.html", items=query) 

    @app.route("/items_canceled_forming", methods=['POST', 'GET'])
    def items_canceled():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            query = query_db('SELECT Forming.id as id, Forming.status as status, Forming.added_by as added_by, Forming.added as added, Forming.changed as changed, Forming.changed_by as changed_by, Forming.comment, Products.product_name as product_name, Products.cooling_time as cooling_time, Products.frames_quantity as frames_quantity FROM Forming LEFT JOIN Products ON Forming.product_id = Products.id')
            return render_template("items_canceled_forming.html", items=query) 

    @app.route("/products", methods=['POST', 'GET'])
    def products():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            query = query_db('SELECT * FROM Products ORDER BY product_name DESC')
            return render_template("products.html", items=query) 
    
    @app.route("/edit_item_forming/<id>", methods=['POST', 'GET'])
    def edit_item_forming(id):
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            status = str(request.form['a1'])
            comment = str(request.form['a3'])
            comment = comment.replace("'", "")
            query = "UPDATE Forming SET comment='" + comment + "', status='" + status + "', changed_by='" + str(session["user"]) + "', changed=current_timestamp() WHERE id=" + id
            print(query)
            query_update(query)
            return redirect(url_for('forming'))


    @app.route("/edit_item_foundry/<id>", methods=['POST', 'GET'])
    def edit_item(id):
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            status_foundry = str(request.form['a1'])
            comment = str(request.form['a3'])
            comment = comment.replace("'", "")
            query = "UPDATE Foundry SET comment='" + comment + "', status_foundry='" + status_foundry + "', changed_by='" + str(session["user"]) + "', changed=current_timestamp() WHERE id=" + id
            query_update(query)
            return redirect(url_for('foundry'))

    @app.route("/add_product", methods=['POST'])
    def add_product():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            product_name =  str(request.form['a1'])
            frames_quantity = str(request.form['a2'])
            if frames_quantity == '':
                frames_quantity = '2'
            cooling_time = str(request.form['a3'])
            if cooling_time == '':
                cooling_time = '0'
            comment_product = str(request.form['a4'])
            comment_product = comment_product.replace("'", "")
            query = "INSERT INTO Products(product_name, frames_quantity, cooling_time, modified_by, modified, comment_product) VALUES('" + product_name + "','" + frames_quantity + "','" + cooling_time + "','" + str(session["user"]) + "',current_timestamp(),'" + comment_product + "')"
            query_update(query)
            return redirect(url_for('products'))  

    @app.route("/edit_product/<id>", methods=['POST'])
    def edit_product(id):
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            product_name =  str(request.form['a1'])
            item_status = str(request.form['a2'])
            frames_quantity = str(request.form['a3'])
            cooling_time = str(request.form['a4'])
            comment_product = str(request.form['a5'])
            comment_product = comment_product.replace("'", "")
            query = "UPDATE Products SET product_name='" + product_name +  "', item_status='" + item_status + "', frames_quantity='" + frames_quantity + "', cooling_time='" + cooling_time + "', comment_product='" + comment_product + "', modified_by='" + str(session["user"]) + "', modified=current_timestamp() WHERE id=" + id
            query_update(query)
            return redirect(url_for('products'))

    @app.route("/add_item_forming", methods=['POST'])
    def add_item_forming():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            product_name =  str(request.form['a1'])
            query_frames_quantity = "SELECT frames_quantity FROM Products WHERE product_name LIKE '" + product_name +"'"
            frames_quantity = query_db(query_frames_quantity)
            n = int(frames_quantity[0]['frames_quantity'])
            items_quantity = int(request.form['a2'])
            comment = str(request.form['a3'])
            comment = comment.replace("'", "")
            product_id_query = "SELECT id FROM Products WHERE product_name LIKE '" + product_name + "'"
            product_id_dict = query_db(product_id_query)
            product_id = str(product_id_dict[0]['id'])
            k = n * items_quantity
            query = "INSERT INTO Forming(product_id, added_by, changed_by, comment) VALUES (" + product_id + ",'" + str(session["user"]) + "'," + "'" + str(session["user"]) + "'" + ",'" + comment + "'" + ")"
            for k in range (k):
                query_update(query)
            return redirect(url_for('forming'))  

    @app.route("/add_item_forming_cascade", methods=['POST'])
    def add_item_forming_cascade():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            product_name =  str(request.form['a1'])
            query_frames_quantity = "SELECT frames_quantity FROM Products WHERE product_name LIKE '" + product_name +"'"
            frames_quantity = query_db(query_frames_quantity)
            n = int(frames_quantity[0]['frames_quantity'])
            items_quantity = int(request.form['a2'])
            comment = str(request.form['a3'])
            comment = comment.replace("'", "")
            product_id_query = "SELECT id FROM Products WHERE product_name LIKE '" + product_name + "'"
            product_id_dict = query_db(product_id_query)
            product_id = str(product_id_dict[0]['id'])
            k = n * items_quantity
            query_forming = "INSERT INTO Forming(product_id, added_by, changed_by, comment) VALUES (" + product_id + ",'" + str(session["user"]) + "'," + "'" + str(session["user"]) + "'" + ",'" + comment + "'" + ")"
            for k in range (k):
                query_update(query_forming)
            query_foundry = "INSERT INTO Foundry(product_id, added_by, changed_by) VALUES (" + product_id + ",'" + str(session["user"]) + "'," + "'" + str(session["user"]) + "'" + ")"
            for items_quantity in range (items_quantity):
                query_update(query_foundry)
            return redirect(url_for('forming'))   

    @app.route("/add_item_foundry", methods=['POST'])
    def add_item_foundry():
        if not g.user:
            flash(f'Login required.')
            return redirect(url_for('login'))
        else:
            product_name =  str(request.form['a1'])
            items_quantity = int(request.form['a2'])
            comment = str(request.form['a3'])
            comment = comment.replace("'", "")
            product_id_query = "SELECT id FROM Products WHERE product_name LIKE '" + product_name + "'"
            product_id_dict = query_db(product_id_query)
            product_id = str(product_id_dict[0]['id'])
            query = "INSERT INTO Foundry(product_id, added_by, changed_by, comment) VALUES (" + product_id + ",'" + str(session["user"]) + "'," + "'" + str(session["user"]) + "'" + ",'" + comment + "')"
            for items_quantity in range (items_quantity):
                query_update(query)
            return redirect(url_for('foundry'))  

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5555, debug=True)


        
####################################################################
####################################################################
####################################################################

main()


