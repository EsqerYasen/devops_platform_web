from common.utils.HttpUtils import *
from .cell import *

import redis

def delete_file(file_path):
    pass

class CmdbCellTable():
    """
     
    """
    
    def __init__(self, request, serivceName='cmdb'):
        self.hu = HttpUtils(request)
        self.serivceName = serivceName
    
    def insert(self, cell_config, restName='/rest/cell/add/'):
        """
        insert cell into DB:cmdb_host, cmdb_hostgroup, cmdb_hostgrp;
        cell_config is a list, item in list is:
        {
	        'ip': '2.4.1.1',
	        'cpu': 2.0,
	        'mem': 4.0,
	        'disk': 50.0,
	        'node_name': 'kfc_preorder_nh_online_sgemfb8r_jar2'
        }
        connections is a dict:
        {
            '4.8.1.4': [
                {
                    'ip': '4.8.1.5',
                    'node_name': 'kfc_preorder_nh_pilot_ikxmhb8r_nginx-1',
                    'node_type': 'middle_ware'
                },
                {
                    'ip': '2.4.1.6',
                    'node_name': 'kfc_preorder_nh_pilot_ikxmhb8r_mysql-1',
                    'node_type': 'middle_ware'
                }
            ]
        }
        """
        res = self.hu.post(
            serivceName= self.serivceName, 
            restName=restName, 
            datas=cell_config
        )

        print(res)

    def get_cell_config(self, cell_id, restName='/rest/cell/gethostlistbycellname/'):
        # cell_config = [{
        #         'ip': '2.4.1.1',
        #         'cpu': 2.0,
        #         'mem': 4.0,
        #         'disk': 50.0,
        #         'node_name': 'kfc_preorder_nh_online_sgemfb8r_jar2'
        #     },
        #     {
        #         'ip': '2.4.1.1',
        #         'cpu': 2.0,
        #         'mem': 4.0,
        #         'disk': 50.0,
        #         'node_name': 'kfc_preorder_nh_online_sgemfb8r_jar2'
        #     }
        # ]
        # cell_id = 'fuom9b8r'
        res = self.hu.get(
            serivceName= self.serivceName, 
            restName=restName, 
            datas=dict(cellname=cell_id)
        )
        if res['status']!=200:
            return []
        return res['results']
    
    def get_cell_connections(self, cell_id):
        
        # http://172.29.164.92:8000/rest/cell/gethostlistbycellname?cellname=re2m9b8r
        connections = {'172.29.164.91':
                        [
                            {
                                'ip':'172.29.164.92',
                                'node_type':'nginx'
                            }
                        ]
                    }
        return connections

class RedisMQ():

    def __init__(self, cell_id):
        self.__conn = redis.Redis(host='172.29.164.91', db=10)
        self.chan_pub = cell_id
        # self.chan_pub = 'fm104.5'

    def publish(self, msg):
        self.__conn.publish(self.chan_pub,msg)
 
        return True
