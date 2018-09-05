function getData(url, tableDataName){
    axios({
        method:'GET',
        url: url
    }).then(function(resp){
        tmp = resp.data['ret'];
        console.log(tmp);
        vm[tableDataName] = tmp;
    }).catch(resp => {
        console.log('Fail:'+resp.status+','+resp.statusText);
    });
}

function post_cmt(url, content, method, message){
    axios({
        method:'POST',
        url: url,
        data: {
            method: method,
            record: content
        },
        //headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    }).then(function(resp){
        if (resp.data['result'] >= 0){
            vm.$message({
                message:message.success,
                type: 'success',
                center: true
            });
            //console.log(vm.tableDataName);
            vm.refreshTableData(vm.url, vm.tableDataName);
        }
        else{
            vm.$message.error(message.fail+':'+resp.data['err_msg']);
        }
    }).catch(resp => {
        vm.$message.error(message.fail);
    });
}

function initTable(obj){
    obj.changeUrl('attr');
    getData(obj.url, 'attrTableData');
    obj.changeUrl('int');
    getData(obj.url, 'intTableData');
    obj.changeUrl('cmt');
    getData(obj.url, 'comment');
}

vm = new Vue({
    el: '#app',
    data: {
        visible: false,
        attrTableData: [],
        attrCurrentPage: 1,
        attrPagesize: 2,
        attrFilter: '',
        intTableData: [],
        intCurrentPage: 1,
        intPagesize: 3,
        intFilter: '',
        activeNames: ['2', '3'], //collapse

        comment: {
            'content':'comment',
            'pub_date':''
        },
        
        url: 'blank_url',
        tableDataName: '',
        editMethod: 'Edit Dialog',
        editTriggle: false,
        formInline: {id:-1, name:'', value:''}
    },
    created: function(){
        initTable(this);
    },
    computed:{
        attrTotal: function(){
            return this.attrTableData.length;
        },
        intTotal: function(){
            return this.intTableData.length;
        },
    },
    //watch: {
        //attrFilter: function(){
            //console.log('a watch');
        //}
    //},
    filters: {
        pagination: function(td, cp, ps){
            return td.slice((cp-1)*ps,cp*ps);
        },
        contentFilter: function(td, content){
            ret = [];
            for(var i=0; i<td.length; i++){
                if(td[i].name.indexOf(content)>=0 || td[i].value.indexOf(content)>=0){
                    ret.push(td[i]);
                }
            }
            return ret;
        }
    },
    methods: {
        attrHandleSizeChange: function(size) {
            this.attrPagesize = size;
        },
        attrHandleCurrentChange: function(currentPage, keyName){
            this[keyName]= currentPage;
        },
        intHandleSizeChange: function(size) {
            this.intPagesize = size;
        },
        intHandleCurrentChange: function(currentPage, keyName){
            this[keyName]= currentPage;
        },
        changeUrl: function(src){
            tmp = {
                attr: 'http://127.0.0.1:8000/restapi/attr/',
                int: 'http://127.0.0.1:8000/restapi/int/',
                cmt: 'http://127.0.0.1:8000/restapi/cmt/'
            };
            this.url = tmp[src];
        },
        changeTableDataName: function(src){
            tmp = {
                attr: 'attrTableData',
                int: 'intTableData',
                cmt: 'comment',
            };
            this.tableDataName = tmp[src];
        },
        triggleNew: function(src){
            vm.changeUrl(src);
            vm.changeTableDataName(src);
            vm.editMethod = "New";
            vm.editTriggle = true;
        },
        triggleUpdate: function(row, src){
            vm.changeUrl(src);
            vm.changeTableDataName(src);
            vm.formInline = row;
            vm.editMethod = "Update";
            vm.editTriggle = true;
        },
        refreshTableData: function(url, tableDataName){
            getData(url, tableDataName);
        },
        delRecord: function(row, src){
            vm.changeUrl(src);
            vm.changeTableDataName(src);
            tableDataName = src == 'attr' ? 'attrTableData':'intTableData';
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
                if (resp.data['result'] >= 0){
                    vm.$message({
                        message:message_success,
                        type: 'success',
                        center: true
                    });
                    vm.refreshTableData(vm.url, vm.tableDataName);
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
                    //console.log(vm.tableDataName);
                    vm.refreshTableData(vm.url, vm.tableDataName);
                }
                else{
                    vm.$message.error(message_fail+':'+resp.data['err_msg']);
                }
            }).catch(resp => {
                vm.$message.error(message_fail);
            });
        },
        submitCmt: function(){
            message = {
                success: 'update ok',
                fail: 'update fail'
            }
            this.changeUrl('cmt');
            this.changeTableDataName('cmt');
            post_cmt(vm.url, this.comment, 'create', message)
        }
    }
})
