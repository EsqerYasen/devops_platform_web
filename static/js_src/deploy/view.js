  var Backbone = require('backbone');
  Backbone.$ = exports.$ = window.jQuery;
  var _ = require('underscore');
  var config = require('../config.json');
  // var listTemplate = require('./templates/list.ejs');
  // var gridTemplate = require('./templates/grid.ejs');
  window.YUMEVENTS = _.extend({}, Backbone.Events);
  var gridTemplate = require('./templates/partials/grid.ejs');
  // var modalEditUserTemplate = require('./templates/partials/modal_edit_user.ejs');
  // var modalEditModuleGroupTemplate = require('./templates/partials/modal_module_group.ejs');
  // var modalEditUserGroupTemplate = require('./templates/partials/modal_user_group.ejs');
  // var modalEditCommonTemplate = require('./templates/partials/modal_modify_privilege.ejs');
  // var menuListItem = require('./templates/partials/list_menu.ejs');

  // var gridItem = require('./templates/partials/grid_row.ejs');

  // var commonAddTemplate = require('./templates/partials/modal_common_add.ejs');
  // var commonCreateTemplate = require('./templates/partials/modal_common_create.ejs');


  // var selectAddSelectTemplate = require('./templates/partials/modal_add_sub_template.ejs');
  // var selectAddInputAndSelectTemplate = require('./templates/partials/modal_add_input_sub_template.ejs');
  // var buttonTemplate = require('./templates/partials/menu_button.ejs');

  var Screen = Backbone.View.extend({
    el: '.wrapper-content',
    userInfo: false,
    model: false,
    permssions: [],
    events: {
      'click .btn-primary.search': 'search'
    },
    initialize: function(user, userId, model) {

      console.log('view inited');
      this.userInfo = user;
      this.model = model;
      this.userId = userId;
      $('.scrollable').scroll(this.onScroll.bind(this));
      window.YUMEVENTS.on("loadmore", this.loadMore.bind(this));
      window.YUMEVENTS.on("closeModal", this.closeModal.bind(this));
      this.showJobList();
      // $('.job_list_container').height(650);
      // $('.scrollable').height(650);

      // $('#yumModal').modal({show: false});
    },
    search: function(e){
      this.name = $('input#name').val();
      $('.scrollable tbody').empty();
      this.showJobList();
      e.preventDefault();
      e.stopPropagation();
    },
    showJobList: function(limit, offset) {
      this.model.getJobList(this.name, this.userId, limit, offset).then(function(res) {
        var ids = []
        $(res.results).map(function(i, _item) {
          ids.push(_item.id);
        });
        var model = this.model;
        var self = this;
        this.model.getVersionLists(ids).then(function(versions) {
          console.log('res.results', res.results);
          console.log('versions', versions);
          self.appendToGrid({
            results: res.results,
            versions: versions.results,
          });
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
          val = 0;
          $.each(permissions, function(_i, perm) {
            if (perm.idx === item.id) {
              val = Math.max(val, perm.value);
            }

          })
          $('.job_list tbody').append(gridTemplate({
            item: item,
            versions: this.geToolsVersionsById(item.id, versions),
            permission: val
          }));
        }.bind(this))
      }
    },
    geToolsVersionsById: function(toolId, versions) {
      var found = [];
      $.each(versions, function(i, version) {
        if (version.deploy_tool_id - toolId === 0) {
          found.push(version);
        }
      });
      return found;
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
    },
    closeModal: function() {
      $('#yumModal').modal('hide');
    },
    showModalCreate: function(e) {

    },

    doGetUserGroupModules: function(groupid) {
    },

    checkIsOwner: function(data) {

    },
    updateList: function(data) {
    },
    appendList: function(data) {
    },
    appendGrid: function(data) {

    },
    updateGrid: function(data) {

    }
  })
  module.exports = Screen;
