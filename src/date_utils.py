from datetime import datetime, timedelta

def get_date_range_from_month(reference_month):
    try:
        start_date = datetime.strptime(reference_month, "%Y-%m")
        end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        return start_date.strftime("%Y-%m-%dT00:00:00.000000-03:00"), end_date.strftime("%Y-%m-%dT23:59:59.999999-03:00")
    except ValueError:
        print("Formato de mês inválido. Use o formato YYYY-MM.")
        return None, None
