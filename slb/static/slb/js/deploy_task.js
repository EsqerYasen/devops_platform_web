function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

vm = new Vue({
    el: "#app",
    data: {
        task_id: "100",
        task_status: "created",
        site_name: "siteA",
        nginx_cluster_id: "",
        version: "3",
        host_list:[
            //{id: "1", ip: '1.1.1.1', version:"siteA-2", time: '2018-08-10 09:00:00'},
            //{id: "2", ip: '1.1.1.1', version:"siteA-2", time: '2018-08-10 09:00:00'}, 
            //{id: "3", ip: '1.1.1.1', version:"siteA-2", time: '2018-08-10 09:00:00'},
            //{id: "4", ip: '1.1.1.1', version:"siteA-2", time: '2018-08-10 09:00:00'},
            //{id: "5", ip: '1.1.1.1', version:"siteA-2", time: '2018-08-10 09:00:00'},
            //{id: "6", ip: '1.1.1.1', version:"siteA-2", time: '2018-08-10 09:00:00'},
            //{id: "7", ip: '1.1.1.1', version:"siteA-2", time: '2018-08-10 09:00:00'}
        ],
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
        tmp4 = tmp2[1].split("="); //nginx_cluster_id： k-v
        tmp5 = tmp2[2].split("="); //version： k-v
        tmp6 = tmp2[3].split("="); //task_id： k-v
        this.site_name = tmp3[1]; 
        this.nginx_cluster_id = tmp4[1];
        this.version = tmp5[1];
        this.task_id = tmp6[1];
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
        },

        start_publish: function(){
            data = {id: this.task_id, hosts: this.host_list, version: this.version}
            this.postData('/slb/rest/deployagent/', data, this.afterStartPublish)
        },

        afterStartPublish: function(resp){
            var ws = new WebSocket("ws://localhost:8000/slb/ws/rtlog/");
            ws.onopen = function() {
              console.log("open");
              ws.send("hello");
            };
            console.log(resp.data);
        }
    }
});

