function showMsg(boolFlag, msg){
    if(boolFlag){ vm.$message({ message:msg, type: 'success', center: true });}
    else{ vm.$message.error(msg);}
};

vm = new Vue({
    el: "#app",
    data: {
        tasks: [
            //{task_id:"1", task_name:"test1", status:"新建", created_by: "robin", create_time:"2018 09-01"},
            //{task_id:"2", task_name:"test2", status:"完成", created_by: "Go", create_time:"2018 09-02"},
            //{task_id:"3", task_name:"test3", status:"新建", created_by: "python", create_time:"2018 09-03"},
            //{task_id:"4", task_name:"test4", status:"新建", created_by: "perl", create_time:"2018 09-05"},
            //{task_id:"5", task_name:"test5", status:"新建", created_by: "ruby", create_time:"2018 09-05"}
        ]
    },
    created: function(){
        this.getTasks();
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

        getTasks: function(){
            this.getData('../../rest/deploytaskslist', {}, this.afterGetTasks);
        },

        render_tag_status: function(){
            var tagClass_dict = {"running": "label label-warning", "success": "label label-success", "fail": "label label-danger", "default": "label label-default"}
            for(var i=0;i<this.tasks.length;i++){
                try{
                    this.tasks[i]["tagClass"] = tagClass_dict[this.tasks[i]["status"]];}
                catch(err){
                    this.tasks[i]["tagClass"] = tagClass_dict["default"];}
                //task = this.tasks[i];
                //if(task.status == "running"){
                    //this.tasks[i]["tagStatus"] = "info"; 
                //}
                //else if(task.status == "success"){
                    //this.tasks[i]["tagStatus"] = "success"; 
                //}
                //else if(task.status == "fail"){
                    //this.tasks[i]["tagStatus"] = "danger"; 
                //}
                //else{
                    //this.tasks[i][""]
                //}
            }
        },

        afterGetTasks: function(resp){
            tmp = resp.data['ret'];
            this.tasks= tmp['results'];
            this.render_tag_status();
        },

        delTask: function(task_id){
            params = {id:task_id}
            this.getData('', params, this.afterDelTask);
        },

        afterDelTask: function(resp){
            data = resp.data['ret'];
            if(data.status==200){
                showMsg(true, data.msg);
                this.getTasks();
            }
            else{
                showMsg(false, data.msg);
            }
        }

    }
});

