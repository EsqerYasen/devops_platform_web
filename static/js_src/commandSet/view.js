  var Backbone = require('backbone');
  Backbone.$ = exports.$ = window.jQuery;
  var _ = require('underscore');
  window.YUMEVENTS = _.extend({}, Backbone.Events);
  var gridTemplate = require('./templates/partials/grid.ejs');

  var Screen = Backbone.View.extend({
    el: '.wrapper-content',
    userInfo: false,
    model: false,
    userId: false,
    permssions: [],
    events: {
      'click .btn-primary.search': 'search',
    },
    initialize: function(user, userId, model) {
      console.log('view inited');
      this.userInfo = user;
      this.model = model;
      this.userId = userId;
      // $('.scrollable').scroll(this.onScroll.bind(this));
      $('.scrollable').scroll(_.debounce(this.onScroll.bind(this), 1000));
      window.YUMEVENTS.on("loadmore", this.loadMore.bind(this));
      this.showList();
      // $('.scrollable').height(650);
    },
    //var name = $('.btn-primary.search').val()
    search: function(e){
      this.name = $('input#name').val();
      $('.command_set_list tbody').empty();
      this.showList();
      e.preventDefault();
      e.stopPropagation();
    },
    showList: function(limit, offset) {

      this.model.getList(this.userId, limit, offset, this.name).then(function(res) {
        var model = this.model;
        //{1:'常用命令',2:'上传文件',3:'远程文件',4:'shell脚本',5:'自定义'}
        this.appendToGrid({
          results: res
        });
      }.bind(this));
    },
    appendToGrid: function(param) {
      var lists = param.results;
      var versions = param.versions;
      var permissions = param.permissions || [];
      var val = 0;
      if (lists.length) {
        $.each(lists, function(i, item) {
          $('.command_set_list tbody').append(gridTemplate({
            item: item,
            devopsToolsTypeTrans: {1:'常用命令',2:'上传文件',3:'远程文件',4:'shell脚本',5:'自定义'}
          }));
        }.bind(this))
      }
    },
    loadMore: function() {
      console.log("loadMore");
      this.showList(10, $('tbody tr').length);
    },
    onScroll: function(e) {
      if ($('.scrollable').scrollTop() + $('.scrollable').height() >= $('.scrollable .command_set_list').height()) {
        console.log("bottom!");
        this.loadMore();
      }
    }
  })
  module.exports = Screen;
