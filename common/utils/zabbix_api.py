from common.utils.HttpUtils import *
from devops_platform_web.settings import ZABBIX_USERNAME,ZABBIX_PASSWORD,ZABBIX_URL
import logging,time

logger = logging.getLogger('devops_platform_wap')

zabbix_auth = None

class zabbix_api():

    def __init__(self):
        global zabbix_auth
        if zabbix_auth is None or zabbix_auth == '':
            self.login()

    def login(self):
        global zabbix_auth
        try:
            data = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": ZABBIX_USERNAME,
                    "password": ZABBIX_PASSWORD
                },
                "id": 1,
            }
            login_result = HttpUtils(None).post2(ZABBIX_URL,data)
            if login_result.status_code == 200:
                result = login_result.json()
                zabbix_auth = result['result']
        except Exception as e:
            logger.error(e,exc_info=1)

    def get_event(self,time_from = None,time_till = None,count=50):
        global zabbix_auth
        if time_from is None:
            time_from = int(time.time()-60*10)
            time_till = int(time.time())
        try:
            data = {
                "jsonrpc": "2.0",
                "method": "event.get",
                "params": {
                    "output": "extend",
                    "time_from": time_from,
                    "time_till": time_till,
                    "sortfield": ["clock", "eventid"],
                    "sortorder": "DESC"
                },
                "auth": zabbix_auth,
                "id": 1
            }
            event_result = HttpUtils(None).post2(ZABBIX_URL,data)
            event_list = event_result.json().get("result", [])
            event_list = event_list[0:count]
        except Exception as e:
            logger.error(e,exc_info=1)
        return event_list

    def get_alert(self):
        result = []
        global zabbix_auth
        try:
            event_list = self.get_event()
            eventIds = []
            for event in event_list:
                eventIds.append(event['eventid'])
            data = {
                "jsonrpc": "2.0",
                "method": "alert.get",
                "params": {
                    "output": "extend",
                    "eventids": eventIds
                },
                "auth": zabbix_auth,
                "id": 1
            }
            alert_result = HttpUtils(None).post2(ZABBIX_URL,data)
            alert_list = alert_result.json().get("result", [])
            for alert in alert_list:
                result.append({"subject":alert['subject'],
                               "actualValue":alert['retries'],
                               "eventTime":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(alert['clock']))),
                               "eventId":alert['eventid']})
        except Exception as e:
            logger.error(e,exc_info=1)
        return result
