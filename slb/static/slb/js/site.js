Vue.component('my_access_log',{
    template: '<el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input>',
    props: ['cmdarg', 'row', 'cmd'],
    methods: {
        argUpdated: function(w, r){
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    },
    computed: {
        cmdcmdarg: {
            get: function(){return this.cmdarg;},
            set: function(v){}
        },
    },
});

Vue.component('my_proxy_pass',{
    template: '<div>pool_name: <el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input></div>',
    props: ['cmdarg', 'row', 'cmd'],
    computed:{
        cmdcmdarg: {
            get: function(){ return this.cmdarg; },
            set: function(v){}
        }
    },
    methods: {
        argUpdated: function(w, r){
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    }
});

Vue.component('my_more_clear_headers',{
    template: '<el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input>',
    props: ['cmdarg', 'row', 'cmd'],
    methods: {
        argUpdated: function(w, r){
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    },
    computed: {
        cmdcmdarg: {
            get: function(){return this.cmdarg;},
            set: function(v){}
        },
    },
});

Vue.component('my_more_set_headers',{
    template: '<el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input>',
    props: ['cmdarg', 'row', 'cmd'],
    methods: {
        argUpdated: function(w, r){
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    },
    computed: {
        cmdcmdarg: {
            get: function(){return this.cmdarg;},
            set: function(v){}
        },
    },
});

Vue.component('my_ifelse',{
    template: '<el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input>',
    props: ['cmdarg', 'row', 'cmd'],
    methods: {
        argUpdated: function(w, r){
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    },
    computed: {
        cmdcmdarg: {
            get: function(){return this.cmdarg;},
            set: function(v){}
        },
    },
});

Vue.component('my_return',{
    template: '<el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input>',
    props: ['cmdarg', 'row', 'cmd'],
    methods: {
        argUpdated: function(w, r){
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    },
    computed: {
        cmdcmdarg: {
            get: function(){return this.cmdarg;},
            set: function(v){}
        },
    },
});

Vue.component('my_rewrite',{
    template: '<el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input>',
    props: ['cmdarg', 'row', 'cmd'],
    methods: {
        argUpdated: function(w, r){
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    },
    computed: {
        cmdcmdarg: {
            get: function(){return this.cmdarg;},
            set: function(v){}
        },
    },
});

Vue.component('my_static_resource',{
    template: '<el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input>',
    props: ['cmdarg', 'row', 'cmd'],
    methods: {
        argUpdated: function(w, r){
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    },
    computed: {
        cmdcmdarg: {
            get: function(){return this.cmdarg;},
            set: function(v){}
        },
    },
});

var ztree = Vue.component('ztree', {
    data: function(){
        return {
            setting:{
              check: {  
                    enable: true,  
                    nocheckInherit: false ,
                    chkboxType: { "Y": "p", "N": "p" },
                    chkStyle: "radio"
                },  
                data: {  
                    simpleData: {  
                        enable: true  
                    }  
                },
                callback: {
                    beforeClick: this.beforeClick,
                    onClick: this.zTreeOnClick,
                    onCheck: this.zTreeOnCheck,
                },
                view: {
                    selectedMulti: false,
                },
            },
            zNodes: [],
        }
    },
    template: '<div id="areaTree"> <div class="box-title"> <a href="#">列表<i class="fa  fa-refresh" @click="freshArea">点击</i></a> </div> <div class="tree-box"> <div class="zTreeDemoBackground left"> <ul id="treeDemo" class="ztree"></ul> </div> </div> </div>',
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

        initTree: function(){
            this.getData('../rest/nginxclustertree/', {}, this.afterInitTree);
        },

        afterInitTree: function(resp){
            if(resp.data.status==200){
                var tmp = JSON.parse(resp.data.data);
                for(i=0; i<tmp.length;i++){
                    item = tmp[i];
                    item['nocheck'] = true;
                    if(item.node_name1 && item.node_name2 && item.node_name3 && item.node_name4 && item.node_name5 && item.node_name6=='nginx'){
                        item['nocheck'] = false;
                    }
                }
                this.zNodes = tmp; 

                console.log(this.zNodes);
            }
        },

        freshArea: function(){
            $.fn.zTree.init($("#treeDemo"), this.setting, this.zNodes);
        },
        zTreeOnClick: function(event, treeId, treeNode) {
            //console.log(treeNode.tId + ", " + treeNode.name);
        },
        zTreeOnCheck: function(event, treeId, treeNode) {
            if (treeNode.checked){
                vm.siteDetail['nginx_cluster_id'] = treeNode.id;
                var tmp = treeNode.node_name1 +'_'+ treeNode.node_name2 +'_'+ treeNode.node_name3 +'_'+ treeNode.node_name4 +'_'+ treeNode.node_name5 +'_'+ treeNode.node_name6;
                vm.siteDetail['nginx_cluster_name'] = tmp;
                vm.clusterTreeDialogTriggle = false;
            }
            else{
                vm.nginx_cluster_name = '';
                vm.nginx_cluster_id = -1;
            }
        },
        //beforeClick: function(treeId, treeNode) {
          //var zTree = $.fn.zTree.getZTreeObj("treeDemo");
          //// zTree.checkNode(treeNode, !treeNode.checked, null, true);
          //zTree.checkNode(treeNode, !treeNode.checked, true, true); //第二个参数!treeNode.checked和"",省略此参数效果等同，则根据对此节点的勾选状态进行 toggle 切换，第三个参数设置为true时候进行父子节点的勾选联动操作 ，第四个参数true 表示执行此方法时触发 beforeCheck & onCheck 事件回调函数；false 表示执行此方法时不触发事件回调函数
          //return false;
        //}
      },
      created: function(){
          this.initTree();
      },
      mounted(){
          $.fn.zTree.init($("#treeDemo"), this.setting, this.zNodes).expandAll(true);
          this.freshArea();
      }
});

function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

var defaultSiteDetail = {
    //basicConfig
    id: -1,
    site_name: "",
    state_control: "enable",
    domain_name: "",
    port: 80,
    //defaultPool: "",
    //nginx_cluster_name: "",
    //nginx_cluster_id: "",
    //group: "default-grp",
    is_https: false,
    siteMPRuleList: [
    ],
};

var defaultMPRule = {
    id: "-1", 
    regular_expression:"",
    matching_type: "",
    caseSensitive: "",
    https_type: "",
    cmdList: [{command_type: "access_log", command_param: "access_log"}]
};

var defaultCmdList = [{command_type: "access_log", command_param: ""}];

var testMPRule = [
    {id: "1", regular_expression:"/root", matching_type: "prefix", case_sensitive: true, https_type: "all", cmdList: [{command_type: "proxy_pass", command_param: "test_proxy_pass"}, {command_type: "access_log", command_param: "test_access_log"}]},
    {id: "2", regular_expression:"/root/a", matching_type: "common", case_sensitive: true, https_type: "http", cmdList: [{command_type: "access_log", command_param: "access_log"}]},
    {id: "3", regular_expression:"/root/b", matching_type: "regex", case_sensitive: false, https_type: "all", cmdList: [{command_type: "more_clear_headers", command_param: "clear_headers"}]},
    {id: "4", regular_expression:"/root/c", matching_type: "excat", case_sensitive: true, https_type: "https", cmdList: [{command_type: "more_set_headers", command_param: "set_header"}]}
];

editor = CodeMirror.fromTextArea(document.getElementById("previewTextArea"), {
    mode: 'nginx',
    lineNumbers: true,
    readOnly: false,
    lineSeparator: "\r\n"
});

vm = new Vue({
    el: "#app",
    data: {
        navIndex: "1",
        activeIndex: "1",
        sites: [],
        urls: [],
        tabIndex: "2",
        siteNameDialogTriggle: false,
        siteDetailActiveTabName: "basicConfig",
        siteDetail: JSON.parse(JSON.stringify(defaultSiteDetail)),
        siteMPRuleList: [],
        siteVersions: [],
        selectedVersion: '',
        addMappingRuleDialogTriggle: false,
        //newMappingRuleForm:{id: -1, path: '', matchType: '', caseSensitive:'Y', httpType: ['http', 'https'], cmdList: [{cmdType: 'proxy_pass', cmdArg: 'abc'}] },
        mappingRule: {id: "1", regular_expression: '', matching_type: '', caseSensitive:'Y', https_type: ['all'], cmdList: [{command_type: 'proxy_pass', command_parm: 'abc'}] },
        cmdList: [],
        pools: [],
        clusterTreeDialogTriggle: false,
        previewDialogTriggle: false,
        previewContent: '',
        editor: '',
        mydefine: "my_access_log"
    },
    created: function(){
        //this.getSites();
        window_url = window.location.href;
        site_id = parseInt(window_url.split("=")[1]);
        if(site_id){
            //console.log(site_id);
            this.getSiteDetail(site_id);
        }
        else{
            this.siteNameDialogTriggle = true;
        }
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
                //tmp = resp.data['ret'];
                //obj[target] = tmp;
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
                data: data
            }).then(function(resp){
                func(resp);
            }).catch(resp => {
                console.log('Fail:'+resp.status+','+resp.statusText);
            });
        },

        getSites: function(){
            //this.sites =  [
                //{id: "1", site_name: "site-1"},
                //{id: "2", site_name: "site-2"},
                //{id: "3", site_name: "site-3"},
                //{id: "4", site_name: "site-4"}
            //];
            this.getData('../rest/getmngsitelist/', {}, this.afterGetSites);
        },

        afterGetSites: function(resp){
            tmp = resp.data['ret'];
            this.sites = tmp;
            if(this.sites.length>0){
                this.getSiteDetail(this.sites[0].id);
            }
            //this.getPools();
            //this.getNginxClusters();
        },

        getSiteDetail: function(id){
            //siteDetails = [ 
                //{
                    ////basicConfig
                    //id: "1",
                    //site_name: "site-1",
                    //state_control: "enable",
                    //domain_name: "kfc.com",
                    //port: 80,
                    //defaultPool: "Pool-1",
                    //nginx_cluster_id: "1",
                    //nginx_cluster_name: "Nginx-1",
                    //current_version: "0",
                    //group: "default-grp",
                    //is_https: true,
                    //siteMPRuleList: testMPRule 
                //},
                //{
                    ////basicConfig
                    //id: "2",
                    //site_name: "site-2",
                    //state_control: "enable",
                    //domain_name: "taco.com",
                    //port: 80,
                    //defaultPool: "Pool-2",
                    //nginx_cluster_id: "1",
                    //nginx_cluster_name: "Nginx-2",
                    //current_version: "0",
                    //group: "default-grp",
                    //is_https: false,
                //},
                //{
                    ////basicConfig
                    //id: "3",
                    //site_name: "site-3",
                    //state_control: "force_offline",
                    //domain_name: "daojia.com",
                    //port: 80,
                    //defaultPool: "Pool-3",
                    //nginx_cluster_id: "1",
                    //nginx_cluster_name: "Nginx-3",
                    //current_version: "0",
                    //group: "default-grp",
                    //is_https: false,
                //},
                //{
                    ////basicConfig
                    //id: "4",
                    //site_name: "site-4",
                    //state_control: "disable",
                    //domain_name: "pizza.com",
                    //port: 80,
                    //defaultPool: "Pool-4",
                    //nginx_cluster_id: "1",
                    //nginx_cluster_name: "Nginx-4",
                    //current_version: "0",
                    //group: "default-grp",
                    //is_https: false,
                //},
            //]
            ////console.log(id);
            //console.log(siteDetails[id-1]);
            //this.siteDetail = siteDetails[id-1];
            this.getData('../rest/getmngsiteinfo/', {'id': id}, this.afterGetSiteDetail);
        },

        afterGetSiteDetail: function(resp){
            tmp = resp.data['ret'];
            //console.log(tmp);
            this.siteDetail = tmp;
            this.getMPRuleList(this.siteDetail.id);
            this.getSiteVersion(this.siteDetail.id);
        },

        getSiteVersion: function(id){
            this.getData('../rest/deployversionbysiteid', {id:id}, this.afterGetSiteVersion);
        },

        afterGetSiteVersion: function(resp){
            tmp = resp.data['ret'];
            //console.log(tmp);
            this.siteVersions = tmp;
            this.selectedVersion = tmp[0].k;
        },

        getMPRuleList: function(nginx_site_id){
            //test_mpRules = [
            //];
            //this.siteMPRuleList = test_mpRules[nginx_site_id-1]
            this.getData('../rest/getmappingruleslist', {'nginx_site_id': nginx_site_id}, this.afterGetMPRule);
        },

        afterGetMPRule: function(resp){
            tmp = resp.data['ret']
            //console.log(tmp);
            this.siteMPRuleList = tmp;
        },

        getCmdList: function(rule_id){
            this.getData('../rest/getcmdlist', {'id': rule_id}, this.afterGetCmdList);
        },

        afterGetCmdList: function(resp){
            tmp = resp.data['ret'];
            //console.log(tmp);
            this.cmdList = tmp.cmd_list;
            this.siteMPRuleList['cmdList'] = tmp.cmd_list;
        },

        insert_cmdList: function(index, cmd_list){
            //console.log(this.siteMPRuleList[0].id);
            //console.log(index);
            for(i=0; i<this.siteMPRuleList.length; i++){
                if(this.siteMPRuleList[i].id == index){
                    //console.log('get')
                    this.siteMPRuleList[i].cmdList= cmd_list;
                    break;
                }
            }
        },

        getConfig: function(){
            return "upstream alex.web.kfc.com.cn {\r\n server 1.1.1.1:80 max_fails=3 weight=1 fail_timeout=4;  \n server 2.2.2.2:80 max_fails=3 weight=1 fail_timeout=3;  \n keepalive 40;\n keepalive_timeout 60s;\n check interval=3000 fall=3 rise=2 timeout=3000 default_down=false type=tcp;\n }";
            //this.getData('../rest/', {'id': id}, this.afterGetConfig);
        },

        afterGetConfig: function(resp){
            tmp = resp.data['ret'];
            //console.log(tmp);
            this.siteDetail = tmp;
        },

        getPools: function(){
            tmp = [
                {id: 1, name:"Pool-1"},
                {id: 2, name:"Pool-2"},
                {id: 3, name:"Pool-3"},
                {id: 4, name:"Pool-4"}
            ];
            this.pools = tmp;
            //this.getData('../rest/', {'id': id}, this.afterGetPools);
        },

        afterGetPools: function(resp){
            tmp = resp.data['ret'];
            //console.log(tmp);
            this.siteDetail = tmp;
        },

        getNginxClusters: function(){
            tmp = [
                {id: 1, name:"Nginx-1"},
                {id: 2, name:"Nginx-2"},
                {id: 3, name:"Nginx-3"},
                {id: 4, name:"Nginx-4"}
            ];
            this.nginxClusters = tmp;
            //this.getData('../rest/', {'id': id}, this.afterGetNginxClusters);
        },

        afterGetNginxClusters: function(resp){
            tmp = resp.data['ret'];
            //console.log(tmp);
            this.siteDetail = tmp;
        },

        onchange_nginx_cluster: function(val){
            //for(i=0; i<this.nginxClusters.length; i++){
                //if(this.nginxClusters[i].name==val){
                    //this.siteDetail['nginx_id'] == this
                //}
            //}
            this.siteDetail['nginx_cluster_id'] = '100';
        },
        
        handleNavSelect: function(key, keyPath){
        },

        handleSiteSelect: function(key, keyPath){
            //console.log(key);
            this.activeIndex = key;
            this.getSiteDetail(key);
            this.siteDetailActiveTabName = "basicConfig";
        },

        handleTabChange: function(tab){
            //console.log(tab);
            //this.tabName = "basicConfig";
        },

        addSite: function(){
            this.siteDetail = JSON.parse(JSON.stringify(defaultSiteDetail));
            this.siteDetailActiveTabName = "basicConfig";
            this.siteNameDialogTriggle = true;
        },

        saveSiteName: function(){
            this.siteNameDialogTriggle = false;
        },

        editSiteDetail: function(){
            this.siteDetailDivStatus = 'wr';
        },

        siteDetailFormSave: function(operation){
            this.postData('../rest/mngsitecreateorupdate/', this.siteDetail, this.afterPostSiteDetail);
        },

        afterPostSiteDetail: function(resp){
            tmp = resp.data;
            if(tmp.status==200){
                showMsg(true, tmp.msg);
                this.siteDetail.id=tmp.id;
            }
            else{ showMsg(false, tmp.msg);}
        },

        jumpUp: function(row) {
            //console.log(row.id);
            if(row.id==1){return;}
            id = row.id-1;
            previousId = id-1;
            tmpCurrent = this.siteMPRuleList[id];
            tmpCurrent.id = previousId+1;
            tmpPrevious = this.siteMPRuleList[previousId];
            tmpPrevious.id = id+1;
            this.siteMPRuleList.splice(previousId, 2, tmpCurrent, tmpPrevious);
        },

        jumpDown: function(row) {
            //console.log(row.id);
            if(row.id==this.siteMPRuleList.length){return;}
            id = row.id-1; //align wiht array
            laterId = id+1;
            tmpCurrent = this.siteMPRuleList[id];
            tmpCurrent.id = laterId+1;
            tmpLater = this.siteMPRuleList[laterId];
            tmpLater.id = id+1;
            this.siteMPRuleList.splice(id, 2, tmpLater, tmpCurrent);
        },

        jumpDoubleUp: function(row){
            id = row.id-1;
            tmp = this.siteMPRuleList[id];
            tmp.id=1;
            for(i=0; i<id; i++){
                this.siteMPRuleList[i].id = this.siteMPRuleList[i].id+1;
            }
            this.siteMPRuleList.splice(id, 1);
            this.siteMPRuleList.unshift(tmp);
        },

        jumpDoubleDown: function(row){
            id = row.id-1;
            tmp = this.siteMPRuleList[id];
            tmp.id = this.siteMPRuleList.length;
            for(i=id+1; i<tmp.id; i++){
                this.siteMPRuleList[i].id = this.siteMPRuleList[i].id-1;
            }
            this.siteMPRuleList.splice(id, 1);
            this.siteMPRuleList.push(tmp);
        },

        handleCmdargChange: function(val){
            //val is dict: {input-content, scope} 
            this.mappingRule.cmdList[val.s.$index].command_param = val.v;
        },

        addMappingRule: function(){
            this.addMappingRuleDialogTriggle = true;
            this.mappingRule = JSON.parse(JSON.stringify(defaultMPRule));
            //this.cmdList = JSON.parse(JSON.stringify(defaultCmdList));
        },
        
        editMappingRule: function(row){
            console.log(row);
            this.getCmdList(row.id);
            //this.mappingRule = this.siteMPRuleList[row.id];
            this.mappingRule = this.siteMPRuleList[0];
            this.addMappingRuleDialogTriggle = true;
        },

        saveMappingRule: function(){
            //this.mappingRule = this.cmdList;
        },

        delMappingRule: function(row){
            //console.log(row);
        },

        //infoMappingRule: function(row){
            //this.infoMappingRuleDialogTriggle = true;
            //this.infoMappingRuleForm.matchType = 'prefix';
        //},
        addCmd: function(){
            this.mappingRule.cmdList.push(JSON.parse(JSON.stringify(defaultCmdList)));
        },

        delCmd: function(row){
            //console.log(row);
            for(i=0; i<this.siteMPRuleList.length; i++){
                if(this.siteMPRuleList[i].id==row.mapping_rules_id){
                    for(j=0; j<this.siteMPRuleList[i].cmdList.length; j++){
                        if(this.siteMPRuleList[i].cmdList[j].id==row.id){
                            this.siteMPRuleList[i].cmdList.splice(j, 1);
                        }
                    }
                }
            }
            //this.newMappingRuleForm.cmdList.splice();
        },

        cmdTypeChange: function(cmdType){
            //console.log(a);
            if(cmdType=='access_log'){
                this.mydefine = 'my_access_log'; }
            else if(cmdType=='proxy_pass'){
                this.mydefine = 'my_proxy_pass'; }
            else if(cmdType=='more_clear_headers'){
                this.mydefine = 'my_more_clear_headers'; }
            else if(cmdType=='more_set_headers'){
                this.mydefine = 'my_more_set_headers'; }
            else if(cmdType=='static-resource'){
                this.mydefine = 'my_static_resource'; }
            else if(cmdType=='rewrite'){
                this.mydefine = 'my_rewrite'; }
            else if(cmdType=='return'){
                this.mydefine = 'my_return'; }
            else if(cmdType=='ifelse'){
                this.mydefine = 'my_ifelse'; }
        },

        previewConfigFile: function(){
            this.previewDialogTriggle = true;
            //this.siteDetail['cmd_list'] = this.cmdList;
            //console.log(siteDetail);
            //this.postData('../rest/configfile', {'siteConfig':siteDetail}, afterPreviewConfigFile);
            this.previewContent = this.getConfig();
            //this.editor = CodeMirror.fromTextArea(document.getElementById("previewTextArea"), {});
            this.editor = editor;
        },

        createDist: function(){
            //console.log(this.siteDetail);
            id = this.siteDetail.id;
            this.getData('../rest/deployversioncreateview', {id:id}, this.afterCreateDist);
        },

        afterCreateDist: function(resp){
            tmp = resp.data['ret'];
            if(tmp.status==200){ showMsg(true, tmp.msg);}
            else{ showMsg(false, tmp.msg);}
        },

        selectCluster: function(){
            this.clusterTreeDialogTriggle = true;
        },

        handleCloseSiteName: function(){
            if(this.siteDetail.site_name.length==0){
                showMsg(false, '请输入站点名称');
                this.siteNameDialogTriggle = true;
            }
        },

        deploy_url: function(i){
            url = "/slb/deploy/deploy_task?site_name="+this.siteDetail.site_name+"&nginx_cluster_id="+this.siteDetail.nginx_cluster_id+"&version="+this.siteVersions[i].version+"&task_id="+this.siteVersions[i].task_id;
            return url;
        },

        rollback: function(){
            if(this.siteVersions.length<=1){
                showMsg(false, '无历史版本，无法执行回滚');
            }
            else{
                //goto deploy page
                //console.log(this.deploy_url(1));
                window.location= this.deploy_url(1);
            }
        },

        deploy: function(){
            if(this.siteVersions.length==0){
                showMsg(false, '请先创建版本后再发布');
            }
            else{
                //goto deploy page
                //console.log(this.deploy_url(0));
                window.location=this.deploy_url(0);
            }
        },

    }
});

