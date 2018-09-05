function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

vm = new Vue({
    el: "#app",
    data: {
        sites: []
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
            //if(this.sites.length>0){
                //this.getSiteDetail(1);
            //}
            //this.getPools();
            //this.getNginxClusters();
        },

        delSite: function(siteID){
            this.getData('../rest/delsite', {id: siteID}, this.afterDelSite);
        },

        afterDelSite: function(resp){
            data = resp.data['ret'];
            console.log(data.status);
            if(data.status==200){
                showMsg(true, data.msg);
                this.getSites();
            }
            else{
                showMsg(false, data.msg);
            }
        }

    }
});

