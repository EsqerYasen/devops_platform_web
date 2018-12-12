import json
import time
import redis

# from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer

step_name_dict = {
    "authorized_key": "授权密钥",
    "check_host_env": "检查机器环境",
    "init_host_var": "初始化机器参数",
    "install_middleware": "安装中间件",
    "install_app": "安装应用",
    "register": "注册配置",
    "start_app": "启动应用"
}

class RemoteCellLog():
    RUNNING = 0
    SUCCESS = 1
    FAIL = 2

    def __init__(self, cell_id, count, debug=False):
        self.cell_id = cell_id
        self.cell_step = "{cell_id}_step".format(cell_id=self.cell_id) #key: TEST_steps
        self.origin = None
        self.active_step = None
        self.server_count = count
        self.__log_cache = []
        self.__last_log_len = 0

    def from_redis(self, redis_config):
        r = redis.Redis(**redis_config)
        self.origin = r

    def is_finish(self, step):
        # is_tag = lambda step: step['step_tag']==step_tag
        # step = list(filter(is_tag, steps))[0]
        # return True if step['status'] > RemoteCellLog.RUNNING else False
        key_name = '{cell_id}_{step}'.format(
            cell_id=self.cell_id,
            step=step.lowrer()
        ) #key: TEST_PUSH_KEY_LOG
        return True if self.origin.llen(key_name)==self.server_count else False

    @staticmethod
    def is_all_finish(steps):
        for step in steps:
            if step['status']< RemoteCellLog.SUCCESS:
                return False
        return True

    @staticmethod    
    def get_actvie_step(steps):
        for step in steps:
            if step['status'] < RemoteCellLog.SUCCESS:
                return step['step_tag']
        else: return None

    def get_steps(self):
        """
        return steps info
        """
        tmp_steps =self.origin.lrange(self.cell_step, 0 ,-1)
        self.steps = [json.loads(str(step, encoding='utf8')) for step in tmp_steps]
        return self.steps

    @staticmethod
    def get_finished_steps(steps):
        return []

    def refresh(self):
        self.__refresh_step()
        # self.__refresh_log()

    def get_log_cache(self):
        log_cache = self.__log_cache
        self.__log_cache = []
        return log_cache

    def get_log(self, step):
        key_name = '{cell_id}_{step}'.format(
            cell_id=self.cell_id,
            step=step
        ) #key: TEST_PUSH_KEY_LOG
        return self.origin.lrange(key_name, 0, -1)

    def __refresh_step(self):
        """
        refresh step list and find the active_step
        when all of the steps have finished, active_step will be the last step
        """
        tmp_steps =self.origin.lrange(self.cell_step, 0 ,-1)
        self.steps = [json.loads(str(step, encoding='utf8')) for step in tmp_steps]
        self.active_step = self.__find_tag()

    def __refresh_log(self):
        key_name = '{cell_id}_{active_step}'.format(
            cell_id=self.cell_id,
            active_step=self.active_step.lower()
        ) #key: TEST_PUSH_KEY_LOG
        log_len = self.origin.llen(key_name)
        log_offset = log_len - self.__last_log_len
        if log_offset!=0:
            self.__log_cache = self.__log_cache + self.origin.lrange(self.active_step, 0, log_offset-1)
        self.__last_log_len = log_len

    def __find_tag(self):
        for step in self.steps:
            if step['status'] < RemoteCellLog.SUCCESS:
                return step['step_tag']
        else: return step['step_tag']

class CellConsumer(WebsocketConsumer):
# class CellConsumer(AsyncWebsocketConsumer):
    def connect(self):
        # handshake create connection
        self.accept()

    def receive(self, text_data=None, bytes_data=None, debug=True):
        # push message to group
        redis_config = dict(host='172.29.164.92', port=6060, db=6)
        data = json.loads(text_data)
        cell_id = data['cell_id']
        server_count = data['server_count']
        rl = RemoteCellLog(cell_id, server_count, debug=True)
        rl.from_redis(redis_config)
        # finished_steps = []
        #send log for finished steps
        while True:
            logs = dict()
            for step in step_name_dict.keys():
                # if not rl.is_finish(step):
                tmp = rl.get_log(step)
                tmp = [json.loads(str(t, encoding='utf8')) for t in tmp]                   
                logs.update(dict({step:tmp}))
            self.send(text_data=json.dumps(logs))
            time.sleep(3)
            # steps = rl.get_steps()
            # self.send(
            #     text_data=json.dumps(
            #         dict(msg_type='steps', data=steps)
            #     )
            # )
            # f_steps = RemoteCellLog.get_finished_steps(steps)
            # for step in f_steps:
            #     if not step in finished_steps:
            #         log = rl.get_log(step)
            
            #     self.send(
            #         text_data=json.dumps(
            #             dict(msg_type='logs', step=step, data=log)
            #         )
            #     )
            
            #     finished_steps.append(step)
            # active_step = RemoteCellLog.get_actvie_step(steps)
            # log = rl.get_log(active_step)
            # self.send(
            #     text_data=json.dumps(
            #         dict(msg_type='logs', step=step, data=log)
            #     )
            # )

            # if RemoteCellLog.is_all_finish(steps):
            #     break
            # time.sleep(3)

    def disconnect(self, close_code):
        # remove the channel from group when connection broken
        self.close()