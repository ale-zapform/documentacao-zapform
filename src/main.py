import string
from auth import get_auth_token
from config import get_configs_and_status_names
from date_utils import get_date_range_from_month
from orders import get_status_count
from spreadsheet import gerar_planilha  # Importando o novo módulo de planilhas

def main():
    # Perguntar ao usuário se quer fornecer ZF Client ou config IDs
    input_type = input("Você deseja fornecer (1) ZF Clients ou (2) Config IDs? Informe 1 ou 2: ").strip()

    # Validação do tipo de entrada
    if input_type == "1":
        input_type_desc = "ZF Clients"
    elif input_type == "2":
        input_type_desc = "Config IDs"
    else:
        print("Opção inválida. Por favor, informe 1 ou 2.")
        return

    # Entrada de ZF Clients ou Config IDs, e mês de referência
    input_values = input(f"Informe os {input_type_desc} separados por vírgula: ").split(",")
    reference_month = input("Informe o mês de referência (formato YYYY-MM): ")

    # Calcular start_date e end_date
    start_date, end_date = get_date_range_from_month(reference_month)
    if not start_date or not end_date:
        return

    auth_token = get_auth_token()
    status_list = list(map(str, range(10))) + list(string.ascii_uppercase)  # Status de "0" a "9" e "A" a "Z"

    # Lista para armazenar os dados da planilha geral
    data_geral = []

    # Dicionário para armazenar os dados de cada cliente ou config
    data_por_cliente = {}

    # Variável para armazenar o total de ordens de todos os clientes ou configs
    total_geral_ordens = 0

    # Iterar por cada valor informado (ZF Clients ou Config IDs)
    for input_value in input_values:
        input_value = input_value.strip()  # Remover espaços em branco
        print(f"\nProcessando {input_type_desc} {input_value} para o mês de {reference_month}")

        if input_type == "1":
            # Obter todas as configs e nomes de status do ZF Client
            configs, status_mapping = get_configs_and_status_names(auth_token, input_value)
        else:
            # Se o usuário optou por Config IDs, criar uma lista de um único config
            configs = [{"id": input_value, "name": f"Config {input_value}"}]
            status_mapping = {status: f"Status {status}" for status in status_list}

        if not configs:
            print(f"Nenhuma config encontrada para o {input_type_desc} {input_value}.")
            continue

        print(f"Configs encontradas para {input_type_desc} {input_value}: {configs}")
        print(f"Nomes dos Status encontrados: {status_mapping}")

        # Lista para armazenar dados por cliente (para a aba individual)
        data_cliente = []

        # Contador de ordens por configuração e por cliente
        total_orders_per_config = 0
        total_orders_per_client = 0

        # Iterar por cada config e contar as ordens por status
        for config in configs:
            config_id = config["id"]
            config_name = config["name"]
            print(f"\nProcessando config: {config_id} - {config_name}")
            
            # Adiciona uma linha de título para cada configuração no cliente
            data_cliente.append([f"Config: {config_name}", f"Config ID: {config_id}", "", "", "", ""])
            
            # Armazena as informações de status para a aba de cliente
            total_orders_config = 0  # Inicializar o contador de ordens para cada configuração
            for status in status_list:
                count = get_status_count(auth_token, config_id, start_date, end_date, status)
                if count is not None and count > 0:
                    status_name = status_mapping.get(status, "Status desconhecido")
                    print(f"Status {status} ({status_name}): {count} ordens")
                    
                    # Adicionando os dados na lista geral e na lista do cliente
                    data_geral.append([input_value, config_id, config_name, status, status_name, count])
                    data_cliente.append([status, status_name, count, "", "", ""])
                    
                    total_orders_config += count  # Incrementar o total de ordens por configuração

            # Adicionar total de ordens por configuração no final
            data_cliente.append(["Total de ordens", "", total_orders_config, "", "", ""])
            total_orders_per_config += total_orders_config  # Incrementar o total geral para o cliente ou config

        # Adicionar o total geral de ordens do cliente ou config
        data_cliente.append(["", "", "", "", "", ""])  # Linha em branco
        data_cliente.append(["Total Geral de Ordens", "", total_orders_per_config, "", "", ""])
        
        # Incrementar o total geral de ordens de todos os clientes ou configs
        total_geral_ordens += total_orders_per_config

        # Adicionar o total de ordens por cliente/config na planilha geral
        data_geral.append([input_value, "", "", "", "Total de ordens", total_orders_per_config])
        
        # Adiciona os dados por cliente/config no dicionário
        data_por_cliente[input_value] = data_cliente

    # Adicionar o total de ordens de todos os clientes/configs na planilha geral
    data_geral.append(["Total de ordens de todos os clientes/configs", "", total_geral_ordens, "", "", ""])

    # Gerar a planilha utilizando o módulo "spreadsheet.py"
    gerar_planilha(data_geral, data_por_cliente, reference_month)

if __name__ == "__main__":
    main()
