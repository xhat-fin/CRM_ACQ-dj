import jwt
from flask import Flask, jsonify, render_template, request, session, url_for, redirect
import requests as req
from datetime import datetime

app = Flask(__name__)
app.secret_key = '123'



def check_token(access, refresh):
    try:
        data_ac_token = jwt.decode(access, options={"verify_signature": False})
        data_re_token = jwt.decode(refresh, options={"verify_signature": False})
    except:
        return False
    date_now = datetime.now()
    if date_now < datetime.fromtimestamp(data_ac_token.get('exp')):
        print('ACCESS токен валидный')
        return True
    elif date_now < datetime.fromtimestamp(data_re_token.get('exp')):
        new_ac_token = req.post('http://127.0.0.1:8000/auth/api/token/refresh/', json={"refresh": refresh})
        new_ac_token = new_ac_token.json()
        session['access'] = new_ac_token.get('access')
        session['refresh'] = new_ac_token.get('refresh')
        print('заменили с помощью refresh access')
        return True
    else:
        print('Все просрочено')
        return False



                                                #############################
                                                # РЕГИСТРАЦИЯ И АВТОРИЗАЦИЯ #
                                                #############################



# РЕГИСТРАЦИЯ
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('auth/register.html', data={})
    if request.method == "POST":
        reg_data = {
            'username': request.form['username'],
            'password': request.form['password'],
            'role': 'employee'
        }

        if request.form['repeat_password'] != reg_data.get("password"):
            return render_template('auth/register.html', data={"message": "Пароли не совпадают"})

        response = req.post('http://127.0.0.1:8000/auth/register/', json=reg_data)
        if response.status_code == 200:
            return redirect(url_for(endpoint='login'))
    return render_template('auth/register.html', data={"message": "Произошла ошибка, попробуйте еще раз."})


# ЛОГИН
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('auth/sign-in.html')

    if request.method == "POST":
        log_data = {
            'username': request.form['username'],
            'password': request.form['password']
        }

        response = req.post('http://127.0.0.1:8000/auth/log-in/', json=log_data)

        if response.status_code == 200:
            data = response.json()
            session['access'] = data['access']
            session['refresh'] = data['refresh']
            session['user'] = data['user']
            return redirect(url_for(endpoint='index'))
        return jsonify({"message": "Error"})
    return jsonify({"error": "method error"})



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for(endpoint='login'))



# ГЛАВНАЯ СТРАНИЦА
@app.route("/", methods=['GET'])
def index():
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(access=session.get('access'), refresh=session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    return render_template('index.html')


                                                        ###########
                                                        # КЛИЕНТЫ #
                                                        ###########


# просмотр клиентов
@app.route("/clients", methods=['GET'])
def get_clients():
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(session.get('access'), session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    headers = {
        "Authorization": f"Bearer {session.get('access')}"
    }

    clients = req.get('http://127.0.0.1:8000/clients/', headers=headers)
    clients = clients.json()
    return render_template('clients/clients.html', clients=clients)



# просмотр конкретного клиента
@app.route("/client/<int:id>", methods=['GET'])
def get_client_id(id):
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(session.get('access'), session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    headers = {
        "Authorization": f"Bearer {session.get('access')}"
    }

    client = req.get(f'http://127.0.0.1:8000/clients/{id}/', headers=headers)
    contracts = req.get(f'http://127.0.0.1:8000/eq-contract/eq-client/{id}/', headers=headers)
    contracts = contracts.json()
    client = client.json()
    return render_template('clients/client_id.html', client=client, contracts=contracts)



# обновление клиента
@app.route('/client-update/<int:id>', methods=['GET', 'POST'])
def client_update(id):
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(access=session.get('access'), refresh=session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    if request.method == "GET":
        headers = {
            "Authorization": f"Bearer {session.get('access')}"
        }
        response = req.get(f'http://127.0.0.1:8000/clients/{id}/', headers=headers)
        data = response.json()
        return render_template('clients/client_update.html', data=data)

    if request.method == "POST":
        new_data_client = {
            'name': request.form['name'],
            'unp': request.form['unp']
        }
        headers = {
            "Authorization": f"Bearer {session.get('access')}"
        }
        try:
            response = req.put(f'http://127.0.0.1:8000/clients/{id}/', json=new_data_client, headers=headers)
            if response.status_code == 200:
                return redirect(url_for('get_client_id', id=id))
            else:
                return render_template('clients/client_update.html',
                                       data={"id": id, "error": "Ошибка обновления"})
        except Exception as e:
            return render_template('clients/client_update.html',
                                   data={"id": id, "error": f"Ошибка сервера: {str(e)}"})
    return redirect(url_for(endpoint='get_client_id', id=id))


# создание клиента
@app.route('/create-client', methods=['GET', 'POST'])
def client_create():
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(access=session.get('access'), refresh=session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    if request.method == "GET":
        return render_template('clients/create_client.html', data=None)

    if request.method == "POST":
        new_client = {
            'name': request.form['name'],
            'unp': request.form['unp']
        }
        headers = {
            "Authorization": f"Bearer {session.get('access')}"
        }
        try:
            response = req.post(f'http://127.0.0.1:8000/clients/', json=new_client, headers=headers)
            if response.status_code == 200:
                id = response.json()['new_clients']['id']
                return redirect(url_for('get_client_id', id=id))
            else:
                return render_template('clients/create_client.html',
                                       data={"error": "Ошибка создания. Попробуйте еще раз"})
        except Exception as e:
            return render_template('clients/create_client.html',
                                   data={"error": f"Ошибка: {str(e)}"})
    return redirect(url_for(endpoint='get_clients'))



                                                        ##############
                                                        # УСТРОЙСТВА #
                                                        ##############



@app.route('/eq-contracts', methods=['GET'])
def get_eq_contracts():
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(access=session.get('access'), refresh=session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    headers = {
        "Authorization": f"Bearer {session.get('access')}"
    }

    response = req.get('http://127.0.0.1:8000/eq-contract/', headers=headers)
    contracts = response.json()


    return render_template('eq_contracts/contracts.html', contracts=contracts)



@app.route('/eq-contract/<int:id>', methods=['GET'])
def get_eq_contract_id(id):
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(access=session.get('access'), refresh=session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    headers = {
        "Authorization": f"Bearer {session.get('access')}"
    }

    response_contract = req.get(f'http://127.0.0.1:8000/eq-contract/{id}/', headers=headers)
    response_transactions = req.get(f'http://127.0.0.1:8000/eq-contract/transactions-contract/{id}/', headers=headers)
    contract = response_contract.json()
    transactions = response_transactions.json()

    return render_template('eq_contracts/contract_id.html', contract=contract, transactions=transactions)


                                                            ##############
                                                            # ТРАНЗАКЦИИ #
                                                            ##############


@app.route('/transactions', methods=['GET'])
def get_transactions():
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(access=session.get('access'), refresh=session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    headers = {
        "Authorization": f"Bearer {session.get('access')}"
    }

    response_transactions = req.get(f'http://127.0.0.1:8000/eq-contract/transactions', headers=headers)
    transactions = response_transactions.json()

    return render_template('transactions/transactions.html', transactions=transactions)



@app.route('/transactions/<int:id>', methods=['GET'])
def get_transaction_id(id):
    if 'access' not in session:
        print('Нет токена')
        return redirect(url_for(endpoint='login'))
    if check_token(access=session.get('access'), refresh=session.get('refresh')) == False:
        session.clear()
        return redirect(url_for(endpoint='login'))

    headers = {
        "Authorization": f"Bearer {session.get('access')}"
    }

    response_transaction = req.get(f'http://127.0.0.1:8000/eq-contract/transactions/{id}', headers=headers)
    transaction = response_transaction.json()

    return render_template('transactions/transaction_id.html', transaction=transaction)





if __name__ == "__main__":
    app.run(debug=True, port=5000)
