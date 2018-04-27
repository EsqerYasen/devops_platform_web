Vue.component('yum-alert', {
  template:'<div transiton="fade" style="width:300px;text-align:center;" class="alert alert-warning" v-show="message">\n' +
  '    <a href="javascript:;" class="close" data-dismiss="alert" @click="close">\n' +
  '        &times;\n' +
  '    </a>\n' +
  '    <strong>{{ message }}</strong>\n' +
  '</div>',
  data:function(){
  },
  methods:{
    close:function(){
      store.state.message = '';
    }
  },
  props:['message']
});