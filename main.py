import os

from datetime import date
from dateutil.relativedelta import relativedelta
from gspread import service_account

from api_util import get_log_data
from api_fields import hit_field_list, visit_field_list


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    counter_id1 = os.getenv("COUNTER_PLATFORM")
    counter_id2 = os.getenv("COUNTER_CARGOSEARCH")  # Add another counter ID
    api_host_url = "https://api-metrika.yandex.ru"

    start_date = os.getenv("START_DATE")
    yesterday = (date.today() - relativedelta(days=1)).strftime("%Y-%m-%d")
    end_date = os.getenv("END_DATE", default=yesterday)

    data_list_platform = [{
        "source": "hits",
        "api_field_list": hit_field_list,
        "google_sheet_url": os.getenv("HIT_SHEET_URL_PLATFORM")
    }, {
        "source": "visits",
        "api_field_list": visit_field_list,
        "google_sheet_url": os.getenv("VISIT_SHEET_URL_PLATFORM")
    }]
    gc = service_account()

    for data_elem in data_list_platform:
        data = get_log_data(api_host_url,
                            counter_id,
                            token,
                            data_elem["source"],
                            start_date,
                            end_date,
                            data_elem["api_field_list"])

        sh = gc.open_by_url(data_elem["google_sheet_url"])
        sh.sheet1.update([data.columns.values.tolist()]
                         + data.fillna("Unknown").values.tolist())
        
    data_list_cargosearch= [{
        "source": "hits",
        "api_field_list": hit_field_list,
        "google_sheet_url": os.getenv("HIT_SHEET_URL_CARGOSEARCH")
    }, {
        "source": "visits",
        "api_field_list": visit_field_list,
        "google_sheet_url": os.getenv("VISIT_SHEET_URL_CARGOSEARCH")
    }]
    gc = service_account()

    for data_elem in data_list_cargosearch:
        data = get_log_data(api_host_url,
                            counter_id,
                            token,
                            data_elem["source"],
                            start_date,
                            end_date,
                            data_elem["api_field_list"])

        sh = gc.open_by_url(data_elem["google_sheet_url"])
        sh.sheet1.update([data.columns.values.tolist()]
                         + data.fillna("Unknown").values.tolist())
