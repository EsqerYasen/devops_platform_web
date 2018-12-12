function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

function findServer(ip){
    for(var i=0;i<vm.cell_config.length;i++){
        if(ip==vm.cell_config[i].ip){
            return i;
        }
    }
}

function authorizedKeyHanlder(step_logs){
    if(vm.push_key_not_finish==false){
        return;
    }
    if(step_logs.length==vm.cell_config.length){
        vm.push_key_not_finish = false;
    }
    for(var i=0;i<step_logs.length;i++){
        var host_log = step_logs[i];
        var index = findServer(host_log.IP);
        if(host_log.Status == 200){
            Vue.set(vm.hosts[index], 'status', 'success');
        }
        else{
            Vue.set(vm.hosts[index], 'status', 'fail');
        }
    }
    for(var i=0;i<vm.hosts.length;i++){
        if(vm.hosts[i].status=='success'){
            vm.success_count = vm.success_count + 1;
        }
        if(vm.hosts[i].status=='fail'){
            vm.fail_count = vm.fail_count + 1;
        }
    }
    if(vm.success_count==vm.cell_config.length){
        vm.unReadyForDeploy=false;
    }
}

function deployHanlder(logs){
    // "check_host_env": "检查机器环境",
    // "init_host_var": "初始化机器参数",
    // "install_middleware": "安装中间件",
    // "install_app": "安装应用",
    // "register": "注册配置",
    // "start_app": "启动应用"
    var step_list = ['start_app', 'register', 'install_app', 'install_middleware', 'init_host_var', 'check_host_env']
    for(var i=0;i<vm.cell_config.length;i++){
        var ip=vm.cell_config[i].ip;
        var is_not_found=true;
        for(var j=0;j<step_list.length&&is_not_found;j++){
            var step = step_list[j]
            var step_logs = logs[step]
            for(var k=0;k<step_logs.length;k++){
                var host_log = step_logs[k];
                if(step_logs[k].IP==ip){
                    is_not_found=false;
                    Vue.set(vm.hosts[i], 'step', step);
                    if(host_log.Status == 200){
                        Vue.set(vm.hosts[i], 'status', 'success');
                    }
                    else{
                        Vue.set(vm.hosts[i], 'status', 'fail');
                    }
                    break;
                }
            }
        }
    }
}

function startWS(cell_id, count){
    vm.ws = new WebSocket("ws://"+window.location.host+"/cmdb/cell/pull");

    vm.ws.onopen = function() {
        console.log("open");
        data = JSON.stringify({'cell_id':cell_id, 'server_count':count});
        vm.ws.send(data);
    };

    vm.ws.onmessage = function(msg){
        var logs = JSON.parse(msg.data);
        vm.logs = logs;
        console.log(logs);
        if(vm.step=='show_list'){
            authorizedKeyHanlder(logs.authorized_key);
        }
        if(vm.step=='run'){
            deployHanlder(logs);
        }
    }
    vm.ws.onclose = function() { alert("连接已关闭..."); };
}

vm = new Vue({
    el: "#app",
    data: {
        fileList: [],
        push_key_not_finish: true,
        success_count: 0,
        fail_count: 0,
        step: 'import',
        cell_id: '',
        cell_config: [],
        activeStep: '1',
        // steps: [],
        stepLog: [],
        templates: [],
        cellForm: {is_API_deploy: false},
        hosts: [],
        locations: [],
        unReadyForDeploy: true,
        ws: null,
        logs: [],
        authorized_log: '',
        logVisible: false
    },

    created: function(){
        this.getTemplateList();
        this.locations = this.getLocations();
    },

    computed:{
        logs: function(){
            return this.stepLog.join('\n');
        }
    },

    methods: {
        getData: function(url, params, func, args){
            obj = this;
            axios({
                method:'GET',
                url: url,
                params: params
            }).then(function(resp){
                func(resp, args);
                //tmp = resp.data['ret'];
                //obj[target] = tmp;
            }).catch(function(resp){
                //console.log(resp);
                console.log('Fail:'+resp.status+','+resp.statusText);
            });
        },

        postData: function(url, data, headers, func){
            obj = this;
            axios({
                method:'POST',
                url: url,
                data: data, 
                headers: headers
            }).then(function(resp){
                func(resp);
            }).catch(resp => {
                console.log('Fail:'+resp.status+','+resp.statusText);
            });
        },

        getTemplateList: function(){
            this.getData('../template/', {data:[]}, this.afterGetTemplateList);
        },

        afterGetTemplateList: function(resp){
            if(resp.data.status==200){
                this.templates = resp.data.data;
            }
            else{
                showMsg(false, '无法获取模板清单');
            }
            
        },

        uploadReq: function(content){
            let data = new FormData();
            data.append('file', content.file);
            data.append('template_id', this.cellForm.templateId);
            data.append('location', this.cellForm.location);
            data.append('is_API_deploy', this.cellForm.is_API_deploy);
            var headers = {'Content-Type':'multipart/form-data'};
            this.postData('../post/', data, headers, this.afterUpload);
        },

        afterUpload: function(resp){
            if(resp.data.status==200){
                this.cell_config = resp.data.data.cell_config;
                this.cell_id = resp.data.data.cell_id;
                for(var i=0;i<this.cell_config.length;i++){
                    this.hosts.push({status: 'init', step:'authorized_key'});
                }
                this.step ='show_list';
                showMsg(true, '创建Cell成功');
                startWS(this.cell_id, this.hosts.length);
            }
            else{
                showMsg(false, '创建Cell失败');
            }
        },

        genCell: function(){
            if(!this.cellForm.is_API_deploy){
                this.$refs.upload.submit();
            }
            else{
                const data_post = new URLSearchParams()
                data_post.append('template_id', this.cellForm.templateId);
                data_post.append('location', this.cellForm.location);
                data_post.append('is_API_deploy', this.cellForm.is_API_deploy);
                var headers = {'Content-Type':'application/x-www-form-urlencoded'};
                this.postData('../post/', data_post, headers, this.afterUpload);
            }
        },

        runCell: function(){
            this.getData('../runCell/', {cell_id:this.cell_id}, this.afterRunCell);
        },

        afterRunCell: function(resp){
            if(resp.status==200){
                this.step = 'run';
                for(var i=0;i<this.cell_config.length;i++){
                    Vue.set(vm.hosts[i], 'status', 'init');
                    Vue.set(vm.hosts[i], 'step', 'check_host_env');
                }
                // startWS(this.cell_id);
            }
            else{
                showMsg(false, 'Error! Cannot create cell');
            }
        },

        refresh_steps: function(steps){
            for(var i=0;i<steps.length;i++){
                step = steps[i];
                if(step.status<2){
                    this.activeStep = (i+1).toString();
                    break;
                }
            }
        },

        getLocations: function(){

            var level1s = ['nh', 'ks', 'jd']
            var level2s = ['uat', 'pilot', 'online']
            var level1_list = []
            var level2_list = []
            for(var i=0;i<level2s.length;i++ ){
                level2_list.push({label: level2s[i], value: level2s[i]});
            }

            for(var i=0;i<level1s.length;i++ ){
                var children = level2_list;
                level1_list.push({label: level1s[i], value: level1s[i], children: children});
            }
            return level1_list;
        },

        startWS: function(){
            startWS(this.cell_id);
        },

        stopWS: function(){
            this.ws.close();
        },

        getLog: function(step, ip){
            this.logVisible = true;
            var step_logs = this.logs[step];
            for(var i=0;i<step_logs.length;i++){
                if(step_logs[i].IP==ip){
                    this.authorized_log = step_logs[i].Msg;
                    return;
                }
            }
            this.authorized_log = 'not found';
        }
    }
});