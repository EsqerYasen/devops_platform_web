Vue.component('my_access_log',{
    props: ['cmdarg'],
    template: '<el-input v-model="cmdarg"></el-input>'
});

Vue.component('my_proxy_pass',{
    props: ['cmdarg'],
    computed:{
        innerarg: {
            get: function(){
                return this.cmdarg;
            },
            set: function(newvalue){
                this.cmdarg = newvalue;
            }
        }
    },
    template: '<div>pool_name: </div>'
});

Vue.component('my_more_clear_headers',{
    props: ['cmdarg'],
    template: '<el-input v-model="cmdarg"></el-input>'
});

Vue.component('my_more_set_headers',{
    props: ['cmdarg'],
    template: '<el-input v-model="cmdarg"></el-input>'
});

Vue.component('my_ifelse',{
    props: ['cmdarg'],
    template: '<div>if-condition:<el-input ></el-input></br>if-statement: <el-input></el-input></div>'
});

Vue.component('my_return',{
    props: ['cmdarg'],
    template: '<div>response-code: <el-input ></el-input></br>response-content: <el-input></el-input></div>'
});

Vue.component('my_rewrite',{
    props: ['cmdarg'],
    template: '<div>flag: <el-input ></el-input></br>matches: <el-input></el-input></br>target-pattern: <el-input></el-input></div>'
});

Vue.component('my_static_resource',{
    props: ['cmdarg'],
    template: '<div>expires: <el-input ></el-input></br>root-doc: <el-input></el-input></div>'
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
              //[
              //{ id:1,pid:0,name:"大良造菜单",open:true,nocheck:false,
                //children: [
                    //{ id:11,pid:1,name:"当前项目"},
                    //{ id:12,pid:1,name:"工程管理",open:true,
                        //children: [
                            //{ id:121,pid:12,name:"我的工程"},
                            //{ id:122,pid:12,name:"施工调度"},
                            //{ id:1211,pid:12,name:"材料竞价"}
                        //]
                    //},
                    //{ id:13,pid:1,name:"录入管理",open:true,
                        //children: [
                            //{ id:131,pid:13,name:"用工录入"},
                            //{ id:132,pid:13,name:"商家录入"},
                            //{ id:1314,pid:13,name:"机构列表"}
                        //]
                    //},
                    //{ id:14,pid:1,name:"审核管理",open:true,
                        //children: [
                            //{ id:141,pid:14,name:"用工审核"},
                            //{ id:142,pid:14,name:"商家审核"},
                            //{ id:145,pid:14,name:"机构审核"}
                        //]
                    //},
                    //{ id:15,pid:1,name:"公司管理",open:true,
                        //children: [
                            //{ id:1517,pid:15,name:"我的工程案例"},
                            //{ id:1518,pid:15,name:"联系人设置"},
                            //{ id:1519,pid:15,name:"广告设置"}
                        //]
                    //},
                    //{ id:16,pid:1,name:"业务管理",open:true,
                        //children: [
                            //{ id:164,pid:16,name:"合同范本"},
                            //{ id:165,pid:16,name:"合同列表"},
                            //{ id:166,pid:16,name:"需求调度"}
                        //]
                    //},
                    //{ id:17,pid:1,name:"订单管理",open:true,
                        //children: [
                            //{ id:171,pid:17,name:"商品订单"},
                            //{ id:172,pid:17,name:"用工订单"},
                            //{ id:175,pid:17,name:"供应菜单"}
                        //]
                    //},
                    //{ id:18,pid:1,name:"我的功能",open:true,
                        //children: [
                            //{ id:181,pid:18,name:"免费设计"},
                            //{ id:182,pid:18,name:"装修报价"},
                            //{ id:1817,pid:18,name:"项目用工"}
                        //]
                    //},
                    //{ id:19,pid:1,name:"分润管理",open:true,
                        //children: [
                            //{ id:191,pid:19,name:"分润列表"}
                        //]
                    //},
                    //{ id:110,pid:1,name:"运营管理",open:true,
                        //children: [
                            //{ id:1101,pid:110,name:"代理列表"},
                            //{ id:1102,pid:110,name:"代售商品"}
                        //]
                    //},
                //]
              //}
            //]
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
                //tmp = resp.data['ret'];
                //obj[target] = tmp;
            }).catch(function(resp){
                console.log(resp);
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
    //mappingRule
    siteMPRuleList: [
    ],
};

var defaultMPRule = {
    id: "1", 
    regular_expression:"",
    matching_type: "",
    caseSensitive: "",
    https_type: "",
    //cmdList: [{command_type: "proxy_pass", command_param: ""}]
};

var defaultCmdList = [{command_type: "proxy_pass", command_param: ""}];

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
    //components:{
        //"access_log": access_log
    //},
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
        this.getSites();
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
                this.getSiteDetail(1);
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
            id = tmp.id;
            this.insert_cmdList(id, this.cmdList);
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

        addMappingRule: function(){
            this.addMappingRuleDialogTriggle = true;
            this.mappingRule = JSON.parse(JSON.stringify(defaultMPRule));
            this.cmdList = JSON.parse(JSON.stringify(defaultCmdList));
        },
        
        editMappingRule: function(row){
            this.addMappingRuleDialogTriggle = true;
            this.mappingRule = row;
            console.log(row);
            this.cmdList = row.cmdList;
        },

        saveMappingRule: function(){
            this.mappingRule = this.cmdList;
        },


        delMappingRule: function(row){
            //console.log(row);
        },

        //infoMappingRule: function(row){
            //this.infoMappingRuleDialogTriggle = true;
            //this.infoMappingRuleForm.matchType = 'prefix';
        //},
        addCmd: function(){
            this.newMappingRuleForm.cmdList.push({});
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
        }
    }
});

