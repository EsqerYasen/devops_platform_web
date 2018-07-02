var byId = function (id) { return document.getElementById(id); };



Vue.filter('transfromTextareaHtml', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.replace(/\n/g,'<br/>');
})


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
        curCmd:{},
        versions:[],
        cmdIndexTop: 1
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
      changeValue:function(obj){
          obj.value = [];
          if(obj.value2){
            obj.value2.map(function(item){
              obj.value.push(item.name);
            })
          }
      },
      changeValue2:function(obj, it){
        obj.value = [];
        it.checked = !it.checked;
        obj.valueSet.map(function(item){
          item.checked? obj.value.push(item.name):'';
        })
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
      if(cmd.tool_versions){  //新增
       this.versions = cmd.tool_versions.split(',');
       if( this.curCmd && !this.curCmd.ignoreData){
           Vue.set(this.curCmd, 'ignoreData', false); //默认不忽略错误
       }
          Vue.set(this.curCmd, 'currentVersion', Number(this.curCmd.currentVersion ?this.curCmd.currentVersion : this.versions[0]).toFixed(1)); //默认选中第一个（最新使用版本）
        // 根据id和版本号查找到对应的参数列表
          this.getParamsByVersion(cmd.tool_id,this.curCmd.currentVersion, null);
      }else if(cmd.command_tool_version){  //编辑
          var _this = this;
          $.get("/platform/toolset/list",function(result){
              result.data.filter(function(version,index){
                  if(cmd.command_tool_id === version.tool_id){
                      _this.versions = version.tool_versions.split(',');
                  }
              });
              console.log("**********",this.versions);
          });
          if( typeof  cmd.default_script_parameter === "string"){
              cmd.default_script_parameter = JSON.parse(cmd.default_script_parameter.replace(/'/g, '"'));
          }
          // 根据id和版本号查找到对应的参数列表
          this.getParamsByVersion(cmd.command_tool_id,cmd.command_tool_version, cmd.default_script_parameter);
      }
       $('#dialogModal').modal('show');
       // if(parseInt(cmd.tool_set_type) !== 4)return;
       if(parseInt(cmd.tool_set_type) !== 5)return;
        // setTimeout(function() {
        //   window.editor = null;
        //   $('.CodeMirror').remove();
        //     if (!window.editor) {
        //       window.editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        //           lineNumbers: true,
        //           styleActiveLine: true,
        //           matchBrackets: true,
        //           theme: 'eclipse'
        //       });
        //       editor.setSize('auto', '250px');
        //     }
        //     window.editor.setValue(cmd.command);
        // },500)

    },
      getParamsByVersion: function (tool_id, currentVersion, default_script_parameter) {
          var _this = this;
          $.get("/working/tools/infobytoolidandversion/?tool_id="+tool_id + "&tool_version=" + Number(currentVersion).toFixed(1),function(result){
              var paramList = [];
              var param = result.data.param;
            if(param){
                var jsonObj =  JSON.parse(param);//转换为json对象
                for(var i=0;i<jsonObj.length;i++){
                    paramList.push(jsonObj[i]);
                }
            }
            // 显示上次更改记录
              if(default_script_parameter) {
                  paramList.filter(function (param, index) {
                      default_script_parameter.filter(function (default_param, default_index) {
                          if (default_param.key === param.paramNameZh) {
                      switch (param.type) {
                          case "text":
                          case  "select":
                                      param.value = default_param.value
                            break;
                          case "multiple":
                                      param.valueSet.filter(function (keyObj, keyIndex) {
                                          if (default_param.value.indexOf(keyObj.name) > -1) {
                                              keyObj.checked = true;
                                          }
                                      });
                              break;
                          default:
                              break;
                      }

                  }
              });
                  });
              }
              Vue.set(_this.curCmd, 'param', paramList);
          });

      },
      changeVersion: function (currentCmd,action) {
        if(action === 'edit'){
            this.getParamsByVersion(currentCmd.command_tool_id, currentCmd.command_tool_version, null)
        }else if(action === 'add'){
          this.getParamsByVersion(currentCmd.tool_id, currentCmd.currentVersion, null)
        }
      },
    closeEdit:function(currentCmd){
        if(currentCmd) {
        this.curCmd = currentCmd;
            console.log("__保存当前工具:",this.curCmd);
            //todo:保存信息
        }
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
          // if(item.tool_set_prime_type == initTop && item.tool_set_type == initLeft){
          if(item.tool_set_type == initLeft){
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
        keywords:'',
      cmdIndexLeft: '1',//当前选中的左边的index
      cmdIndexTop: '1',//当前选中的右边的index
      switchLabelFlag: 1
    }
  },
  methods:{
    findCmdByTopLeft:function(top, left){
      this.cmds = [];
      var cmds = [];
      for(var i in this.taskCmds){
        var item = this.taskCmds[i];
        // if(item.tool_set_prime_type == top && item.tool_set_type == left){
        if(item.tool_set_type == left){
          cmds.push(item);
        }
      }
      this.cmds = cmds;
    },
      search: function(){
        this.cmds = [];
        var cmds = [];
        for(var i in this.taskCmds){
          var item = this.taskCmds[i];
          if( (item.name && (item.name.indexOf(this.keywords)>=0) ) ){
            cmds.push(item);
          }
        }
        this.cmds = cmds;
      },
    changeCmdLeftIndex: function(item, index){
      this.cmdIndexLeft = index;
      this.findCmdByTopLeft(this.cmdIndexTop, this.cmdIndexLeft);
    },
    changeCmdTopIndex: function(index){
      // if(parseInt(index) !== 1){
      //   Alertwin.alert({ message: '本功能正在维护中'});
      //   return;
      // }
      //   this.cmdIndexTop = index;
      // this.findCmdByTopLeft(this.cmdIndexTop, this.cmdIndexLeft);
        this.switchLabelFlag = index;
    },
      addVaraibleObj: function () {
          store.commit('addVariable');
      },
      delVar:function(i){
          store.commit('removeVar', i);
      },
  },
  template:'#task-cmds'
});


var transApiDataToLocal  = function(apiData){
  var steps = apiData.steps;
    var vars = [];
    if(apiData.vars){
        vars = apiData.vars;
  }
  for(var i in steps){
    var tmp = steps[i];
    tmp.tlines = [];
    for(var i$1=0;i$1<tmp.lines.length; i$1++){
      var item = tmp.lines[i$1];
      if(item.param){
        item.param.map(function(item){
          if(item.value && item.type === 'multiple')item.value =  item.value.split(',') ;
        })
      }
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
  if(steps && steps.length > 0){
      steps.filter(function (step){
          if(!step.vars){
             Vue.set(step,'vars',[]);
          }
      });
  }
  store.commit('setSteps', steps);
  store.commit('setVars', vars);
  console.log('解析接口数据: ', apiData, steps);
};
var transLocalToApiData = function(basic, steps,vars){
    console.log("------------transLocalToApiData",steps);
    // 全局变量
    var validVars = [];
    if(vars && vars.length > 0){
        //获取有效变量，key=null 或 value=null均为无效变量
        vars.filter(function (varObj,index) {
            if(varObj.key && varObj.value){
                validVars.push(varObj);
            }
        });
    }
  var res = {name: basic.name,vars:validVars};
  for(var key in basic){
    res[key] = basic[key];
  }
  res.steps = [];
  for(var i=0; i<steps.length; i++ ){
    var step = steps[i];//左边大步
    res.steps[i] = {lines:[],name:steps[i].name,is_skip:steps[i].is_skip?1:0, activeIndex:steps[i].activeIndex, seq_no:i+1, target_group_ids:steps[i].target_group_ids,target_host_list:steps[i].target_host_list,go_live:steps[i].go_live,target_type:steps[i].target_type };
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



