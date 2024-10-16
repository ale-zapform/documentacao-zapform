import requests

def get_auth_token():
    login_url = "https://admin.zapform.com.br/api/auth/login/"
    login_payload = {
        "username": "integracao-zapform",
        "password": "Senha@02"
    }

    response = requests.post(login_url, json=login_payload)
    response.raise_for_status()
    json_response = response.json()
    
    token = json_response.get("key")
    return token
