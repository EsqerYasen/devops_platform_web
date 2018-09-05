function getData(url, tableDataName){
    axios({
        method:'GET',
        url: url
    }).then(function(resp){
        tmp = resp.data['ret'];
        vm[tableDataName] = tmp;
        initBusinessCata(vm);
    }).catch(resp => {
        console.log('Fail:'+resp.status+','+resp.statusText);
    });
}

function initTable(obj){
    getData(obj.url, 'businessData');
}

function initBusinessCata(obj){
    tmp = [];
    for(i=0;i<obj.businessData.length;i++){
        tmp.push({'cataName': obj.businessData[i].catalog, 'checked': false});
    }
    tmp_json = {};
    for(i=0;i<tmp.length;i++){
        if(tmp_json[tmp[i].cataName]!=1){
            obj.business_cata.push(tmp[i]);
            tmp_json[tmp[i].cataName] = 1;
        }
    }
}

vm = new Vue({
    el: '#el-app',
    data: {
        businessData: [],
        CurrentPage: 1,
        Pagesize: 2,
        filter: '',
        url: '../rest/business/',
        editMethod: 'Edit Dialog',
        editTriggle: false,
        formInline: {id:-1, business_name:''},
        //business_cata: [
            //{'cataName':'KFC', 'checked': true},
            //{'cataName':'TACO', 'checked': false}
        //],
        business_cata: []
    },
    created: function(){
        initTable(this);
    },
    computed:{
        Total: function(){
            return this.businessData.length;
        }
    },
    //watch: {
        //businessData: function(){ //关注的变量名: businessData, 变量名变化时执行函数
        //}
    //},
    filters: {
        pagination: function(td, cp, ps){
            return td.slice((cp-1)*ps,cp*ps);
        },
        cataFilter: function(td, cata){
            //console.log(td);
            //console.log(cata);
            tmp = [];
            for(i=0; i<cata.length; i++){
                for(j=0; j<td.length; j++){
                    if(cata[i].checked && td[j].catalog==cata[i].cataName){
                        tmp.push(td[j]);
                    }
                }
            }
            //console.log(tmp);
            return tmp;
        },
        contentFilter: function(td, content){
            ret = [];
            for(var i=0; i<td.length; i++){
                if(td[i].business_name.indexOf(content)>=0 || td[i].owner.indexOf(content)>=0){
                    ret.push(td[i]);
                }
            }
            return ret;
        }
    },
    methods: {
        HandleSizeChange: function(size) {
            this.Pagesize = size;
        },
        HandleCurrentChange: function(currentPage, keyName){
            this[keyName]= currentPage;
        },
        triggleNew: function(src){
            vm.editMethod = "New";
            vm.editTriggle = true;
        },
        triggleUpdate: function(row){
            vm.formInline = row;
            vm.editMethod = "Update";
            vm.editTriggle = true;
        },
        refreshTableData: function(url){
            getData(url, 'businessData');
        },
        delRecord: function(row){
            message_success = 'delete ok';
            message_fail = 'delete fail';
            axios({
                method:'POST',
                url: vm.url,
                data: {
                    method:'delete',
                    record: row
                },
                //headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function(resp){
                //console.log(resp.data);
                if (resp.data['result'] >= 0){
                    vm.$message({
                        message:message_success,
                        type: 'success',
                        center: true
                    });
                    vm.refreshTableData(vm.url);
                }
                else{
                    vm.$message.error(message_fail+':'+resp.data['err_msg']);
                }
            }).catch(resp => {
                vm.$message.error(message_fail);
            });
        },
        onSubmit: function(formInline){
            vm.editTriggle=false;
            if (vm.editMethod == 'New'){
                method = "create"
                message_success = 'create ok';
                message_fail = 'create fail';
            }
            else{
                method = "modify"
                message_success = 'modify ok';
                message_fail = 'modify fail';
            }
            //console.log(formInline);
            axios({
                method:'POST',
                url: vm.url,
                data: {
                    method: method,
                    record: formInline
                },
                //headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function(resp){
                if (resp.data['result'] >= 0){
                    vm.$message({
                        message:message_success,
                        type: 'success',
                        center: true
                    });
                    //console.log(vm.businessData);
                    vm.refreshTableData(vm.url, 'businessData');
                }
                else{
                    vm.$message.error(message_fail+':'+resp.data['err_msg']);
                }
            }).catch(resp => {
                vm.$message.error(message_fail);
            });
        }
    }
})
