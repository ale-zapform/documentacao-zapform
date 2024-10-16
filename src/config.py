import requests

def get_configs_and_status_names(auth_token, zfclient_id):
    url = f"https://api.zapform.com.br/api/v2/workflow/?zfclient={zfclient_id}"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Token {auth_token}",
        "X-CSRFToken": "GUAyZg8pK68CxsPKcoObQTJu0g6nBPhrGchOrhoOMnA8MZ0ZlZctA15a5B2HGmpc"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        configs = [{"id": config["id"], "name": config["name"]} for config in data["results"]]
        
        status_mapping = {}
        for config in data["results"]:
            for status in config.get("status", []):
                status_mapping[status["code"]] = status["status"]

        return configs, status_mapping
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching configs and statuses for zfclient {zfclient_id}: {e}")
        return [], {}
