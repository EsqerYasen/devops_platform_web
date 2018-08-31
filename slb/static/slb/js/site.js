Vue.component('my_access_log',{
    props: ['cmdarg'],
    template: '<el-input v-model="cmdarg"></el-input>'
});

Vue.component('my_proxy_pass',{
    props: ['cmdarg'],
    template: '<div>pool_name: <el-input v-model="cmdarg"></el-input></div>'
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

function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

var defaultSiteDetail = {
        //basicConfig
        site_name: "abc",
        status: "ENABLE",
        domainName: "",
        port: 80,
        defaultPool: "",
        targetNginx: "",
        group: "default-grp",
        httpsFlag: false,
        //mappingRule
        mappingRules: [
            {id: 1, path:'/root', matchType: 'prefix', caseSensitive: 'Y', httpType: ['http', 'https'], cmdList: [{cmdType: 'proxy_pass', cmdArg: 'proxy_pass'}]},
            {id: 2, path:'/root/a', matchType: 'common', caseSensitive: 'Y', httpType: ['http'], cmdList: [{cmdType: 'access_log', cmdArg: 'access_log'}]},
            {id: 3, path:'/root/b', matchType: 'regex', caseSensitive: 'N', httpType: ['http', 'https'], cmdList: [{cmdType: 'more_clear_headers', cmdArg: 'clear_headers'}]},
            {id: 4, path:'/root/c', matchType: 'excat', caseSensitive: 'Y', httpType: ['http'], cmdList: [{cmdType: 'more_set_headers', cmdArg: 'set_header'}]}
        ],
    };

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
        siteDetail: defaultSiteDetail,
        siteMPRuleList: [],
        siteVersions: [],
        selectedVersion: '',
        addMappingRuleDialogTriggle: false,
        newMappingRuleForm:{id: -1, path: '', matchType: '', caseSensitive:'Y', httpType: ['http', 'https'], cmdList: [{cmdType: 'proxy_pass', cmdArg: 'abc'}] },
        //cmdArgDiv: my_access_log, 
        pools: [],
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
            this.getPools();
            this.getNginxClusters();
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
            //return siteDetails[id-1];
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
        
        handleNavSelect: function(key, keyPath){
        },

        handleSiteSelect: function(key, keyPath){
            //console.log(key);
            this.activeIndex = key;
            this.siteDetail = this.getSiteDetail(key);
            this.siteDetailActiveTabName = "basicConfig";
        },

        handleSiteDetailActiveTabClick: function(tab){
            //console.log(tab);
            //this.tabName = "basicConfig";
        },

        addSite: function(){
            this.siteDetail = defaultSiteDetail;
            this.siteDetailActiveTabName = "basicConfig";
            this.siteNameDialogTriggle = true;
        },

        saveSiteName: function(){
            this.siteNameDialogTriggle = false;
        },

        editSiteDetail: function(){
            this.siteDetailDivStatus = 'wr';
        },

        siteDetailFormSave: function(){
            this.postData('../', this.siteDetail, this.afterPostSiteDetail);
        },

        afterPostSiteDetail: function(resp){
            tmp = resp.data['ret']
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
            tmpCurrent = this.siteDetail.mappingRule[id];
            tmpCurrent.id = previousId+1;
            tmpPrevious = this.siteDetail.mappingRule[previousId];
            tmpPrevious.id = id+1;
            this.siteDetail.mappingRule.splice(previousId, 2, tmpCurrent, tmpPrevious);
        },

        jumpDown: function(row) {
            //console.log(row.id);
            if(row.id==this.siteDetail.mappingRule.length){return;}
            id = row.id-1; //align wiht array
            laterId = id+1;
            tmpCurrent = this.siteDetail.mappingRule[id];
            tmpCurrent.id = laterId+1;
            tmpLater = this.siteDetail.mappingRule[laterId];
            tmpLater.id = id+1;
            this.siteDetail.mappingRule.splice(id, 2, tmpLater, tmpCurrent);
        },

        jumpDoubleUp: function(row){
            id = row.id-1;
            tmp = this.siteDetail.mappingRule[id];
            tmp.id=1;
            for(i=0; i<id; i++){
                this.siteDetail.mappingRule[i].id = this.siteDetail.mappingRule[i].id+1;
            }
            this.siteDetail.mappingRule.splice(id, 1);
            this.siteDetail.mappingRule.unshift(tmp);
        },

        jumpDoubleDown: function(row){
            id = row.id-1;
            tmp = this.siteDetail.mappingRule[id];
            tmp.id = this.siteDetail.mappingRule.length;
            for(i=id+1; i<tmp.id; i++){
                this.siteDetail.mappingRule[i].id = this.siteDetail.mappingRule[i].id-1;
            }
            this.siteDetail.mappingRule.splice(id, 1);
            this.siteDetail.mappingRule.push(tmp);
        },

        addMappingRule: function(){
            this.addMappingRuleDialogTriggle = true;
            //this.newMappingRuleForm.httpType = "ALL";
            //this.newMappingRuleForm.matchType = "prefix";
            //this.newMappingRuleForm.caseSensitive = true;
            //this.newMappingRuleForm.cmdList.push({id: -1, cmdType: 'proxy_pass', cmdArg: 'abc'});
        },
        
        submitNewMappingRule: function(){
            //console.log(this.newMappingRuleForm);
            this.newMappingRuleForm.id = this.siteDetail.mappingRules.length+1;
            this.siteDetail.mappingRules.push(this.newMappingRuleForm);
            this.addMappingRuleDialogTriggle = false;
        },

        editMappingRule: function(row){
            this.addMappingRuleDialogTriggle = true;
            //console.log(row);
            this.newMappingRuleForm = row;
            this.getCmdList(row.id);
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
            this.siteDetail['cmd_list'] = this.cmdList;
            //console.log(siteDetail);
            this.postData('../rest/configfile', {'siteConfig':siteDetail}, afterPreviewConfigFile);
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
        }
    }
});

