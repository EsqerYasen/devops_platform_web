function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

vm = new Vue({
    el: "#app",
    data: {
        templates: [],
        templateFormVisible: false,
        serviceDialogVisible: false,
        connDialogVisible: false,
        historyVisible: false,
        services: [],
        t_logs: [],
        servicesForm: [],
        templateForm: {},
        serviceData: {
            serviceName: '',
            version: '',
            port: '',
            serviceType: '',
            serverSpec: '',
            count: 1,
            cpu: 0,
            mem: 0,
            disk: 50,
            connections: [],
        },
        filter_content: '',
        currentPage: 1,
        pageSize: 2,
        action: '',
        components: [
            {
                name: "MongoDB",
                version: "4.0.4",
                port: "27017",
                type: "middleware"
            },
            {
                name: "Redis",
                version: "5.0",
                port: "6379",
                type: "middleware"
            },
            {
                name: "RabbitMQ",
                version: "3.7.8",
                port: "15672",
                type: "middleware"
            },
            {
                name: "MySQL",
                version: "5.7",
                port: "3306",
                type: "middleware"
            },
        ],
        isSelfDefineServer: false,
        isEditTemplate: false,
        serverSpecs: [
            {
                name: "自定义"
            },
            {
                name: "S3.SMALL1",
                info: {
                    cpu: 1,
                    mem: 1
                },
            },
            {
                name: "S3.SMALL2",
                info: {
                    cpu: 1,
                    mem: 2
                },
            },
            {
                name: "S3.SMALL4",
                info: {
                    cpu: 1,
                    mem: 4
                },
            },
            {
                name: "S3.MEDIUM4",
                info: {
                    cpu: 2,
                    mem: 4
                },
            },
            {
                name: "S3.MEDIUM8",
                info: {
                    cpu: 2,
                    mem: 8
                },
            },
            {
                name: "S3.LARGE8",
                info: {
                    cpu: 4,
                    mem: 8
                },
            },
            {
                name: "S3.LARGE16",
                info: {
                    cpu: 4,
                    mem: 16
                },
            }
        ],
        templateFormDisEditable: false,
        templateNameDisEditable: false,
        serviceDisEditable: false,
        service_index: -1,
        business: []
    },
    created: function(){
        this.getTemplateList();
        this.business = this.getBusiness();
    },
    computed: {
        template: function(){
            var ret_template = {};
            for(var i=0; i<this.servicesForm.length; i++){
                var serviceName = this.servicesForm[i].serviceName;
                var tmp = JSON.parse(JSON.stringify(this.servicesForm[i]));
                delete tmp.disabled;
                tmp.count = parseInt(tmp.count);
                tmp.cpu = parseInt(tmp.cpu);
                tmp.mem = parseInt(tmp.mem);
                tmp.disk = parseInt(tmp.disk);
                keyName = serviceName + '_' + i;
                // keyName = serviceName + i; //node_name split by '_'
                ret_template[keyName] = tmp;
            }
            // ret_template['business'] = this.templateForm.business.join('_');
            // ret_template['name'] = this.templateForm.name;
            ret_template['name'] = this.templateForm.name.join('_');
            return ret_template;
        },
        template_count: function(){
            // if(this.filter_content.length==0){
            //     return this.templates.length;
            // }
            // else{
                return this.display_templates.length;
            // }
        },
        display_templates: function(){
            var ret1 = new Array();
            for(i=0;i<this.templates.length;i++){
                // if(this.templates[i].name.indexOf(this.filter_content)>=0 || this.templates[i].business.indexOf(this.filter_content)>=0 ){
                if(this.templates[i].name.indexOf(this.filter_content)>=0){
                    ret1.push(this.templates[i]);
                }
            }
            return ret1;
            // var start = (this.currentPage - 1)*this.pageSize;
            // var end = start + this.pageSize;
            // var ret = ret1.slice(start, end);
            // return ret;
        }
        
    },
    filters: {
        pagination: function(templates, currentPage, pageSize){
            var ret = new Array();
            var start = (currentPage - 1)*pageSize;
            var end = start + pageSize;
            ret = templates.slice(start, end);
            return ret;
        },
        search: function(templates, filterContent){
            var ret = new Array();
            for(i=0;i<templates.length;i++){
                // if(templates[i].name.indexOf(filterContent)>=0 || templates[i].business.indexOf(filterContent)>=0 ){
                if(templates[i].name.indexOf(filterContent)>=0){
                    ret.push(templates[i]);
                }
            }
            return ret;
        }
    },
    methods: {
        getData: function(url, params, func, args){
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

        initServiceData: function(){
            this.serviceData = {
                serviceName: '',
                version: '',
                port: '',
                serviceType: '',
                serverSpec: '',
                count: 1,
                cpu: 0,
                mem: 0,
                disk: 50,
                connections: [],
                action: ''
            }
        },

        initTemplateForm: function(){
            this.servicesForm = [];
            this.services = [];
            this.templateForm = {};
            this.initServiceData();
        },

        getTemplateList: function(){
            this.getData('../', {}, this.afterGetTemplateList);
        },

        afterGetTemplateList: function(resp){
            if(resp.data.status==200){
                this.templates = resp.data.data;
            }
            else{
                showMsg(false, '获取模板清单失败');
            }
            
        },

        delTemplate: function(template_id){
            this.$confirm('此操作将永久删除该模板, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true
            }).then(() => {
                const data_post = new URLSearchParams();
                data_post.append('action', 'delete');
                data_post.append('template_id', template_id);
                headers = {'Content-Type':'application/x-www-form-urlencoded'};
                this.postData('../', data_post, headers, this.afterDelTemplate);
            }).catch(() => {
                this.$message({type: 'info',message: '已取消删除'});
            });
        },

        afterDelTemplate: function(resp){
            if(resp.data.status=200){
                showMsg(true, '删除模板成功');
                this.getTemplateList();
            }
            else{
                showMsg(false, '删除模板失败');
            }
        },

        createTemplate: function(){
            this.initTemplateForm();
            this.templateFormVisible = true;
            this.templateFormDisEditable = false;
            this.templateNameDisEditable = false;
            this.isEditTemplate = true;
            this.action = 'create';
        },

        postTemplate: function(){
            const data_post = new URLSearchParams();
            data_post.append('action', this.action);
            data_post.append('template', JSON.stringify(this.template));
            data_post.append('template_id', this.templateForm.id);
            headers = {'Content-Type':'application/x-www-form-urlencoded'};
            this.postData('../', data_post, headers, this.afterPostTemplate);
        },

        afterPostTemplate: function(resp){
            this.$confirm('確定要更新该模板吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true
            }).then(() => {
                if(this.action=='create'){
                    msg = '创建';
                }
                else if(this.action=='update'){
                    msg = '更新';
                }
                if(resp.data.status==200){
                    showMsg(true, msg+'模板成功');
                    this.getTemplateList();
                    this.templateFormVisible = false;
                    this.initTemplateForm();
                }
                else{
                    showMsg(false, msg+'模板失败');
                }
            }).catch(() => {});
        },

        cancelPostTemplate: function(){
            this.$confirm('確定要放弃对该模板的操作吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true
            }).then(() => {
                this.templateFormVisible = false;
                this.initTemplateForm();
            }).catch(() => {});
        },

        getTemplate: function(template_id){
            data = {template_id:template_id};
            this.isEditTemplate = false;
            this.getData('../', data, this.afterGetTemplate);
        },

        afterGetTemplate: function(resp){
            if(resp.data.status==200){
                var tmp_data = resp.data.data;
                // this.templateForm.name = tmp_data.name;
                // this.templateForm.business = tmp_data.business.split('_');
                this.templateForm.name = tmp_data.name.split('_');
                this.action = '';
                this.services = tmp_data.services;
                this.servicesForm = JSON.parse(JSON.stringify(this.services));
                this.templateFormVisible = true;
                this.templateFormDisEditable = true;
            }
            else{
                showMsg(false, '获取模板失败');
            }
        },

        modifyTemplate: function(template_id){
            data = {template_id:template_id};
            this.isEditTemplate = true;
            this.getData('../', data, this.afterModifyTemplate);
            this.action = 'update';
        },

        afterModifyTemplate: function(resp){
            if(resp.data.status==200){
                var tmp_data = resp.data.data;
                this.templateForm.id = tmp_data.id;
                // this.templateForm.name = tmp_data.name;
                // this.templateForm.business = tmp_data.business.split('_');
                this.templateForm.name = tmp_data.name.split('_');
                this.services = tmp_data.services;
                this.servicesForm = JSON.parse(JSON.stringify(this.services));
                this.templateFormVisible = true;
                this.templateFormDisEditable = false;
                this.templateNameDisEditable = true;
            }
            else{
                showMsg(false, '修改模板失败');
            }
        },

        getService: function(service){
            this.serviceData = service;
            this.serviceDisEditable = true;
            this.serviceDialogVisible = true;
        },

        delService: function(service_index){
            this.$confirm('確定要刪除该组件吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true
            }).then(() => {
                this.servicesForm.splice(service_index,1);
                for(var i=0; i<this.servicesForm.length;i++){
                    var new_connections = Array()
                    for(var j=0; j<this.servicesForm[i].connections.length;j++){
                        var obj = this.servicesForm[i].connections[j];
                        var obj_list = obj.split("_");
                        var last_index = obj_list.length-1;
                        var index = obj.split("_")[last_index];
                        if(service_index > index){
                            new_connections.push(obj);
                        }
                        else if(service_index < index){
                            new_connections.push(obj_list[0]+"_"+(index-1));
                        }
                        // else{ // service_index == index
                        //     do nothing
                        // }
                    }
                    this.servicesForm[i].connections = new_connections;
                }
            }).catch(() => {});
        },

        // modifyService: function(service, service_index){
        //     this.serviceData = service;
        //     this.serviceDisEditable = false;
        //     this.serviceDialogVisible = true;
        //     this.service_index = service_index;
        // },

        resetService: function(row, index){
            if(index>=this.services.length){
                return;
            }
            this.$confirm('確定要重置该组件吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true
            }).then(() => {
                Vue.set(this.servicesForm, index, JSON.parse(JSON.stringify(this.services[index])));
            }).catch(() => {});
        },

        addService: function(){
            var tmpServiceData = JSON.parse(JSON.stringify(this.serviceData));
            // if(this.service_index>0){
            //     this.servicesForm.splice(this.service_index, 1, tmpServiceData);
            //     this.service_index = -1;
            // }
            // else{
                this.servicesForm.push(tmpServiceData);
            // }
            this.initServiceData();
            this.serviceDialogVisible = false;
        },

        addANewService: function(){
            var tmpServiceData = JSON.parse(JSON.stringify(this.serviceData));
            this.servicesForm.push(tmpServiceData);
        },

        clearConnections: function(){
            this.serviceData.connections = [];
        },

        getBusiness: function(){
            var level1s = ['kfc', 'ph', 'dfjb', 'xfy', 'taco']
            var level2s = ['preorder', 'delivery', 'sso', 'pay']
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
        
        handleChangeOnServiceName: function(value){
            for(var i=0;i<this.components.length;i++){
                var component = this.components[i];
                if (component.name==value){
                    this.serviceData.port = component.port;
                    this.serviceData.serviceType = component.type;
                    this.serviceData.version = component.version;
                    break;
                }
            }
        },

        handleChangeServiceNameInTable: function(val, row){
            for(var i=0;i<this.components.length;i++){
                var component = this.components[i];
                if (component.name==val){
                    row.port = component.port;
                    row.serviceType = component.type;
                    row.version = component.version;
                    break;
                }
            }
        },

        handleInstanceTypeInTable: function(val, row){
            if(val=='自定义'){
                return
            }
            for(var i=0;i<this.serverSpecs.length;i++){
                var serverSpec = this.serverSpecs[i];
                if (serverSpec.name==val){
                    row.cpu = serverSpec.info.cpu;
                    row.mem = serverSpec.info.mem;
                    break;
                }
            }
        },

        handleInstanceType: function(value){
            if(value=='自定义'){
                return
            }
            for(var i=0;i<this.serverSpecs.length;i++){
                var serverSpec = this.serverSpecs[i];
                if (serverSpec.name==value){
                    this.serviceData.cpu = serverSpec.info.cpu;
                    this.serviceData.mem = serverSpec.info.mem;
                    break;
                }
            }
        },

        handlePageChange: function(pageNum){
            this.currentPage = pageNum;
        },
         
        handlePageSizeChange: function(pageSize){
            this.pageSize = pageSize;
            console.log(pageSize);
        },

        indexMethod: function(index){
            return index+1;
        },

        setConnection: function(){

        },

        select_focus: function(index){
            for(var i=0;i<this.servicesForm.length;i++){
                delete this.servicesForm[i].disabled;
            }
            Vue.set(this.servicesForm[index], 'disabled', true);
        },

        getTemplateLog: function(template_id){
            data = {template_id:template_id};
            
            this.getData('../log/', data, this.afterGetTemplateLog);
        },

        afterGetTemplateLog: function(resp){
            if(resp.data.status==200){
                var tmp_data = resp.data.data;
                this.t_logs = tmp_data;
                this.historyVisible = true;
            }
            else{
                showMsg(false, '获取历史失败');
            }
        },
    }
});