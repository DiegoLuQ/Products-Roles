import secrets
from datetime import datetime, date, timedelta
import pytz


chile_tz = pytz.timezone("America/Santiago")

def generate_api_key():
    date_chile = datetime.now(chile_tz)
    start_date = date_chile
    exp_date = date_chile + timedelta(days=7)

    data = {
        "api_key":secrets.token_urlsafe(16),
        "start_date": start_date.date(),
        "exp_date": exp_date.date()
    }
    return data



def format_date(date:str):
    date_format = "%Y-%m-%d"
    convert_data = datetime.strptime(date, date_format)

def convert_str_to_date(date_str:str) -> date:
    convert_data = format_date(date_str)
    new_date = convert_data + timedelta(days=7)
    return new_date


def compare_exp_date_current_date(date_str):
    fecha_end = format_date(date_str)
    current_date = datetime.now(chile_tz).date()
    if fecha_end.date() <= current_date:
        return {"msg":"Tu API Key ha caducado", "is_ok": False}
    else:
        expire_in = fecha_end.date() - current_date
        return {"msg":"Aun tenemos tiempo", "expira_en":f" API Key expira en: {expire_in}", "date_end":str(fecha_end.date()), "is_ok":True}

