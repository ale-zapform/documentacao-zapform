import requests

def get_status_count(auth_token, config_id, start_date, end_date, status):
    url = f"https://api.zapform.com.br/api/zc/{config_id}/order/?status={status}&time_created__gt={start_date}&time_created__lte={end_date}"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Token {auth_token}",
        "X-CSRFToken": "pd0c6XV4WWSqqqYPW2oSeHBM9YimZmKsDp02AfN0MdOSOsBZ4idbSAJNgXC4FgeQ"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        count = data.get("count", 0)
        return count
        
    except requests.exceptions.RequestException as e:
        print(f"Error for status {status} in config {config_id}: {e}")
        return None
