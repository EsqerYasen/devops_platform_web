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
      'click .appIcon:not(.disabled)': 'onAppItemClick',
      'click .notification': 'onNotificationClick',
      'click .hmi_clickable:not(.disabled)': 'onHmiClick',
      'click .back': 'handleBack',
      'click .setting_list .setting_li': 'onSettingLiClick',
      'click .setting_list .setting_buttons .hmi_button:not(.no_show)': 'onSettingButtonClick',
      'click .scroll:not(.inactive)': 'handScrollButton',
      'click .btn_edit': 'showModalEdit',
      'click .btn_remove': 'showModalRemove',
      'click .modal_userGroup_add_module': 'showModalAddTouserGroup',
      'click button.save.create': "handleCreate",
      'click button.save': "handleChange",
      'click input.btn_remove': "handleRemove",
      'click button.add_modal': "showModalAdd",
      'click button.create_modal': "showModalCreate",
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
      $('.job_list_container').height(window.innerHeight - 200);

      // $('#yumModal').modal({show: false});
    },
    showJobList: function(limit, offset) {
      this.model.getJobList(this.userId, limit, offset).then(function(res) {
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
      console.log(111111111);
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
      // $('.scrollable >table')
      if ($('.scrollable').scrollTop() + $('.scrollable').height() >= $('.scrollable .job_list').height()) {
        console.log("bottom!");
        this.loadMore();
      }
    },
    closeModal: function() {
      $('#yumModal').modal('hide');
    },
    //commonCreateTemplate
    showModalCreate: function(e) {

    },

    doGetUserGroupModules: function(groupid) {
      // return this.model.getUserGroupModules({
      //   id: groupid
      // }).then(function(items) {
      //   this.showUserGroupModules(items, groupid)
      // }.bind(this));
    },

    checkIsOwner: function(data) {
      // var isOwner = false;
      // switch (data.grid_type) {
      //   case "module_users":
      //     var module = this.model.getItemByIdFromCache('modules', data.moduleId, true);
      //     if (module && module.owner_id == this.userInfo.userid) {
      //       isOwner = true;
      //     }
      //     break;
      //   default:
      //     break;
      // }
      // console.log('checkIsOwner', data, this.userInfo);
      // return isOwner;
    },
    updateList: function(data) {
      // $(this.el).find('.list').html(listTemplate(data));
    },
    appendList: function(data) {
      // $(this.el).find('.list .list-group').append(menuListItem(data));
    },
    appendGrid: function(data) {
      // $(this.el).find('.data-grid').data('recentData');
      // $(this.el).find('.data-grid table tbody').append(
      //   gridItem(
      //     $.extend({
      //       isOwner: this.checkIsOwner($(this.el).find('.data-grid').data('recentData'))
      //     }, data)
      //   )
      // );
    },
    updateGrid: function(data) {
      // data = _.extend({
      //   modalEditTitle: "",
      //   tabs: [],
      //   userInfo: this.userInfo,
      //   isOwner: this.checkIsOwner(data),
      //   buttons: []
      // }, data);
      // $(this.el).find('.data-grid').empty();
      // $(this.el).find('.data-grid').html(gridTemplate(data));
      // $(this.el).find('.data-grid').data('recentData', data);
    }
  })
  module.exports = Screen;
