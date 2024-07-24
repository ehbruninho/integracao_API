import requests
from mysql.connector import Error
import mysql.connector
import json


def create_conn():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='cloudmigra.com.br',
            user='cloudmigracom_megazap',
            password='!@#Nova!@#',
            database='cloudmigracom_glpi'
        )
        if conn.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn

def fetch_query(conn, query):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

def execute_query(conn, query, data=None):
    cursor = conn.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        conn.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
conn = create_conn()

def valida_cnpj(cnpj):
    try:
        select_cnpj_query = "SELECT id FROM glpi_entities where cpf_cnpj = '{}'".format(cnpj)
        cursor = conn.cursor()
        cursor.execute(select_cnpj_query)
        result = cursor.fetchall()

        if result:
            print(f" CNPJ encontrado, cliente {cnpj} {result[0][0]}")
            encontra_Token(result[0][0])
            return result[0][0]
        else:
            print("CNPJ não encontrado")
            return None

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return None

    finally:
        cursor.close()
        conn.close()

def encontra_Token(id_entidade):
    try:
        select_token_query = "SELECT api_token FROM glpi_users where entities_id = '{}'".format(id_entidade)
        cursor = conn.cursor()
        cursor.execute(select_token_query)
        result = cursor.fetchall()

        if result:
            op = ''
            print(f"Cliente  encontrado id_entidade = {id_entidade} api_token = {result[0][0]}")
            op = input("1 - Incluir Ticket \n2 - Consultar ticket\n")
            if op == '1':
                incluir_chamado_api(result[0][0])
            else:
                consulta_tickets_api(result[0][0])
            return result[0][0]
        else:
            print("Cliente não encontrado")
            return None

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return None

    finally:
        cursor.close()
        conn.close()

def consultar_entidades():

    select_entidades_query = "SELECT *  FROM glpi_entities"
    entidades = fetch_query(conn, select_entidades_query)

    for entidade in entidades:
        print(entidade)

def consulta_tickets_api(token):
    glpi_url = "http://54.207.73.132/glpi/apirest.php" # Glpi/Configuração/Geral
    api_token = token# Gerado na função encontra Token


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"user_token {api_token}",
        "App-Token": "fAebGLTWJRwvadzW0gsWeuLune8ojtZtiWh1xuKp"# Gerado no GLPI Em API/Token
    }

    response = requests.get(f"{glpi_url}/initSession", headers=headers)
    session_data = response.json()
    session_token = session_data['session_token']
    headers['Session-Token'] = session_token


    tickets_url = f"{glpi_url}/Ticket"
    params = {
    "forcedisplay[0]": "id",
    "forcedisplay[1]": "name",
    "forcedisplay[2]": "status",
    "forcedisplay[3]": "date",
    "forcedisplay[4]": "entities_id"
    }

    response = requests.get(tickets_url, headers=headers, params=params)
    tickets = response.json()

    tickets_entidade = [ticket for ticket in tickets]

    for chamados in tickets_entidade:
        print(chamados)

    close_session_url = f"{glpi_url}/killSession"
    response = requests.post(close_session_url, headers=headers)
    print(response.json())

def incluir_chamado_api(token):
    glpi_url = "http://54.207.73.132/glpi/apirest.php"  # Glpi/Configuração/Geral
    api_token = token  # Gerado na função encontra Token

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"user_token {api_token}",
        "App-Token": "fAebGLTWJRwvadzW0gsWeuLune8ojtZtiWh1xuKp"  # Gerado no GLPI Em API/Token
    }
    # Criar sessão
    response = requests.get(f"{glpi_url}/initSession", headers=headers)
    session_data = response.json()
    session_token = session_data['session_token']
    headers['Session-Token'] = session_token


    def criar_ticket(title, description):
        ticket_data = {
            "input": {
                "name": title,
                "content": description,
                "status": 1  # Status inicial do ticket (ajuste conforme necessário)
            }
        }

        response = requests.post(f"{glpi_url}/Ticket", headers=headers, data=json.dumps(ticket_data))

        if response.status_code == 201:
            ticket = response.json()
            print(f"Ticket criado com sucesso: ID={ticket['id']}")
            return ticket
        else:
            print(f"Erro ao criar ticket: {response.status_code} - {response.text}")
            return None

    # Solicitar que o cliente insira os detalhes do ticket
    title = input("Digite o título do ticket: ")
    description = input("Digite a descrição do ticket: ")

    criar_ticket(title, description)

    close_session_url = f"{glpi_url}/killSession"
    response = requests.post(close_session_url, headers=headers)
    print(response.json())

cnpj_cliente = input("Digite o CNPJ: ")
valida_cnpj(cnpj_cliente)