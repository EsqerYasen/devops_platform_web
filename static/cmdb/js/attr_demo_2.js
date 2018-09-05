myh3 = Vue.component('myh3', {
    //prop: [],
    template: "#myh3"
});

myh4 = Vue.component('myh4', {
    //prop: [],
    template: "#myh4"
});

function getData(url, obj){
    axios({
        method:'GET',
        url: url
    }).then(function(resp){
        tmp = resp.data['ret'];
        console.log(tmp);
        obj.tableData = tmp;
    }).catch(resp => {
        console.log('Fail:'+resp.status+','+resp.statusText);
    });
}

myTable = Vue.component('myTable', {
    template: "#myTable",
    data: function() {
        return {
            tableData: [
            ],
            CurrentPage: 1,
            Pagesize: 3,
            filter: ''
        }
    },
    computed: {
        Total: function(){
            return this.tableData.length;
        }
    },
    created: function(){
        getData('http://127.0.0.1:8000/restapi/attr/', this);
    },
    filters:{
        pagination: function(td, cp, ps){
            return td.slice((cp-1)*ps,cp*ps);
        }
    },
    methods:{
        triggleDialog: function(){
        },
        HandleSizeChange: function(size){
            this.Pagesize = size;
        },
        HandleCurrentChange: function (page) {
            this.CurrentPage = page;
        }
    }
});

vm = new Vue({
    el: "#app",
    components: {
        'myh3': myh3,
        'myh4': myh4,
        'myTable': myTable
    },
    data:{
        activeNameTab: "attribute",
        componentID: myTable,
        tableData: [
            {id:1, name:'aa'}
        ],
        CurrentPage: 1,
        Pagesize: 3,
        Total: 1
    },
    methods:{
        handleClick: function(tab, event){
            if (tab.name=='attribute'){
                this.componentID = myTable;
            }
            else if (tab.name=='interface'){
                this.componentID = myh4;
            }
        },
        HandleCurrentChange: function(){
        },
        HandleSizeChange: function(){
        }
    }
});
