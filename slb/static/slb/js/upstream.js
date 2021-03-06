defaultUpstreamDetail = {
    id: "-1",
    cluster_name: "",
    load_balancin_strategy: "",
    keep_alive: "",
    check_up_type: "",
    check_up_timeout: "",
    check_up_space: "",
    cluster_nodes: []
};

defaultMultiForm = {
    port: '',
    max_fails: '',
    fail_timeout: '',
    weight: ''
}

function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

var ztree = Vue.component('ztree', {
    data: function(){
        return {
            setting:{
              check: {  
                    enable: true,  
                    nocheckInherit: false,
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
                    if(item.node_name1 && item.node_name2 && item.node_name3 && item.node_name4 && item.node_name5 && item.node_name6 && item.node_name6!='nginx'){
                        item['nocheck'] =false;
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
                vm.treeNodeID = treeNode.id;
                var tmp = treeNode.node_name1 +'_'+ treeNode.node_name2 +'_'+ treeNode.node_name3 +'_'+ treeNode.node_name4 +'_'+ treeNode.node_name5 +'_'+ treeNode.node_name6;
                vm.cluster_name = tmp;
                vm.upstreamNameDialogTriggle = false;
            }
            else{
                vm.treeNodeID = '';
                vm.cluster_name = '';
            }
        },
      },
      created: function(){
          this.initTree();
      },
      mounted(){
          $.fn.zTree.init($("#treeDemo"), this.setting, this.zNodes).expandAll(true);
          this.freshArea();
      }
});

vm = new Vue({
    el: "#app",
    //components:{
        //access_log: access_log
    //},
    data: {
        navIndex: "2",
        activeIndex: "1",
        upstreams: [],
        upstreamDetail: JSON.parse(JSON.stringify(defaultUpstreamDetail)),
        editNodeDialogTriggle: false,
        nodeFormInline: {nodeName: '', ip: '', port: 80, weight: 1, maxFail: 3, timeout: 30, status: 'enable'},
        clusterTreeDialogTriggle: false,
        upstreamNameDialogTriggle: false,
        treeNodeID: '',
        multiForm: JSON.parse(JSON.stringify(defaultMultiForm)),
        multiModifyTriggle: false,
        selected: []
    },
    created: function(){
        //this.getUpstreams();
        window_url = window.location.href;
        upstream_id = parseInt(window_url.split("=")[1]);
        if(upstream_id){
            this.getUpstreamDetail(upstream_id);
        }
        else{
            this.upstreamNameDialogTriggle = true;
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
            }).catch(resp => {
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
        
        //handleNavSelect: function(key, keyPath){
        //},

        //handleUpstreamSelect: function(key, keyPath){
            //console.log(key);
            //this.getUpstreamDetail(key);
            ////this.upstreamDetail.load_balancin_strategy = this.upstreamDetail.load_balancin_strategy.toString();
        //},

        upstreamDetailFormSave: function(){
            //console.log(this.upstreamDetail);
            this.postData('../rest/serviceclusterbyid/', this.upstreamDetail, this.afterUpstreamDetailFormSave);
        },

        afterUpstreamDetailFormSave: function(resp){
            console.log(resp);
            if(resp.data.status==200){
                showMsg(true, resp.data.msg);
                //console.log(this.upstreams);
                if(resp.data.id!=this.upstreamDetail.id){
                    this.upstreams.push({id: resp.data.id, cluster_name: this.upstreamDetail.cluster_name});}
            }
            else{showMsg(false, resp.data.msg);}
        },

        addUpstream: function(){
            this.upstreamDetail = JSON.parse(JSON.stringify(defaultUpstreamDetail));
            this.selectTreeDialogTriggle = true;
        },

        editNode: function(row){
            this.editNodeDialogTriggle = true;
            this.nodeFormInline = row;
        },

        //delNode: function(row){
            ////console.log(row);
            //id = row.id - 1;
            //this.upstreamDetail.nodes.splice(id, 1);
        //},

        submitNode: function(){
            this.editNodeDialogTriggle = false;
            console.log(this.nodeFormInline);
            //if(true){ showMsg(true, "保存节点成功");}
            //else{ showMsg(false, "保存节点失败");}
        },

        getUpstreams: function(){
            this.getData('../rest/serviceclusterlist', {}, this.afterGetUpstreams);
        },

        afterGetUpstreams: function(resp){
            tmp = resp.data['ret'];
            this.upstreams = tmp;
            if(this.upstreams.length>0){
                this.getUpstreamDetail(1);
            }
        },

        getUpstreamDetail: function(upstreamID){
            params = {id: upstreamID}
            this.getData('/slb/rest/serviceclusterbyid', params, this.afterGetUpstreamsDetail);
        },

        afterGetUpstreamsDetail: function(resp){
            tmp = resp.data['ret'];
            this.upstreamDetail = tmp;
        },

        getHosts: function(treeNodeID){
            this.getData('/slb/rest/gethostlistbygrupid/', {group_id: treeNodeID}, this.afterGetHosts);
        },

        afterGetHosts: function(resp){
            if(resp.data.status==200){
                ret_data = resp.data.data;
                console.log(ret_data);
                ret = [];
                for(i=0;i<ret_data.length;i++){
                    var tmp = {};
                    tmp['host_ip'] = ret_data[i].host_ip;
                    tmp['host_id'] = ret_data[i].host_id;
                    tmp['port'] = '80';
                    tmp['weight'] = '1';
                    tmp['max_fails'] = '3';
                    tmp['fail_timeout'] = '2';
                    tmp['state'] = 'enable';
                    ret.push(tmp);
                }
                console.log(ret);
                //this.upstreamDetail['cluster_nodes']= [{host_ip: '1.1.11.1', port:'80'}];
                this.upstreamDetail['cluster_nodes'] = ret;
            }
        },

        handleCloseUpstreamName: function(){
            if(this.cluster_name.length==0){
                showMsg(false, '请输入集群名称');
                this.upstreamNameDialogTriggle = true;
            }
            else{
                this.upstreamDetail.cluster_name = this.cluster_name;
                this.selectTreeDialogTriggle = false;
                this.getHosts(this.treeNodeID);
            }
        },

        multiModify: function(){
            this.multiModifyTriggle = !this.multiModifyTriggle;
            this.multiForm = JSON.parse(JSON.stringify(defaultMultiForm)); 
        },

        syn2nodes: function(key){
            for(var i=0;i<this.selected.length;i++){
                var id = this.selected[i];
                //console.log(this.upstreamDetail.cluster_nodes[id][key]);
                for(var j=0; j<this.upstreamDetail.cluster_nodes.length; j++){
                    if(this.upstreamDetail.cluster_nodes[j].host_id == id){
                        this.upstreamDetail.cluster_nodes[j][key]=this.multiForm[key];
                        break;
                    }
                }
            }
        },

        handleSelectionChange: function(val){
            ret = [];
            for(i=0;i<val.length;i++){
                ret.push(val[i].host_id);
            }
            this.selected = ret;
        }
    }
});
