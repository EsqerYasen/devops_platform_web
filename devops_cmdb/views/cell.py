# -*-coding: utf8 -*-
import uuid
import copy

template  = {
    "jar1": {
        "count" : 4,
        "cpu": 4,
        "mem": 8,
        "disk": 50,
        "type": "jar",
        "middle_ware": ["nginx-1", "mysql-1"]
    },
    "jar2": {
        "count" : 4,
        "cpu": 2,
        "mem": 4,
        "disk": 50,
        "type": "jar",
        "middle_ware": ["nginx-2", "mysql-2"]
    },
    "nginx-1": {
        "count": 1,
        "cpu": 4,
        "mem": 8,
        "disk": 50,
        "type": "middle_ware",
    },
    "nginx-2": {
        "count": 1,
        "cpu": 2,
        "mem": 4,
        "disk": 50,
        "type": "middle_ware",
    },
    "mysql-1": {
        "count": 1,
        "cpu": 2,
        "mem": 4,
        "disk": 50,
        "type": "middle_ware",
    },
    "mysql-2":{
        "count": 1,
        "cpu": 2,
        "mem": 4,
        "disk": 50,
        "type": "middle_ware",
    }
}

def generate_short_uuid():
    # 生成8位码

    char_set = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ]
    uc = list()
    uu = str(uuid.uuid1()).replace("-", "")
    for i in range(8):
        sub_char = uu[i * 4: i * 4 + 4]
        num = int(sub_char, 16)
        uc.append(char_set[num % 0x24])
    return "".join(uc)
    # 0x3E 是16进制的62，上面列表有62个元素

SHEET_COL_DICT = [
    {"name": "ip", "type": "str"},
    {"name": "cpu", "type": "int"},
    {"name": "mem", "type": "int"},
    {"name": "disk", "type": "int"}
]

COL_COUNT = len(SHEET_COL_DICT)

class Cell():
    """
    """
    def __init__(self, template, parents):
        self.template = template
        self.parents = parents
        self.cell_id = self.__get_id()
        self.cell = dict(cell_id=self.cell_id, cell_config=[])
        self.__xls = None
        self.connections = {}
    
    def from_sheet(self, sheet):
        self.__xls = [ dict(zip(sheet.row_values(0), sheet.row_values(i)))
            for i in range(1, sheet.nrows)]
        self.__pair()
        self.__connection()
        assert self.__exist_rest_server() == False

    def from_sheet_dict(self, sheet_dict):
        pass

    def __connection(self):
        for host_ip in self.connections:
            remotes = self.connections[host_ip]
            remote_list = []
            for remote_name in remotes:
                for host in self.cell['cell_config']:
                    if host["node_name"].endswith(remote_name):
                        remote_list.append(
                            dict(
                                ip=host['ip'],
                                node_name=host['node_name'],
                                node_type=host['node_type']
                            )
                        )
                        break
            self.connections[host_ip] = remote_list

    def __pair(self):
        for obj_name in self.template.keys():
            obj_attr = self.template[obj_name]
            count = obj_attr["count"]
            while count>0:
                index = self.__find_server(obj_attr)
                assert index>=0
                node_name = '{parents}_{cell_id}_{obj_name}'.format(
                        parents = '_'.join(self.parents), 
                        cell_id = self.cell_id, 
                        obj_name = obj_name
                )
                self.__xls[index].update(dict(node_name=node_name, node_type=obj_attr["type"]))
                if 'middle_ware' in obj_attr.keys():
                    self.connections.update({self.__xls[index]['ip']:obj_attr['middle_ware']})
                count = count - 1
        self.cell["cell_config"] = self.__xls

    def __exist_rest_server(self):
        is_not_occupied = lambda x: not "node_name" in x.keys()
        tmp = filter(is_not_occupied, self.__xls)
        return bool(len(list(tmp)))

    def __find_server(self, obj_attr):
        is_not_occupied = lambda x: not "node_name" in x.keys()
        for index, server in enumerate(self.__xls):
            if server["cpu"] == obj_attr["cpu"] and server["mem"] == obj_attr["mem"] and server["disk"] == obj_attr["disk"] and is_not_occupied(server):
                return index
        return -1

    def __get_id(self):
        return generate_short_uuid()
        
def is_sheet_complete(sheet):
    """
    ensure:
    1. column count is correct
    2. there is no blank cell
    3. no duplicate ip in 'IP' column
    """

    #column count is correct
    if sheet.ncols != COL_COUNT:
        print("column count is incorrect, %s, %s"%(sheet.ncols, COL_COUNT))
        return False
    
    #there is no blank cell
    for i in range(sheet.nrows):
        for j in range(sheet.ncols):
           if len(str(sheet.cell(i,j).value)) == 0:
               print("there is blank cell")
               return False

    #no duplicate ip in 'IP' column
    ips = sheet.col_values(0)
    ips_after_filter = list(set(ips))
    if len(ips)!=len(ips_after_filter):
        print("duplicate ip")
        return False
        
    return True

if __name__ == "__main__":
    import xlrd
    import pprint
    workbook = xlrd.open_workbook('D:/Book1.xlsx')
    sheet = workbook.sheet_by_index(0) # read first sheet

    cc = Cell(template, ['kfc', 'preorder', 'nh', 'pilot'])

    cc.from_sheet(sheet)

    # pprint.pprint(cc.cell)
    # pprint.pprint(cc.connections)
    pprint.pprint(cc.test_connection())

