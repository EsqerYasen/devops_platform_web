function getData(obj, url, tableDataName){
    //console.log(url);
    axios({
        method:'GET',
        url: url,
        params: {
            business_id : obj.business_id
        }
    }).then(function(resp){
        tmp = resp.data['ret'];
        //console.log(tmp);
        vm[tableDataName] = tmp;
    }).catch(resp => {
        console.log('Fail:'+resp.status+','+resp.statusText);
    });
}

function isDuplicate(a, b){
    for(i=0;i<b.length;i++){
        if(a.name==b[i].name){
            return true;
        }
    }
    return false;
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
    getData(obj, obj.url, 'attrTableData');
    obj.changeUrl('int');
    getData(obj, obj.url, 'intTableData');
    //obj.changeUrl('cmt');
    //getData(obj, obj.url, 'comment');
}

vm = new Vue({
    el: '#app',
    data: {
        business_id: 0,
        visible: false,
        attrTableData: [],
        attrCurrentPage: 1,
        attrPagesize: 2,
        attrFilter: '',
        intTableData: [],
        intCurrentPage: 1,
        intPagesize: 3,
        intFilter: '',
        comment: [
            {content: 'aaaaaaaaaaaaaaa'},
            {content: 'bbbbbbbbbbbbbbb'},
            {content: 'ccccccccccccccc'}
        ],
        commentOthers: [
            {content: 'aaaaaaaaaaaaaaa'},
            {content: 'bbbbbbbbbbbbbbb'},
            {content: 'ccccccccccccccc'}
        ],
        cmtInputTriggle: false,
        cmtFormInline: {},
        cmtP: true,
        cmtEditTriggle: false,
        urls: {
            attr: '../../rest/attr/',
            int: '../../rest/interface/',
            cmt: '../../rest/cmt/'
        },
        historyTableData: [],
        historyDialogTriggle: false,
        urls4history: {
            attr: '../../rest/attrHistory/',
            int: '../../rest/interfaceHistory/',
            cmt: '../../rest/cmtHistory/'
        },
        tableDataNames: {
            attr: 'attrTableData',
            int: 'intTableData',
            cmt: 'comment',
        },
        url: 'blank_url',
        tableDataName: '',
        editMethod: 'Edit Dialog',
        editTriggle: false,
        formInline: {name:'', value:''},
        activeNameTab: 'attribute', //tab
        actvieTop: 'idc1Top'
    },
    created: function(){
        this.business_id = document.getElementById('business_id').innerHTML;
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
            this.url = this.urls[src];
        },
        changeTableDataName: function(src){
            this.tableDataName = this.tableDataNames[src];
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
            getData(this, url, tableDataName);
        },
        delRecord: function(row, src){
            vm.changeUrl(src);
            vm.changeTableDataName(src);
            tableDataName = src == 'attr' ? 'attrTableData':'intTableData';
            message_success = 'delete ok';
            message_fail = 'delete fail';
            //console.log(row);
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
        history: function(row, src){
            url = this.urls4history[src]+'?name='+row.name;
            //url = this.urls4history[src];
            //console.log('history url: '+url);
            getData(this, url, 'historyTableData');
            this.historyDialogTriggle = true;
        },
        onSubmit: function(formInline){
            vm.editTriggle=false;
            formInline['business_name_id'] = this.business_id;
            if (vm.editMethod == 'New'){
                method = "create"
                message_success = 'create ok';
                message_fail = 'create fail';
                data = formInline;
                if(isDuplicate(formInline, this[this.tableDataName])){
                    vm.$message.error('Duplicate key');
                    return;
                }
            }
            else{
                method = "modify"
                message_success = 'modify ok';
                message_fail = 'modify fail';
                data = formInline;
            }
            //console.log('submit:'+vm.url);
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
        submitCmt: function(c){
            message = {
                success: 'update ok',
                fail: 'update fail'
            };
            this.changeUrl('cmt');
            this.changeTableDataName('cmt');
            data = {
                content: c.content,
                id: c.id
            };
            this.cmtInputTriggle = false;
            console.log(data);
            //post_cmt(vm.url, data, 'create', message)
        },
        cmtDel: function(){
            message = {
                success: 'delete ok',
                fail: 'delete fail'
            },
            this.changeUrl('cmt');
            this.changeTableDataName('cmt');
            data = {
                id: this.comment.id
            }
            console.log(data);
            //post_cmt(this.url, data, 'delete', message);
        },
        handleClick(tab, event) {
            if (tab.name == 'attribute'){
                console.log(tab.name);
            }
        }
    }
})
