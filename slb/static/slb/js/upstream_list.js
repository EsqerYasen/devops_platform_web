function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

vm = new Vue({
    el: "#app",
    data: {
        upstreams: []
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
            }).catch(function(resp){
                console.log(resp);
                console.log('Fail:'+resp.status+','+resp.statusText);
            });
        },

        //postData: function(url, data, func){
            //obj = this;
            //axios({
                //method:'POST',
                //url: url,
                //data: data
            //}).then(function(resp){
                //func(resp);
            //}).catch(resp => {
                //console.log('Fail:'+resp.status+','+resp.statusText);
            //});
        //},

        getUpstreams: function(){
            //this.sites =  [
                //{id: "1", site_name: "site-1"},
                //{id: "2", site_name: "site-2"},
                //{id: "3", site_name: "site-3"},
                //{id: "4", site_name: "site-4"}
            //];
            this.getData('../rest/serviceclusterlist', {}, this.afterGetUpstreams);
        },

        afterGetUpstreams: function(resp){
            tmp = resp.data['ret'];
            this.upstreams = tmp;
        },

        delUpstream: function(upstreamID){
            params = {id: upstreamID}
            this.getData('/slb/rest/serviceclusterdel/', params, this.afterDelUpstream);
        },

        afterDelUpstream: function(resp){
            data = resp.data['ret'];
            if(data.status==200){
                showMsg(true, data.msg);
                this.getUpstreams();
            }
            else{
                showMsg(false, data.msg);
            }
        }

    }
});

