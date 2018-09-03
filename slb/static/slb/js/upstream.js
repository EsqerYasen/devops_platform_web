defaultUpstreamDetail = {
    upstreamName: "",
    policy: "round-robin",
    longConnectionCount: 20,
    healthCheck: "TCP",
    timeout: 3000,
    interval: 3000,
    //degradeRatio:
    //degrade:
    nodes: []
};

function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

vm = new Vue({
    el: "#app",
    //components:{
        //access_log: access_log
    //},
    data: {
        navIndex: "2",
        activeIndex: "1",
        upstreams: [],
        upstreamDetail: defaultUpstreamDetail,
        editNodeDialogTriggle: false,
        nodeFormInline: {nodeName: '', ip: '', port: 80, weight: 1, maxFail: 3, timeout: 30, status: 'enable'},
        postSuccessFlag: false,
    },
    created: function(){
        this.getUpstreams();
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
        
        handleNavSelect: function(key, keyPath){
        },

        handleUpstreamSelect: function(key, keyPath){
            console.log(key);
            this.getUpstreamDetail(1);
            //this.upstreamDetail.load_balancin_strategy = this.upstreamDetail.load_balancin_strategy.toString();
        },

        upstreamDetailFormSave: function(){
            //console.log(this.upstreamDetail);
            data = {data: this.upstreamDetail, operation: 'create'};
            this.postData('../rest/serviceclusterbyid/', data, this.afterUpstreamDetailFormSave);
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
            this.upstreamDetail = defaultUpstreamDetail;
            this.nginxClusterDialogTriggle = true;
        },

        editNode: function(row){
            this.editNodeDialogTriggle = true;
            this.nodeFormInline = row;
        },

        delNode: function(row){
            //console.log(row);
            id = row.id - 1;
            this.upstreamDetail.nodes.splice(id, 1);
        },

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
            this.getData('../rest/serviceclusterbyid', params, this.afterGetUpstreamsDetail);
        },

        afterGetUpstreamsDetail: function(resp){
            tmp = resp.data['ret'];
            this.upstreamDetail = tmp;
        },

    }
});
