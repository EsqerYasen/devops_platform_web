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
    el: '.app',
    userInfo: false,
    model: false,
    permssions: [],
    events: {
    },
    initialize: function(user, userId, model) {

      console.log('view inited');
      this.model = model;
      this.showMenu();
      // $('#yumModal').modal({show: false});
    },
    showMenu: function(limit, offset) {
      this.model.getUserMenus().then(function(res) {

      }.bind(this));
    },
    appendToGrid: function(param) {
      console.log(111111111);
      // var lists = param.results;
      // var versions = param.versions;
      // var permissions = param.permissions || [];
      // var val = 0;
      // if (lists.length) {
      //   $.each(lists, function(i, item) {
      //     val = 0;
      //     $.each(permissions, function(_i, perm) {
      //       if (perm.idx === item.id) {
      //         val = Math.max(val, perm.value);
      //       }

      //     })
      //     $('.job_list tbody').append(gridTemplate({
      //       item: item,
      //       versions: this.geToolsVersionsById(item.id, versions),
      //       permission: val
      //     }));
      //   }.bind(this))
      // }
    }

  })
  module.exports = Screen;
