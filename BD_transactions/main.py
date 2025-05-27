import os
import random
import time
from psycopg2 import connect
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'dbname':os.getenv('DB_NAME'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'host':os.getenv('DB_HOST'),
    'port':os.getenv('DB_PORT')
}


def get_db_connection():
    return connect(**DB_CONFIG)


def insert_transaction(sum_transaction, num_card, sum_commission, contract_id):
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("""
        BEGIN;
            INSERT INTO eq_contract_eqtransactions(sum_transaction, num_card, sum_commission, contract_id, date_transaction) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
            UPDATE eq_contract_eqcontracts SET balance = balance + %s, commission = commission + %s WHERE id = %s;
        COMMIT;
        """, (sum_transaction, num_card, sum_commission, contract_id, sum_transaction, sum_commission, contract_id,));
    return True



def get_id():
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("""SELECT id FROM eq_contract_eqcontracts""")
        id_transactions = cur.fetchall()
    return id_transactions

c = 0
while True:
    try:
        sum_transaction = float(random.randint(1, 1000))
        num_card = random.randint(1000000000000000, 9999999999999999)
        sum_commission = round(sum_transaction * 0.05, 2)
        contract_id = random.choice([i[0] for i in get_id()])
        insert_transaction(sum_transaction, num_card, sum_commission, contract_id)
        print(sum_transaction, num_card, sum_commission, contract_id)
    except Exception as e:
        print("Ошибка", e)
    c += 1
    time.sleep(1)
    if c == 60:
        break

