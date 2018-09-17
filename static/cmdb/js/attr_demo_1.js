var debug = true;
var mockingComments = [{
                    id: 10,
                    comment: '10 comment',
                    date: '2018-01-02',
                    userId: '2',
                    userName: "a"
                },
                {
                    id: 11,
                    comment: '11 comment',
                    date: '2018-02-03',
                    userId: '3',
                    userName: "b"
                },
                {
                    id: 12,
                    comment: '12 comment',
                    date: '2018-03-04',
                    userId: '1',
                    userName: "c"
                },
                {
                    id: 13,
                    comment: '13 comment',
                    date: '2018-04-05',
                    userId: '2',
                    userName: "a"
                },
                {
                    id: 14,
                    comment: '14 comment',
                    date: '2018-01-06',
                    userId: '3',
                    userName: "b"
                },
                {
                    id: 15,
                    comment: '15 comment',
                    date: '2018-01-07',
                    userId: '1',
                    userName: "c"
                },
                {
                    id: 16,
                    comment: '16 comment',
                    date: '2018-01-08',
                    userId: '2',
                    userName: "a"
                }
                ];
var mockingComments2 = [{
                    id: 10,
                    comment: '10a comment',
                    date: '2018-01-02',
                    userId: '2',
                    userName: "a"
                },
                {
                    id: 11,
                    comment: '11a comment',
                    date: '2018-02-03',
                    userId: '3',
                    userName: "b"
                },
                {
                    id: 12,
                    comment: '12a comment',
                    date: '2018-03-04',
                    userId: '1',
                    userName: "c"
                },
                {
                    id: 13,
                    comment: '13a comment',
                    date: '2018-04-05',
                    userId: '2',
                    userName: "a"
                },
                {
                    id: 14,
                    comment: '14a comment',
                    date: '2018-01-06',
                    userId: '3',
                    userName: "b"
                },
                {
                    id: 15,
                    comment: '15a comment',
                    date: '2018-01-07',
                    userId: '1',
                    userName: "c"
                },
                {
                    id: 16,
                    comment: '16a comment',
                    date: '2018-01-08',
                    userId: '2',
                    userName: "a"
                }
                ];


Vue.component('yum-edit-comment',{
    props: ['currentComment', 'commentId'],
    data: function(){
        return{
            commentText: this.currentComment
        }
    },
    template: `
                <el-input
                  type="textarea"
                  :rows="2"
                  placeholder="请输入内容"
                  @change="commentUpdate"
                  v-model="commentText">
                </el-input>
    `,
    methods: {
        commentUpdate: function(w){
        },
    },
    created: function(){
    }
});
Vue.component('yum-comment-timeline-my-comment',{
    props: ['comment', 'temporaryComment'],
    data: function(){
        return {
            isEdit: false,
            btnClass: '',
            btnEditClass: 'fa fa-edit',
            btnTickClass: 'fa fa-check',
            currentComment: ''
        }
    },
    template: `
        <li  class="event">
            <div v-if="isEdit === false">
                <div>
                    {{comment.comment}}
                </div>
                <div>
                    {{comment.date}}
                </div>
            </div>
            <div v-else :class="'comment_text_'+comment.id" >
                <yum-edit-comment :currentComment="comment.comment" :commentId="comment.id"></yum-edit-comment>
            </div>

            <div class="edit_comment">
                <i class="fa fa-times" @click="cancelEdit" v-show="isEdit === true"></i>
                <i :class="btnClass" @click="tick"></i>
            </div>
        </li>
    `,
    template2: `
        <li class="event others">
            <div>
                <div>
                    {{comment.comment}}
                </div>
                <div>
                    {{comment.userName? 'By ' + comment.userName : '' }} {{comment.date}}
                </div>
            </div>
        </li>
    `,
    methods: {
        tick: function(e){
            if (!this.isEdit) {
                this.isEdit = true;
                this.btnClass = this.btnTickClass;
            } else {
                if (this.isEdit) {
                    // this.btnClass = this.btnTickClass;
                    if ($.trim($('.comment_text_'+this.comment.id +' textarea').val()) !== '') {
                        this.isEdit = false;
                        this.btnClass = this.btnEditClass;
                        this.$emit('comment:commit', {v:$('.comment_text_'+this.comment.id +' textarea').val(), id: this.comment.id});
                    } else {
                        $('.comment_text_'+this.comment.id+':visible').addClass('error');
                    }
                } else {
                    this.btnClass = this.btnEditClass;
                }
            }

        },
        cancelEdit: function(){
            this.isEdit = false;
            this.btnClass = this.btnEditClass;
            this.$emit('comment:cancel');
        }
    },
    created: function(){
        this.btnClass = this.btnEditClass;
        this.currentComment = this.comment.comment;
    }
});

Vue.component('yum-comment-timeline-other-comment',{
    props: ['comment', 'userid'],
    template: `
        <li class="event others">
            <div>
                <div>
                    {{comment.comment}}
                </div>
                <div>
                    {{comment.userName? 'By ' + comment.userName : '' }} {{comment.date}}
                </div>
            </div>
        </li>
    `,
    created: function(){
    },

});
Vue.component('yum-comment-timeline-time-node',{
    props: ['comment', 'siteComments'],
    template: `
    <li class="year">
            <div>
                {{comment.nodeText}}
            </div>
        </li>
    `,
    created: function(){
    },
});
Vue.component('yum-comment-timeline-node',{
    props: ['comment', 'userid', 'siteComments'],
    template: `
        <component :is="'yum-comment-timeline-'+comment.type"
                v-bind:comment="comment"
                @comment:commit="commentCommit"
                @comment:cancel="commentCancelEdit"
                @comment:update="handleCommentUpdate"
                />

    `,
    methods: {
        handleCommentUpdate: function(arg){
            this.temporaryComment = arg.v;
            this.commentId = arg.commentId;

        },
        commentCommit: function(args){
            var msg = {text: args.v,  commentId: args.id};
            this.$emit('comment:commit', msg);
            this.temporaryComment = '';
            this.commentId = false;
        },
        commentCancelEdit:function(args){
            this.temporaryComment = '';
            this.editedComment = false;
        }
    },
    created: function(){
        this.className = this.comment.className;
    }
});

Vue.component('yum-comment-topics',{
    props: ['userid', 'siteid'],
    data: function(){
        return {
            topics: []
        }
    },
    template: `
        <div>
        <select @change="changeTopic">
            <option v-for="topic in topics" v-bind:value="topic.id">
                {{topic.text}}
            </option>
        </select>
        </div>
    `,
    methods:{
        changeTopic: function(e){
            var topicId = $(e.target).val();
            if (topicId) {
                if (topicId === -1) {
                    this.$emit('topic:showPopup');
                } else {
                    this.$emit('topic:changed', {topicId: topicId});
                }
            }
        },
        createTopic: function(msg){
            var data = {
                topic: msg.v,
                siteId: this.siteid
            }
            $.ajax({
              type: 'POST',
              url: '../rest/createTopic/',
              data: data,
              dataType: 'application/x-www-form-urlencoded'
            }).then(this.getTopics.bind(this), function(){
                console.warn('!!!using debug data !!!...........>>>>', this.siteComments);
                var matchedComment;
                if (debug) {
                    console.warn('!!!using debug data !!!');
                    this.topics.push(
                        {
                            id: this.topics.length,
                            text: msg.v
                        }
                    );

                }
            }.bind(this));
        },
        getTopics: function(){
            $.get('../rest/getTopics/', {
                "siteId": this.siteid
            }).then(function(topics){
                this.topics = topics;
                return this.topics;
            }.bind(this), function(){
                if (debug) {
                    console.warn('!!!using debug data !!!');
                    this.topics = [{id:'', text: "---"},{id:-1, text: "新增"},{id:1, text: "aaa"}, {id:2, text: "bbb"}, {id:3, text: "ccc"}];
                }
            }.bind(this));
        },
    },
    created: function(){
        this.getTopics();
    },
});
Vue.component('yum-comment-timeline',{
    props: ["siteid", "userid", "topicid"],
    name: "yum_timeline",
    data:function(){
        return {
            siteComments:[],
            showPop: false,
            newCommentText: '',
            btnClass: 'fa fa-check'
        }
    },
    template: `
            <div>
                <div class="t_right">
                <i
                    class="fa fa-comments fa-2x add-comment"
                    @click="showCommentPopup"
                    />
                </div>
                <ul class='timeline' >
                    <yum-comment-timeline-node @comment:commit="commentCommit"
                      v-for="comment in siteComments"
                      :siteComments="siteComments"
                      :comment="comment"
                      v-bind:key="comment.id"
                      v-bind:userid="userid"
                      v-bind:siteid="siteid"
                      v-bind:topicid="topicid"
                    ></yum-comment-timeline-node>
                </ul>
            </div>`,
    methods: {
        tick: function(){
            this.showPop = false;
        },
        closePopup: function(){
            this.showPop = false;
        },
        showCommentPopup: function(){
            this.$emit('show:commmet:popup', true);
        },
        createComment: function(args){
            var data = {
                comment: args.v,
                topicId: this.topicId,
                siteId: this.siteid
            }
            $.ajax({
              type: 'POST',
              url: '../rest/updateComments/',
              data: data,
              dataType: 'application/x-www-form-urlencoded'
            }).then(this.getComments.bind(this), function(){
                console.warn('!!!using debug data !!!...........>>>>', this.siteComments);
                var matchedComment;
                if (debug) {
                    console.warn('!!!using debug data !!!');
                    var d = new Date()
                    this.siteComments.unshift({
                        id: this.siteComments.length+10,
                        isComment: true,
                        comment: args.v,
                        className: 'event',
                        type: 'my-comment',
                        idx: this.siteComments.length,
                        date: d,
                    })

                    this.siteComments.unshift({
                        isComment: false,
                        nodeText: d.getHours() +'/'+ (d.getMinutes()) +'/'+ d.getSeconds(),
                        // nodeText: d.getFullYear() +'/'+ (d.getMonth()+1) +'/'+ d.getDate(),
                        extraClass: this.siteComments.length === 0 ? 'first': '',
                        type: 'time-node',
                        idx: this.siteComments.length

                    })
                }
            }.bind(this));
        },
        resetSiteComments: function(){
            this.siteComments.splice(0, this.siteComments.length);
        },
        getComments: function(){
            $.get('../rest/getComments/', {
                "topicId": this.topicid,
                "siteId": this.siteid
            }).then(function(comments){
                this.siteComments = this.objToArrays(this.arrangeCommentsByDate(comments));
                return this.siteComments;
            }.bind(this), function(){
                if (debug) {
                    console.warn('!!!using debug data !!!');
                    var list = Math.random(1) >= 0.5 ? mockingComments: mockingComments2;
                    this.siteComments = this.objToArrays(this.arrangeCommentsByDate(list));
                }
            }.bind(this));
        },
        commentCommit: function(arg){
            var data = {
                id: arg.commentId,
                text: arg.text
            }
            $.ajax({
              type: 'POST',
              url: '../rest/updateComments/',
              data: data,
              dataType: 'application/x-www-form-urlencoded'
            }).then(this.getComments.bind(this), function(){
                console.warn('!!!using debug data !!!...........>>>>', this.siteComments);
                if (debug) {
                    console.warn('!!!using debug data !!!');
                    $.each(this.siteComments, function(i, comment){
                        if (comment.id === data.id) {
                            comment.comment = data.text;
                            this.siteComments.splice(i, 1, comment);
                        }

                    }.bind(this))
                }
            }.bind(this));
        },
        objToArrays: function(obj){
            var keys = Object.keys(obj);
            var currentUserId = this.userid;
            var commentLines = [];
            var idx = 0;
            if (keys && keys.length) {
                keys = keys.sort(function(a,b){return b>a});
                $.each(keys, function(_i, key){
                    commentLines.push({
                        isComment: false,
                        nodeText: key,
                        extraClass: commentLines.length === 0 ? 'first': '',
                        type: 'time-node',
                        idx: commentLines.length

                    })
                    if (obj[key]){
                        $.each(obj[key], function(__i, _comment){
                            commentLines.push($.extend(true, _comment, {
                                isComment: true,
                                comment: _comment.comment,
                                className: (_comment.userId - currentUserId === 0) ? 'event': 'event others',
                                type: (_comment.userId - currentUserId === 0) ? 'my-comment':'other-comment',
                                idx: commentLines.length
                            }))
                        })

                    }
                })
            }
            return commentLines;
        },
        arrangeCommentsByDate: function(comments){
            var sorted = {};
            var d, timeStr;
            if (comments && comments.length) {
                $.each(comments, function(idx, comment){
                    d = new Date(comment.date);
                    timeStr = [d.getFullYear(), (d.getMonth()+1)<10? ('0'+(d.getMonth()+1)): d.getMonth()+1].join('-');
                    if (typeof sorted[timeStr] === 'undefined') {
                        sorted[timeStr] = [];
                    }
                    sorted[timeStr].push(comment);
                    sorted[timeStr].sort(function(a,b){return a.date<b.date})
                });

                return sorted;
            } else {
                return {};
            }
        },
        getTopics: function(){

        }
    },

    created: function(){
        window.tl =  this;
        this.getComments(1, 2);
    },

});
function getData(url, tableDataName){
    axios({
        method:'GET',
        url: url
    }).then(function(resp){
        tmp = resp.data['ret'];
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
        //activeNames: ['2', '3'], //collapse

        comment: {
            'content':'comment',
            'pub_date':''
        },
        
        url: 'blank_url',
        tableDataName: '',
        editMethod: 'Edit Dialog',
        editTriggle: false,
        formInline: {id:-1, name:'', value:''},
        activeNameTab: 'attribute', //tab
        actvieTop: 'idc1Top'
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
        },
        handleClick(tab, event) {
            if (tab.name == 'attribute'){
                console.log(tab.name);
            }
        }
    }
})
