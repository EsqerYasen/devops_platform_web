function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

status_dict = {'0': 'running', '1': 'ok', '2': 'failed'}
function startWS(ip_list, site_id){
    ws = new WebSocket("ws://localhost:8000/slb/ws/rtlog/");

    ws.onopen = function() {
        console.log("open");
        data = JSON.stringify({ip_list: ip_list, site_id: site_id});
        ws.send(data);
    };

    ws.onmessage = function(msg){
        ws.send('ok')
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

vm = new Vue({
    el: "#app",
    data: {
        task_id: "100",
        task_status: "created",
        site_name: "siteA",
        site_id: "",
        nginx_cluster_id: "",
        version: "3",
        host_list:[],
        pre_hosts: [],
        log: "aaaaaaaaaaaa\naaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaa",
        loading: true

    },
    created: function(){
        window_href = window.location.href;
        //console.log(window_href);
        tmp1 = window_href.split("?"); //args_str
        tmp2 = tmp1[1].split("&"); //args
        tmp3 = tmp2[0].split("="); //site_name: k-v
        tmp7 = tmp2[1].split("="); //site_id： k-v
        tmp4 = tmp2[2].split("="); //nginx_cluster_id： k-v
        tmp5 = tmp2[3].split("="); //version： k-v
        tmp6 = tmp2[4].split("="); //task_id： k-v
        this.site_name = tmp3[1]; 
        this.nginx_cluster_id = tmp4[1];
        this.version = tmp5[1];
        this.task_id = tmp6[1];
        this.site_id= tmp7[1];
        //console.log(site_name);
        //console.log(nginx_cluster_id);
        this.getHosts(this.site_name, this.nginx_cluster_id);
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
                console.log(resp);
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
            console.log(val);
            this.pre_hosts = val;
        },

        getHosts: function(site_name, nginx_cluster_id){
            data = {id: nginx_cluster_id, vs: site_name};
            this.getData('/slb/rest/nginxclusterhostbyid/', data, this.afterGetHosts);
        },

        afterGetHosts: function(resp){
            console.log(resp.data);
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

        start_publish: function(){
            data = {id: this.task_id, hosts: this.host_list, version: this.version}
            this.postData('/slb/rest/deployagent/', data, this.afterStartPublish)
        },

        afterStartPublish: function(resp){
            console.log(resp.data);
            startWS(this.host_list, this.version);
        },

        getLog: function(row){
            console.log(row.host_ip);
            data={'ip':row.host_ip, 'siteId':this.site_id, 'deployId': this.task_id, 'version': this.version};
            this.getData('/slb/rest/nginxdeploylogsbyip', data, this.afterGetLog);
        },

        afterGetLog: function(resp){
            this.log = resp.data['log'];
        }
    }
});

