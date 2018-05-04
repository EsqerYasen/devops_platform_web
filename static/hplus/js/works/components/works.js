var byId = function (id) { return document.getElementById(id); };
Vue.component('task-list', {
  template: '#task-list',
  methods:{
    delTask:function(i){
      store.commit('removeTesk', i);
    },
    addTask:function(){
      store.commit('addTask');
    },
    changeActive:function(i){
      store.commit('setActive', i);
    }
  }
});



Vue.component('task-info', {
  data: function(){
    return {
      taskInfo:{},
        curCmd:{}
    }
  },
  template: '#task-info',
  methods: {
    deleteTask:function(indexObj){
      store.commit('deleteDesk', indexObj);
    },
      selectHost:function(){

      $("#select_host_modal").modal({show:true});

      },

    deleteTaskAll:function(index){
      store.commit('deleteDeskAll', index);

    },
    tabClick:function(indexObj){
      store.commit('tabClick',indexObj);
    },
    changeSeqType: function(v){
      var curStep = this.$store.state.steps[this.$store.state.activeIndex];
      if(!curStep)return;
      Vue.set(curStep, 'isGroup', !!v);
    },
    updateLines: function(e){
      var curStep = this.$store.state.steps[this.$store.state.activeIndex];
      if(!curStep)return;
      var cmd = JSON.parse(JSON.stringify(curStep['lines'][e.newIndex])) ;
      cmd.is_skip = cmd.is_skip || 0;
      curStep['lines'].splice(e.newIndex, 1);
      if(curStep.isGroup && curStep.activeIndex>=0&&curStep['lines'][curStep.activeIndex]){//并
        if(curStep['lines'][curStep.activeIndex]['list']){
          if(curStep['lines'][curStep.activeIndex]['list'].length>=4){
            Vue.set(this.$store.state, 'message',   ('并行操作最多4个'));
            return;
          }
          curStep['lines'][curStep.activeIndex]['list'].push(cmd);
        }
      }else{
        Vue.set(curStep['lines'], e.newIndex, {list:[cmd],activeIndex:0});
      }
    },
    showEdit:function(index){
      var cmd = this.curCmds[index]['list'][this.curCmds[index]['activeIndex']||0];
      this.curCmd = cmd;
       $('#dialogModal').modal('show');

        setTimeout(function() {
            if (!window.editor) {
              window.editor = CodeMirror.fromTextArea(document.getElementById("code"), {
                  lineNumbers: true,
                  styleActiveLine: true,
                  matchBrackets: true,
                  theme: 'eclipse'
              });
              editor.setSize('auto', '250px');
            }
            window.editor.setValue(cmd.command);
        },500)

    },
    closeEdit:function(){
      if(window.editor){
        this.curCmd.command =  window.editor.getValue() ;
        window.editor.setValue('');
      }
      $('#dialogModal').modal('hide')
    },

    selectTool:function(index){
      // alert(index);
      store.commit('selectTool',index);
    }
  },
  computed:{
    curCmds: function(){
      return this.$store.state.steps[this.$store.state.activeIndex] && this.$store.state.steps[this.$store.state.activeIndex]['lines'] || [];
    },
    steps:function(){
      return this.$store.state.steps[this.$store.state.activeIndex]
    }

  }
});



Vue.component('task-cmds', {
  data: function(){
    var t = this;

     $.get("/platform/toolset/list",function(result){

       var _taskCmds = result;
        //服务端数据替换区=============================================================
        var  top = {}, left =  {};
        for(var i in _taskCmds.data){
          top[_taskCmds.data[i].tool_set_prime_type] = _taskCmds.data[i].tool_set_prime_type_zh;
          left[_taskCmds.data[i].tool_set_type] = _taskCmds.data[i].tool_set_type_zh;
        }
        var taskCmds  = _taskCmds.data;

        var cmds = [];
        var initTop = Object.getOwnPropertyNames(top)[0];
        var initLeft = Object.getOwnPropertyNames(left)[0];
        for(var i in taskCmds){
          var item = taskCmds[i];
          if(item.tool_set_prime_type == initTop && item.tool_set_type == initLeft){
            cmds.push(item);
          }
        }
        t.taskCmds = taskCmds;
        t.top = top;
        t.left = left;
        t.cmds = cmds;
        t.cmdIndexLeft = initLeft;
        t.cmdIndexTop = initTop;
     });

    return {
      taskCmds:[],
      top: {},
      left: {},
      cmds:[],
      cmdIndexLeft: '1',//当前选中的左边的index
      cmdIndexTop: '1'//当前选中的右边的index
    }
  },
  methods:{
    findCmdByTopLeft:function(top, left){
      this.cmds = [];
      var cmds = [];
      for(var i in this.taskCmds){
        var item = this.taskCmds[i];
        if(item.tool_set_prime_type == top && item.tool_set_type == left){
          cmds.push(item);
        }
      }
      this.cmds = cmds;
    },
    changeCmdLeftIndex: function(item, index){
      this.cmdIndexLeft = index;
      this.findCmdByTopLeft(this.cmdIndexTop, this.cmdIndexLeft);
    },
    changeCmdTopIndex: function(item, index){
      this.cmdIndexTop = index;
      this.findCmdByTopLeft(this.cmdIndexTop, this.cmdIndexLeft);
    }
  },
  template:'#task-cmds'
});


var transApiDataToLocal  = function(apiData){
  var steps = apiData.steps;
  for(var i in steps){
    var tmp = steps[i];
    tmp.tlines = [];
    for(var i$1=0;i$1<tmp.lines.length; i$1++){
      var item = tmp.lines[i$1];
      if(!tmp.tlines[item.sub_seq_no-1]){
        tmp.tlines[item.sub_seq_no-1] = {
          list:[]
        };
      }
        {
          var x = tmp.lines[i$1];
          if(!x  ){
            console.error('命令解析失败')
          }
        }
      tmp.tlines[item.sub_seq_no-1].list.push(tmp.lines[i$1]);
    }
    tmp.lines = tmp.tlines;
    delete tmp.tlines;
  }
  delete apiData.steps;
  store.commit('setBasic', apiData);
  store.commit('setSteps', steps);
  console.log('解析接口数据: ', apiData, steps);
};
var transLocalToApiData = function(basic, steps){
  var res = {name: basic.name};
  for(var key in basic){
    res[key] = basic[key];
  }
  res.steps = [];
  for(var i=0; i<steps.length; i++ ){
    var step = steps[i];//左边大步
    res.steps[i] = {lines:[],name:steps[i].name, is_skip:steps[i].is_skip?1:0, activeIndex:steps[i].activeIndex, seq_no:i+1, target_group_ids:steps[i].target_group_ids,target_host_list:steps[i].target_host_list,go_live:steps[i].go_live,target_type:steps[i].target_type };
    for(var i$1=0; i$1<step.lines.length; i$1++ ){//中间一块
      for(var i$$1=0; i$$1<step.lines[i$1].list.length; i$$1++){//一个命令块
        var tls = JSON.parse(JSON.stringify(step.lines[i$1].list[i$$1]));
        tls.sub_seq_no = parseInt(i$1)+1;
        tls.is_skip = tls.is_skip ? 1:0;
        res.steps[i].lines[res.steps[i].lines.length] = tls;
      }
    }
  }

  console.log(arguments.callee.name, JSON.stringify(res), '---');
  return res;
};



