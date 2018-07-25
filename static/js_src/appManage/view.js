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
      this.name = "";
      // $('.scrollable').scroll(this.onScroll.bind(this));
      $('.scrollable').scroll(_.debounce(this.onScroll.bind(this), 1000));
      window.YUMEVENTS.on("loadmore", this.loadMore.bind(this));
      this.showJobList();
      // $('.job_list_container').height(window.innerHeight - 200);
      // $('.job_list_container').height(650);
    },
    search: function(e){
      this.name = $('input#name').val();
      $('.scrollable tbody').empty();
      this.showJobList();
      e.preventDefault();
      e.stopPropagation();
    },
    showJobList: function(limit, offset) {
      this.model.getJobList(this.name, this.userId, limit, offset, 1).then(function(res) {
        var model = this.model;
        this.appendToGrid({
          results: res.results
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
          $('.scrollable tbody').append(gridTemplate({
            item: item
          }));
        }.bind(this))
      }
    },
    loadMore: function() {
      console.log("loadMore");
      this.showJobList(10, $('tbody tr').length);
    },
    onScroll: function(e) {
      if ($('.scrollable').scrollTop() + $('.scrollable').height() >= $('.scrollable .job_list').height()) {
        console.log("bottom!");
        this.loadMore();
      }
    }



  })
  module.exports = Screen;
