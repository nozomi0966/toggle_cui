import urllib.request, json
from pytz import timezone
from datetime import datetime
import base64
import json
import settings


class Toggle:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.header = {
            "Content-Type" : "application/json",
            'Authorization': "Basic {}".format(
                self.encode_password_base64(password=self.api_token)
            )
        }

    def encode_password_base64(self, password: str):
        return base64.b64encode(
            '{}:api_token'.format(password).encode('utf-8')
        ).decode('utf-8')
    
    def format_dict_to_json(self, data: dict):
        return json.dumps(data).encode("utf-8")

    def send_request(self, url: str, method: str, header: dict, data=None):
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers=header,
        )
        with urllib.request.urlopen(req) as res:
            response_body = res.read().decode('utf-8')
        return response_body

    def start_toggle(self, description: str, tag: list, pid: int) -> dict:
        url = "https://www.toggl.com/api/v8/time_entries/start"
        data = {
            "time_entry":{
                "description":description,
                "tags":tag,
                "created_with":"python",
            }
        }
        res = self.send_request(
            url=url,
            method="POST",
            data=self.format_dict_to_json(data),
            header=self.header
        )
        res_dict = json.loads(res)
        return res_dict
    
    def runnning_toggle(self) -> dict:
        url = "https://www.toggl.com/api/v8/time_entries/current"
        res = self.send_request(
            url=url,
            method="GET",
            header=self.header
        )
        res_dict = json.loads(res)
        return res_dict

    def stop_toggle(self, time_entry_id: str) -> dict:
        url = 'https://www.toggl.com/api/v8/time_entries/{}/stop'.format(time_entry_id)
        res = self.send_request(
            url=url,
            method="PUT",
            header=self.header
        )
        res_dict = json.loads(res)
        return res_dict
        
def now_time()-> str:
    now_time = datetime.now(
        timezone('UTC')).astimezone(timezone('Asia/Tokyo')
    )
    now_time_str = now_time.strftime("%Y-%m-%dT%H:%M:%S")
    jst_data_un_formated = list(now_time.strftime('%z'))
    jst_data_formated ="{}:{}".format(
        "".join(jst_data_un_formated[0:3]),
        "".join(jst_data_un_formated[3:5])
    )
    return now_time_str + jst_data_formated


if __name__ == '__main__':
    tg = Toggle(settings.ACCSES_TOKEN)
    tg.runnning_toggle()
    # tg.start_toggle(
    #     description='APITEST',
    #     tag=["billed"],
    #     pid=123,
    # )