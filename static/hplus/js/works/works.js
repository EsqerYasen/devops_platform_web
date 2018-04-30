var store = new Vuex.Store({
  state:{
    basic:{},
    steps:[],
    activeIndex:0 //当前最左边index
  },
  mutations:{
    setBasic:function(state, basic){
      state.basic = basic;
      console.log(arguments.callee.name, basic, '------');
    },
      setHost:function(state, obj){
        state.steps[state.activeIndex].target_group_ids = obj.group_id;
        state.steps[state.activeIndex].target_host_list = obj.go_live;
      },
    removeTesk:function(state,index){
      state.steps.splice(index,1)
    },
    addTask:function (state) {
      state.steps.push({
        "lines":[],
        "name":'双击修改',
        "activeIndex":-1,
        "isGroup":false
      });
      state.activeIndex=state.steps.length-1
    },
    setActive:function(state,index){
      state.activeIndex=index
    },
    setSteps: function(state, tl){
      state.steps = [].slice.call(Object.create(tl));
    },
    deleteDesk:function(state,indexObj){
      var linesListLen = state.steps[state.activeIndex]['lines'][indexObj.ind1]['list'].length;
      if(linesListLen<=1){
        state.steps[state.activeIndex]['lines'].splice(indexObj.ind1,1);
      }else{
        if(indexObj.ind2===state.steps[state.activeIndex]['lines'][indexObj.ind1]['activeIndex']){
          Vue.set(state.steps[state.activeIndex]['lines'][indexObj.ind1],'activeIndex',0)
        }
        state.steps[state.activeIndex]['lines'][indexObj.ind1]['list'].splice(indexObj.ind2,1);
      }
    },
    deleteDeskAll:function(state,i){
      state.steps[state.activeIndex]['lines'].splice(i,1)
    },
    tabClick:function(state,indexObj){
      if(state.steps[state.activeIndex]['lines'].length!=0){
        state.steps[state.activeIndex]['lines'][indexObj.ind1]['activeIndex']=indexObj.ind2;
      }
    },
    selectTool:function(state,i){
      state.steps[state.activeIndex]['activeIndex']=i
    }
  }
});