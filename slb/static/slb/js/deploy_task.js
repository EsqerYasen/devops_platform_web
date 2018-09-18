function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

var ws=null;

function startWS(ip_list, site_id){
    ws = new WebSocket("ws://localhost:8000/slb/ws/rtlog/");

    ws.onopen = function() {
        console.log("open");
        data = JSON.stringify({ip_list: ip_list, site_id: site_id, cmd: "start"});
        ws.send(data);
    };

    ws.onmessage = function(msg){
        ws.send(JSON.stringify({cmd: "ack"}));
        console.log(msg.data);
        tmp_list = JSON.parse(msg.data);
        for(var i=0;i<tmp_list.length;i++){
            var ip = tmp_list[i]['ip']
            var tmp_status = tmp_list[i]['status']
            var status = status_dict[tmp_status]
            for(var j=0;j<vm.host_list.length;j++){
                if(vm.host_list[j]['host_ip']==ip){
                    Vue.set(vm.host_list[j], 'status', status);
                }
            }
        }
    }
}

status_dict = {'0': 'running', '1': 'ok', '2': 'failed'}

function parserUrlParams(paramStr){
    params = paramStr.split("&");
    param_dict = {}
    for(var i=0;i<params.length;i++){
        var param = params[i];
        var tmp = param.split("=");
        param_key = tmp[0];
        param_value = tmp[1];
        param_dict[param_key] = param_value;
    }
    return param_dict;
}

vm = new Vue({
    el: "#app",
    data: {
        task_id: 100,
        task_status: "created",
        site_name: "siteA",
        site_id: "",
        nginx_cluster_id: "",
        host_list:[],
        pre_hosts: [],
        log: "",
        loading: true,
        currentVersion: "",
        versions: [],
        ws: null

    },
    created: function(){
        var params_dict = parserUrlParams(window.location.search.substr(1));
        this.site_name = params_dict['site_name']; 
        this.nginx_cluster_id = params_dict['nginx_cluster_id'];
        //this.task_id = params_dict['task_id'];
        this.site_id= params_dict['site_id'];
        //console.log(site_name);
        //console.log(nginx_cluster_id);
        this.getHosts(this.site_name, this.nginx_cluster_id);
        this.getVersion();
    },
    methods:{
        getData: function(url, params, func){
            obj = this;
            axios({
                method:'GET',
                url: url,
                params: params
            }).then(function(resp){
                func(resp);
            }).catch(function(resp){
                console.log('Fail:'+resp.status+','+resp.statusText);
            });
        },

        postData: function(url, data, func){
            obj = this;
            axios({
                method:'POST',
                url: url,
                data:data
            }).then(function(resp){
                func(resp);
            }).catch(resp => {
                console.log('Fail:'+resp.status+','+resp.statusText);
            });
        },

        handleSelectionChange: function(val){
            //console.log(val);
            this.pre_hosts = val;
        },

        getHosts: function(site_name, nginx_cluster_id){
            data = {id: nginx_cluster_id, vs: site_name};
            this.getData('/slb/rest/nginxclusterhostbyid/', data, this.afterGetHosts);
        },

        afterGetHosts: function(resp){
            //console.log(resp.data);
            this.host_list = resp.data.data;
            this.loading = false;
            for(var i=0;i<this.host_list.length;i++){
                if(this.host_list[i]['status']==200){
                    this.host_list[i]['status'] = 'ready';
                }
                else{
                    this.host_list[i]['status'] = 'disconnected';
                }
            }
        },

        getVersion: function(id){
            this.getData('/slb/rest/deployversionbysiteid', {id:this.site_id}, this.afterGetVersion);
        },

        afterGetVersion: function(resp){
            var tmp = resp.data['ret'];
            //console.log(tmp);
            this.currentVersion = tmp[0];
            this.versions = tmp;
        },

        start_publish: function(){
            data = {id: this.site_id, hosts: this.pre_hosts, version: this.currentVersion}
            this.postData('/slb/rest/deployagent/', data, this.afterStartPublish)
        },

        afterStartPublish: function(resp){
            //console.log(resp.data);
            this.task_id = resp.data.task_id;
            //if(ws == null){
                startWS(this.pre_hosts, this.site_id); 
            //}
            //else{ 
                //ws.close(); 
                //startWS(this.pre_hosts, this.site_id); }
        },

        getLog: function(row){
            //console.log(row.host_ip);
            data={ip:row.host_ip, siteId:this.site_id, deployId: this.task_id, version: this.currentVersion};
            this.getData('/slb/rest/nginxdeploylogsbyip', data, this.afterGetLog);
        },

        afterGetLog: function(resp){
            //console.log(resp);
            this.log = resp.data['log'];
        },

        handleCommand: function(command){
            this.currentVersion = command;
        }
    }
});

