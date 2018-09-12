//editor = CodeMirror.fromTextArea(document.getElementById("previewTextArea"), {
    ////mode: 'shell',
    //lineNumbers: true,
    //readOnly: false,
    //lineSeparator: "\r\n"
    ////theme: "eclipse"
//});
Vue.component('my_access_log',{
    template: '<el-input v-model="cmdcmdarg" @change="argUpdated($event, row)"></el-input></div>',
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
    template: '<div>pool_name: <el-select v-model="cmdcmdarg" placeholder="请选择" @change="argUpdated($event, row)"> <el-option v-for="item in upstreams" :key="item.id" :label="item.cluster_name" :value="item.id"> </el-option> </el-select></div>',
    props: ['cmdarg', 'row'],
    data: function(){
        return {
            upstreams: vm.upstreams,
            initValue: ''
        }
    },
    computed:{
        cmdcmdarg: {
            get: function(){
                return this.cmdarg; 
            },
            set: function(v){}
        }
    },
    methods: {
        argUpdated: function(w, r){
            console.log(w);
            this.$emit('updatecmdarg', {v:w, s:r});
        },
    }
});

Vue.component('action_proxy_pass',{
    template: `
    <div>
        <el-form-item label="pool name">
            <el-select v-model="cmdcmdarg" placeholder="请选择" @change="argUpdated($event)">
                <el-option v-for="item in upstreams" :key="item.id" :label="item.cluster_name" :value="item.id"> </el-option> 
            </el-select>
        </el-form-item>
    </div>
    `,
    props: ['cmdarg', 'index'],
    data: function(){
        return {
            upstreams: vm.upstreams,
            initValue: ''
        }
    },
    computed:{
        cmdcmdarg: {
            get: function(){ return this.cmdarg; },
            set: function(v){
            }
        }
    },
    methods: {
        argUpdated: function(w){
            //console.log(w);
            //console.log(this.cmdarg);
            //console.log(this.index);
            this.$emit('innerUpdateAction', {v:w, index: this.index});
        },
    }
});

Vue.component('action_custom',{
    template:`
    <div>
        <el-form-item label="custom">
            <el-input v-model="cmdcmdarg" v-on:input="argUpdated($event)"> </el-input>
        </el-form-item>
    </div>
    `,
    props: ['cmdarg', 'index'],
    computed: {
        cmdcmdarg: {
            get: function(){return this.cmdarg;},
            set: function(v){}
        },
    },
    methods: {
        argUpdated: function(val){
            //console.log(val);
            //console.log(this.row);
            this.$emit('innerUpdateAction', {v:val, index: this.index});
        },
    },
});

Vue.component('my_ifelse',{
    template: `
    <div>
        condition: 
        <el-input v-model="cmdcmdarg.condition" v-on:input="argUpdated($event, row)">
            <el-dropdown slot="append" @command="addAction">
                <span class="el-dropdown-link"> <i class="el-icon-plus el-icon--right"></i></span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item v-for="item,index in stateOptions" :command="item" :key="index">{{item}}</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
        </el-input>
        statements:
        <component v-for="action,index in cmdcmdarg.actions" v-on:innerUpdateAction="handleUpdateActions" :index="index" :is="'action_'+action.cmdType" :cmdarg="action.cmdArg" :key="index"></component>
    </div>
    `,
    props: ['cmdarg', 'row', 'cmd'],
    data: function(){
        return {
            statementType: "aaa",
            stateOptions: ["proxy_pass", "custom"],
            statementType: "proxy_pass"
        }
    },
    computed: {
        cmdcmdarg: {
            get: function(){ return this.cmdarg; },
            set: function(v){
            }
        },
    },
    methods: {
        argUpdated: function(w, r){
            //console.log('condition');
            //console.log(w);
            this.cmdcmdarg.condition = w;
            this.$emit('updatecmdarg', {v:this.cmdcmdarg, s:r});
        },
        handleUpdateActions: function(v){
            index = v['index'];
            val = v['v'];
            this.cmdcmdarg.actions[index].cmdArg = val;
            console.log(this.cmdcmdarg);
            this.$emit('updatecmdarg', {v:this.cmdcmdarg, s:this.row});
        },
        addAction: function(val){
            this.cmdcmdarg.actions.push({cmdType: val, cmdArg: ""});
        }
    },
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

Vue.component('my_static-resource',{
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

                //console.log(this.zNodes);
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
    dynamicAttributes: []
};

var defaultMPRule = {
    id: "-1", 
    regular_expression:"",
    matching_type: "",
    case_sensitive: true,
    https_type: "",
    seq_no: "-1",
    cmd_list: [{command_type: "access_log", command_param: ""}]
};

var defaultCmdList = {command_type: "access_log", command_param: ""};

var testMPRule = [
    {id: "1", regular_expression:"/root", matching_type: "prefix", case_sensitive: true, https_type: "all", cmd_list: [{command_type: "proxy_pass", command_param: "test_proxy_pass"}, {command_type: "access_log", command_param: "test_access_log"}]},
    {id: "2", regular_expression:"/root/a", matching_type: "common", case_sensitive: true, https_type: "http", cmd_list: [{command_type: "access_log", command_param: "access_log"}]},
    {id: "3", regular_expression:"/root/b", matching_type: "regex", case_sensitive: false, https_type: "all", cmd_list: [{command_type: "more_clear_headers", command_param: "clear_headers"}]},
    {id: "4", regular_expression:"/root/c", matching_type: "excat", case_sensitive: true, https_type: "https", cmd_list: [{command_type: "more_set_headers", command_param: "set_header"}]}
];

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
        mappingRule: {
            id: "1", 
            regular_expression: '',
            matching_type: '',
            case_sensitive:'Y',
            https_type: ['all'],
            access_log: "",
            error_log: "",
            error_page_400: "",
            error_page_404: "",
            root: "",
            cmd_list: [{command_type: 'proxy_pass', command_param: 'abc'}]
        },
        cmd_list: [],
        pools: [],
        clusterTreeDialogTriggle: false,
        previewDialogTriggle: false,
        previewContent: '',
        editor: null,
        compareEditor: null,
        mydefine: "my_access_log",
        upstreams: [],
        coption:"选择自定义参数",
        free_options: [],
        freeOptionDialog: false,
        dynamicAttributes: [
            {param_key: "access_log", param_value: "", is_inner: 1}, 
            {param_key: "error_log", param_value: "", is_inner: 1},
            {param_key: "error_page_400", param_value: "", is_inner: 1},
            {param_key: "error_page_404", param_value: "", is_inner: 1},
            {param_key: "root", param_value: "", is_inner: 1},
            {param_key: "include", param_value: "", is_inner: 1},
            {param_key: "custom", param_value: "", is_inner: 0}
        ],
        freeOptionKV: {param_key: "", param_value: "", is_inner: 0},
        //VersionCompare
        versionA: '',
        versionB: '',
        versionContent: {}
    },
    created: function(){
        //this.getSites();
        window_url = window.location.href;
        site_id = parseInt(window_url.split("=")[1]);
        this.getClusters();
        if(site_id){
            //console.log(site_id);
            this.getSiteDetail(site_id);
        }
        else{
            this.siteNameDialogTriggle = true;
        }
        
    },
    methods:{
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
        },

        getSiteDetail: function(id){
            this.getData('../rest/getmngsiteinfo/', {'id': id}, this.afterGetSiteDetail);
        },

        mergeDynamicAttr: function(){
            for(var i=0; i<this.siteDetail.dynamicAttributes.length; i++){
                var tmp_key = this.siteDetail.dynamicAttributes[i].param_key;
                for(var j=0; j<this.dynamicAttributes.length; j++){
                    if(tmp_key==this.dynamicAttributes[j].param_key){
                        this.dynamicAttributes[j]['active'] = true; //disable this key
                    }
                }
            }
        },

        afterGetSiteDetail: function(resp){
            tmp = resp.data['ret'];
            //console.log(tmp);
            this.siteDetail = tmp;
            this.mergeDynamicAttr();
            this.getSiteVersion(this.siteDetail.id);
            this.getMPRuleList(this.siteDetail.id);
        },

        getSiteVersion: function(id){
            this.getData('../rest/deployversionbysiteid', {id:id}, this.afterGetSiteVersion);
        },

        afterGetSiteVersion: function(resp){
            var tmp = resp.data['ret'];
            //console.log(tmp);
            this.siteVersions = tmp;
            this.selectedVersion = tmp[0].k;
        },

        getMPRuleList: function(nginx_site_id){
            this.getData('../rest/getmappingruleslist', {'nginx_site_id': nginx_site_id}, this.afterGetMPRuleList);
        },

        afterGetMPRuleList: function(resp){
            tmp = resp.data['ret']
            //console.log(tmp);
            this.siteMPRuleList = tmp;
            for(i=0;i<this.siteMPRuleList.length;i++){
                this.getCmdList(this.siteMPRuleList[i].id, i);
            }
        },

        getCmdList: function(rule_id, mp_index){
            //console.log(mp_index);
            this.getData('../rest/getcmdlist', {'id': rule_id}, this.afterGetCmdList, [mp_index]);
        },

        afterGetCmdList: function(resp, args){
            tmp = resp.data['ret'];
            //console.log(tmp);
            this.cmd_list = tmp.cmd_list;
            mp_index = args[0];
            this.siteMPRuleList[mp_index].cmd_list = tmp.cmd_list;
            this.mappingRule = this.siteMPRuleList[mp_index];
        },

        insert_cmdList: function(index, cmd_list){
            //console.log(this.siteMPRuleList[0].id);
            //console.log(index);
            for(i=0; i<this.siteMPRuleList.length; i++){
                if(this.siteMPRuleList[i].id == index){
                    //console.log('get')
                    this.siteMPRuleList[i].cmd_list= cmd_list;
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

        getClusters: function(){
            this.getData('../rest/serviceclusterlist', {}, this.afterGetUpstreams);
        },

        afterGetUpstreams: function(resp){
            tmp = resp.data['ret'];
            this.upstreams = tmp;
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

        checkTabChange: function(){

            if(this.siteDetail.id <= 0){
                showMsg(false, "站点未创建，请先保存站点信息");
                return false;
            }
            else{return true;}
        },

        handleTabChange: function(tab){
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
                if(this.siteDetail.id<0){ this.siteDetail.id=tmp.id;}
            }
            else{ showMsg(false, tmp.msg);}
        },

        jumpUp: function(index) {
            //console.log(row.id);
            if(index==0){return;}
            previousId = index-1;
            tmpCurrent = this.siteMPRuleList[index];
            tmpCurrent.seq_no = tmpCurrent.seq_no-1;
            tmpPrevious = this.siteMPRuleList[previousId];
            tmpPrevious.seq_no = tmpPrevious.seq_no+1;
            this.siteMPRuleList.splice(previousId, 2, tmpCurrent, tmpPrevious);
        },

        jumpDown: function(index) {
            if(index==this.siteMPRuleList.length-1){return;}
            laterId = index+1;
            tmpCurrent = this.siteMPRuleList[index];
            tmpCurrent.seq_no = tmpCurrent.seq_no+1;
            tmpLater = this.siteMPRuleList[laterId];
            tmpLater.seq_no = tmpLater.seq_no-1;
            this.siteMPRuleList.splice(index, 2, tmpLater, tmpCurrent);
        },

        jumpDoubleUp: function(index){
            if(index==0){return;}
            tmp = this.siteMPRuleList[index];
            tmp.seq_no=1;
            for(i=0; i<index; i++){
                this.siteMPRuleList[i].seq_no = this.siteMPRuleList[i].seq_no+1;
            }
            this.siteMPRuleList.splice(index, 1);
            this.siteMPRuleList.unshift(tmp);
        },

        jumpDoubleDown: function(index){
            if(index==this.siteMPRuleList.length-1){return;}
            tmp = this.siteMPRuleList[index];
            tmp.seq_no = this.siteMPRuleList.length;
            for(i=index+1; i<this.siteMPRuleList.length; i++){
                this.siteMPRuleList[i].seq_no = this.siteMPRuleList[i].seq_no-1;
            }
            this.siteMPRuleList.splice(index, 1);
            this.siteMPRuleList.push(tmp);
        },

        handleCmdargChange: function(val){
            //val is dict: {input-content, scope} 
            console.log(val);
            this.mappingRule.cmd_list[val.s.$index].command_param = val.v;
        },

        saveMappingRuleList: function(){
            if(this.siteDetail.id<0){
                this.siteDetailFormSave();
            }
            while(this.siteDetail.id<0){}
            data = {id: 0, mapping_rules_list: this.siteMPRuleList, nginx_site_id: this.siteDetail.id}
            this.postData('../rest/mappingrulescreateorupdate/', data, this.afterSaveMappingRuleList);
        },

        afterSaveMappingRuleList: function(resp){
            if(resp.data.status==200){
                this.getMPRuleList(this.siteDetail.id);
                showMsg(true, resp.data.msg);
            }
            else{
                showMsg(false, resp.data.msg);
            }
        },

        addMappingRule: function(){
            this.addMappingRuleDialogTriggle = true;
            this.mappingRule = JSON.parse(JSON.stringify(defaultMPRule));
        },
        
        editMappingRule: function(row, row_index){
            //console.log(row_index);
            this.getCmdList(row.id, row_index);
            //this.mappingRule = this.siteMPRuleList[row.id];
            //this.mappingRule = this.siteMPRuleList[0];
            this.addMappingRuleDialogTriggle = true;
        },

        getUpstreamName: function(cmd_param){
            for(var i=0;i<this.upstreams.length;i++){
                if(cmd_param==this.upstreams[i].id){
                    return this.upstreams[i].cluster_name;
                }
            }
        },

        fillProxyPass: function(mpRule){
            var cluster_name = "";
            for(var i=0;i<mpRule.cmd_list.length;i++){
                if(mpRule.cmd_list[i].command_type=="proxy_pass"){
                    command_param = mpRule.cmd_list[i].command_param;
                    cluster_name = this.getUpstreamName(command_param);
                    var tmp = mpRule.cmd_list[i];
                    tmp['service_cluster_name'] = cluster_name;
                    mpRule.cmd_list[i] = tmp;
                }
                else if(mpRule.cmd_list[i].command_type=="ifelse"){
                    for(var j=0;j<mpRule.cmd_list[i].command_param.actions.length;j++){
                        var statementType = mpRule.cmd_list[i].command_param.actions[j].cmdType;
                        if(statementType=='proxy_pass'){
                            var cluster_id = mpRule.cmd_list[i].command_param.actions[j].cmdArg;
                            cluster_name = this.getUpstreamName(cluster_id);
                            mpRule.cmd_list[i].command_param.actions[j]['service_cluster_name'] = cluster_name;
                        }
                    }
                }
            }
        },

        saveMappingRule: function(){
            this.mappingRule.nginx_site_id = this.siteDetail.id;
            this.fillProxyPass(this.mappingRule);
            //console.log(this.mappingRule);
            if(this.mappingRule.seq_no<=0){
                this.mappingRule.seq_no = this.siteMPRuleList.length + 1;
                var data = this.mappingRule;
            }
            else{
                for(var i=0;i<this.siteMPRuleList.length;i++){
                    this.fillProxyPass(this.siteMPRuleList[i])
                }
                console.log(this.siteMPRuleList);
                var data = {id: 0, mapping_rules_list: this.siteMPRuleList, nginx_site_id: this.siteDetail.id};
            }
            console.log(this.mappingRule);
            this.postData('../rest/mappingrulescreateorupdate/', data, this.afterSaveMappingRule);
            this.addMappingRuleDialogTriggle = false;
        },

        afterSaveMappingRule: function(resp){
            if(resp.data.status==200){
                showMsg(true, resp.data.msg);
                this.getMPRuleList(this.siteDetail.id);
            }
            else{
                showMsg(false, resp.data.msg);
            }

        },

        reseqMP: function(row_index){
            //row_index will be removed
            //this.siteMPRuleList.splice(row_index, 1);
            for(i=row_index+1;i<this.siteMPRuleList.length;i++){
                this.siteMPRuleList[i].seq_no = this.siteMPRuleList[i].seq_no-1;
            }
            this.siteMPRuleList[row_index].is_enabled = 0;
        },

        delMappingRule: function(row, row_index){
            //console.log(row);
            this.reseqMP(row_index);
            data = {id: 0, mapping_rules_list: this.siteMPRuleList, nginx_site_id: this.siteDetail.id}
            this.postData('../rest/mappingrulescreateorupdate/', data, this.afterDelMappingRule);
        },

        afterDelMappingRule: function(resp){
            if(resp.data.status==200){
                this.getMPRuleList(this.siteDetail.id);
                showMsg(true, resp.data.msg);
            }
            else{
                showMsg(false, resp.data.msg);
            }
        },

        //infoMappingRule: function(row){
            //this.infoMappingRuleDialogTriggle = true;
            //this.infoMappingRuleForm.matchType = 'prefix';
        //},
        addCmd: function(){
            this.mappingRule.cmd_list.push(JSON.parse(JSON.stringify(defaultCmdList)));
        },

        delCmd: function(index){
            this.mappingRule.cmd_list.splice(index,1);
        },

        cmdTypeChange: function(cmdType, index){
            //console.log(cmdType);
            //console.log(index);
            if(cmdType=='access_log'){
                this.mydefine = 'my_access_log'; 
                this.mappingRule.cmd_list[index].command_param = "";
            }
            else if(cmdType=='proxy_pass'){
                this.mydefine = 'my_proxy_pass';
                this.mappingRule.cmd_list[index].command_param = "";
            }
            else if(cmdType=='more_clear_headers'){
                this.mydefine = 'my_more_clear_headers'; 
                this.mappingRule.cmd_list[index].command_param = "";
            }
            else if(cmdType=='more_set_headers'){
                this.mydefine = 'my_more_set_headers'; 
                this.mappingRule.cmd_list[index].command_param = "";
            }
            else if(cmdType=='static-resource'){
                this.mydefine = 'my_static_resource'; 
                this.mappingRule.cmd_list[index].command_param = "";
            }
            else if(cmdType=='rewrite'){
                this.mydefine = 'my_rewrite'; 
                this.mappingRule.cmd_list[index].command_param = "";
            }
            else if(cmdType=='return'){
                this.mydefine = 'my_return'; 
                this.mappingRule.cmd_list[index].command_param = "";
            }
            else if(cmdType=='ifelse'){
                this.mydefine = 'my_ifelse'; 
                this.mappingRule.cmd_list[index].command_param = {condition: "", actions:[]};
            }
        },

        previewConfigFile: function(){
            this.previewDialogTriggle = true;
            var data = {siteDetail: this.siteDetail, mplist: this.siteMPRuleList}
            this.postData('../rest/configpreview/', data, this.afterPreviewConfigFile);
        },

        afterPreviewConfigFile: function(resp){
            if (resp.data['ret'].status==200){
                this.previewContent = resp.data['ret'].config;
                if(this.editor == null){
                    this.editor = CodeMirror.fromTextArea(document.getElementById("previewTextArea"), {
                        mode:'nginx',
                        lineNumbers: true,
                        readOnly: false,
                        lineSeparator: "\n",
                        //theme: ''
                    });
                }
                this.editor.setValue(this.previewContent);
            }
            else{
                showMsg(false, resp.data['ret'].msg);
            }
        },

        //previewShow: function(){
            //this.editor = CodeMirror.fromTextArea(document.getElementById("previewTextArea"), {
                //lineNumbers: true,
                //readOnly: false,
                //lineSeparator: "\r\n",
            //});
            //this.editor.setValue('aaa');
        //},

        createDist: function(){
            //console.log(this.siteDetail);
            id = this.siteDetail.id;
            this.getData('../rest/deployversioncreateview', {id:id}, this.afterCreateDist);
        },

        afterCreateDist: function(resp){
            tmp = resp.data['ret'];
            if(tmp.status==200){
                showMsg(true, tmp.msg);
                var task_id = tmp['task_id'];
                var version = tmp['version'];
                var data = {version: version, task_id: task_id, name: this.siteDetail.site_name};
                if(this.siteVersions[0]['version']<version){
                    this.siteVersions.unshift(data);
                }
            }
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

        handleCommand: function(command){
            //console.log(command);
            var options = {access_log: 0, error_log: 1, error_page_400:2, error_page_404: 3, root: 4, include: 5, custom: 6}
            index = options[command];
            this.siteDetail.dynamicAttributes.push(JSON.parse(JSON.stringify(this.dynamicAttributes[index])));
            this.dynamicAttributes[index].active = true;
        },

        freeOptionDialogSubmit: function(){
            this.freeOptionDialog = false;
            this.siteDetail.dynamicAttributes.push(JSON.parse(JSON.stringify(this.freeOptionKV)));
        },

        cancelFreeOptionDialog: function(){
            this.freeOptionDialog = false;
            this.freeOptionKV = {}
        },

        delFreeOption: function(option_name){
            //var option_name_dict = {0: "access_log", 1: "error_log", 2: "error_page_400", 3: "error_page_404", 4: "root"}
            //console.log(option_name);
            for(var i=0; i<this.siteDetail.dynamicAttributes.length;i++){
                if(this.siteDetail.dynamicAttributes[i].param_key == option_name){
                    this.siteDetail.dynamicAttributes.splice(i, 1);
                }
            }
            for(var i=0; i<this.dynamicAttributes.length;i++){
                if(this.dynamicAttributes[i].param_key == option_name){
                    break;
                }
            }
            var tmp_dynamicAttr = this.dynamicAttributes[i];
            tmp_dynamicAttr['active'] = false;
            Vue.set(this.dynamicAttributes, i, tmp_dynamicAttr);
        },

        handleVa: function(va){
        },

        startCompare: function(){
            if(this.versionA.length!=0 && this.versionB.length!=0){
                //if(!(this.versionA in this.versionContent) || !(this.versionB in this.versionContent)){
                    var data = {id: this.siteDetail.id, v1: this.versionA, v2: this.versionB}
                    this.getData('../rest/configversiondiff/', data, this.afterStartCompare);
                //}
                //else{
                    //this.doCompare(this.versionContent[this.versionA], this.versionContent[this.versionB]);
                //}
            }
            else{
                showMsg(false, "请选择版本");
            }
        },

        doCompare: function(data1, data2){
            if(this.compareEditor == null){
                this.compareEditor = CodeMirror.MergeView(document.getElementById('compare'), {
                    value: data1,
                    origLeft: null,
                    orig: data2,
                    lineNumbers: true, 
                    mode: "nginx",
                    styleActiveLine: true,
                    matchBrackets: true,
                    highlightDifferences: true,
                    connect: null,
                    collapseIdentical: false,
                    revertButtons:false,
                });
            }
            else{
                this.compareEditor.orig=data1;
                this.compareEditor.orig=data2;
            }
        },

        afterStartCompare: function(resp){
            var tmp = resp.data;
            if(tmp.status==200){
                this.versionContent[this.versionA] = tmp.data[this.versionA];
                this.versionContent[this.versionB] = tmp.data[this.versionB];
                this.doCompare(this.versionContent[this.versionA], this.versionContent[this.versionB]);
            }
            else{showMsg(false, tmp.msg)}
        },

        handleVb: function(va){
            console.log(va);
            console.log(this.versionA);
        }

    }
});

//cmd_list = [
    //{
        //command_type: 5, proxy_pass
        //command_param: "12",
        //service_cluster_name : "kfc_preorder_nh_pilot_idc_ng"
    //},

    //{
        //command_type: 1, access_log
        //command_param: "example_access",
    //},
    //{
        //command_type: 3, ifelse
        //command_param: {
            //condition: "example_condition",
            //actions: [
                //{
                    //cmdType: "proxy_pass",
                    //cmdArg: "12",
                    //service_cluster_name: "kfc_preorder_nh_pilot_idc_ng"
                //},
                //{
                    //cmdType: "custom",
                    //cmdArg: "example_custom"
                //}
            //]
        //},
    //},
//]

