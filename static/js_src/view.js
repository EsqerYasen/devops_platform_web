  var Backbone = require('backbone');
  Backbone.$ = exports.$ = window.jQuery;
  var _ = require('underscore');

  var listTemplate = require('./templates/list.ejs');
  var gridTemplate = require('./templates/grid.ejs');
  window.YUMEVENTS = _.extend({}, Backbone.Events);
  var modalEditUserTemplate = require('./templates/partials/modal_edit_user.ejs');
  var modalEditModuleGroupTemplate = require('./templates/partials/modal_module_group.ejs');
  var modalEditUserGroupTemplate = require('./templates/partials/modal_user_group.ejs');
  var modalEditCommonTemplate = require('./templates/partials/modal_modify_privilege.ejs');
  var commonAddTemplate = require('./templates/partials/modal_common_add.ejs');
  var commonCreateTemplate = require('./templates/partials/modal_common_create.ejs');


  var selectAddSelectTemplate = require('./templates/partials/modal_add_sub_template.ejs');
  var buttonTemplate = require('./templates/partials/menu_button.ejs');

  var Screen = Backbone.View.extend({
    el: '.app',
    userInfo: false,
    model: false,
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
    initialize: function(user, model) {
      console.log('view inited');
      this.userInfo = user;
      this.model = model;
      $('.cotainer').scroll(this.onScroll.bind(this));
      window.YUMEVENTS.on("loadmore", this.loadMore.bind(this));
      // $('#yumModal').modal({show: false});
    },
    //commonCreateTemplate
    showModalCreate: function(e) {
      console.log(e.currentTarget);
      var btn = $(e.currentTarget);
      var type = btn.data('type');
      var dfd = $.Deferred();
      switch (type) {

        case "create_user_group":
          this.prepareCreateModal(btn.data());
          $.when(this.model.getUsers()).then(function(users) {
            dfd.resolve({
              type: type,
              list: users,
              valField: "username",
              keyField: "id",
              list_name: "select_admin",
              list_kls: "select_admin",
              list_label: "管理员",
              text_name: "group_name",
              text_kls: "group_name",
              text_label: "用户组名"

            });
          })
          break;
        case "add_module":
          this.prepareCreateModal(btn.data());
          $.when(this.model.getModules()).then(function(modules) {
            dfd.resolve({
              type: type,
              list: modules,
              valField: "alias",
              keyField: "id",
            });
          })
          break;
        default:
          // this.debug1(btn.data('edittitle'));
          break;
      }

      // this.showModal(this.debug1, btn.data('edittitle'));
      $.when(dfd).then(function(data) {
        switch (data.type) {
          case "create_user_group":
          case "add_module":
            $('.yumModal .modal-body').html(commonCreateTemplate(data));
            break;
          default:
            break;
        }
        this.showModal();
      }.bind(this))
    },
    showModalAdd: function(e) {
      var btn = $(e.currentTarget);
      var type = btn.data('type');
      console.log(type);
      var dfd = $.Deferred();
      switch (type) {
        case "module_moduleGroups":
        case "add_moudle_moduleGroups":
          var moduleName = btn.data('name');
          this.prepareModalModuleGroups(btn.data());

          $.when(this.model.getModuleGroups()).then(function(groups) {
            dfd.resolve({
              type: type,
              list: groups,
              valField: "name",
              keyField: "id",
            });
          })
          break;
        case "module_user_groups":
        case "user_module_groups":
        case "add_moudle_user_group":
          this.prepareModalUserGroups(btn.data());
          $.when(this.model.getSysUserGroups()).then(function(groups) {
            dfd.resolve({
              type: type,
              list: groups,
              valField: "name",
              keyField: "id",
            });
          })
          break;
        case "add_user":
        case "add_moudle_user":
          this.prepareAddModal(btn.data());
          $.when(this.model.getUsers()).then(function(users) {
            dfd.resolve({
              type: type,
              list: users,
              valField: "username",
              keyField: "id",
            });
          })
          break;
        case "add_module":
          this.prepareAddModal(btn.data());
          $.when(this.model.getModules()).then(function(modules) {
            dfd.resolve({
              type: type,
              list: modules,
              valField: "alias",
              keyField: "id",
            });
          })
          break;
        case "add_moudle_groupModules_module":
          // this.prepareModalUserGroups(btn.data());
          this.prepareAddModalModuleGroupModules(btn.data())
          $.when(this.model.getModules()).then(function(modules) {
            dfd.resolve({
              type: type,
              list: modules,
              valField: "alias",
              keyField: "id",
            });
          })
          break;
        case "add_moudle_groupModules_user":
          this.prepareAddModalModuleGroupUsers(btn.data());
          $.when(this.model.getUsers()).then(function(users) {
            dfd.resolve({
              type: type,
              list: users,
              valField: "username",
              keyField: "id",
            });
          })
          break;
        default:
          // this.debug1(btn.data('edittitle'));
          break;
      }

      // this.showModal(this.debug1, btn.data('edittitle'));
      $.when(dfd).then(function(data) {
        switch (data.type) {
          case "add_user":
          case "add_module":
          case "add_moudle_groupModules_module":
          case "add_moudle_groupModules_user":
          case "add_moudle_user":
          case "add_moudle_user_group":
          case "add_moudle_moduleGroups":
            $('.yumModal .modal-body').html(selectAddSelectTemplate(data));
            break;
          default:
            break;
        }
        this.showModal();
      }.bind(this))

    },
    handleAdd: function(e) {
      var id = $(e.target).data('id');
      var type = $(e.target).data('type');
      var targetId = $(e.target).data('targetId');
      var targetType = $(e.target).data('targetType');
      var param = {
        id: id,
        type: type,
        targetId: targetId,
        targetType: targetType
      }
      this.model.addToModel(param);
    },
    handleCreate: function(e) {
      // e.preventdefault();
      var id = $(e.target).data('id');
      var type = $(e.target).data('type');
      var targetId = $(e.target).data('targetId');
      var targetType = $(e.target).data('targetType');
      var param = {
        id: id,
        type: type,
        targetId: targetId,
        targetType: targetType,
        name: $('.modal input[name="group_name"]').val(),
        admin: $('.modal select[name="select_admin"]').val(),
      }
      this.model.createModel(param);
    },
    handleRemove: function(e) {
      var id = $(e.target).data('id');
      var type = $(e.target).data('type');
      var targetId = $(e.target).data('targetId');
      var targetType = $(e.target).data('targetType');
      var param = {
        id: id,
        type: type,
        targetId: targetId,
        targetType: targetType,
        item: $(e.target).data('item')
      }
      this.model.removeModel(param);
    },
    handleChange: function(e) {
      var privilege = $('.yumModal .btn-group input:checked').val();
      if ($(e.target).hasClass('create')) {
        return;
      }
      var id = $(e.target).data('id');
      var type = $(e.target).data('type');
      var targetId = $(e.target).data('targetId');
      var targetType = $(e.target).data('targetType');
      var param = {
        privilege: privilege,
        id: id,
        type: type,
        targetId: targetId,
        targetType: targetType,
        routingid: $(e.target).data('routingid'),
        item: $(e.target).data('item'),
      }
      this.model.updateModel(param);
    },
    showModalAddTouserGroup: function() {
      $('.yumModal .modal-title').text('添加模块');
      $('.yumModal .modal-body').html(
        selectAddSelectTemplate({
          modules: [{
            id: 1,
            name: '123'
          }]
        }));
      this.showModal();
    },
    prepareAddModalUser: function(modalTitle) {
      $('.yumModal .modal-title').text('添加用户');
      $('.yumModal .modal-body').html(
        commonAddTemplate({
          modules: [{
            id: 1,
            name: '123'
          }]
        }));
      this.showModal();
    },
    prepareAddModal: function(data) {
      $('.yumModal .modal-title').text(data.text);
      $('.yumModal .modal-body').html("");
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type);
      // this.showModal();

    },
    prepareCreateModal: function(data) {
      $('.yumModal .modal-title').text(data.text);
      $('.yumModal .modal-body').html("");
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type).addClass("create");
      // this.showModal();

    },
    showModalRemove: function(data) {


      // if (!(window.app && window.app.routes && window.app.routes[Backbone.history.getFragment()])) {
      //   return;
      // }
      // var routing = window.app.routes[Backbone.history.getFragment()];
      // switch (routing){
      //   case 'load_user':

      // }
      // console.log(routing-      // this.showModal(this.debug2);
    },
    showModalEdit: function(e) {
      var btn = $(e.currentTarget);
      var type = btn.data('type');
      switch (type) {
        case "module_moduleGroups":
          var moduleName = btn.data('name');
          this.prepareModalModuleGroups(btn.data());
          break;
        case "module_user_groups":
        case "user_module_groups":
          this.prepareModalUserGroups(btn.data());
          break;
        case "module_users":
        case "user_modules":
          this.prepareModalUser(btn.data());
          break;
        default:
          this.debug1(btn.data('edittitle'));
          break;
      }

      // this.showModal(this.debug1, btn.data('edittitle'));
      // this.showModal();
      this.showModal();

    },
    prepareModalUser: function(data) {
      $('.yumModal .modal-title').text("编辑用户");
      $('.yumModal .modal-body').html(modalEditCommonTemplate({
        data: $.extend({
          privilege: data.privilege,
          name: data.name,
        }, data)
      }));
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type).data("routingid", data.routingid).data('item', data.item);
    },
    prepareAddModalModuleGroupUsers: function(data) {
      $('.yumModal .modal-title').text("添加用户");
      $('.yumModal .modal-body').html(modalEditCommonTemplate({
        data: {
          privilege: data.privilege,
          name: data.name,
        }
      }));
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type);
    },

    prepareAddModalModuleGroupModules: function(data) {
      $('.yumModal .modal-title').text("添加模块");
      $('.yumModal .modal-body').html(modalEditCommonTemplate({
        data: {
          privilege: data.privilege,
          name: data.name,
        }
      }));
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type);
    },
    prepareModalUserGroups: function(data) {
      $('.yumModal .modal-title').text("编辑用户组");
      $('.yumModal .modal-body').html(modalEditCommonTemplate({
        data: {
          privilege: data.privilege,
          name: data.name,
        }
      }));
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type);
    },

    prepareModalModuleGroups: function(data) {
      $('.yumModal .modal-title').text("编辑模块组");
      $('.yumModal .modal-body').html(modalEditCommonTemplate({
        data: {
          privilege: data.privilege,
          name: data.name,
        }
      }));
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type);
    },
    debug1: function(modalTitle) {
      // if (!(window.app && window.app.routes && window.app.routes[Backbone.history.getFragment()])) {
      //   return;
      // }
      // var routingTo = window.app.routes[Backbone.history.getFragment()];
      $('.yumModal .modal-title').text(modalTitle);
      $('.yumModal .modal-body').html(modalEditUserTemplate({
        user: {
          privilege: 4,
          name: "user" + Math.round(Math.random() * 1000),
          moduleName: "moduleName" + Math.round(Math.random() * 1000)
        }
      }));
      console.log(111111);
    },
    debug2: function() {
      console.log(222222);
    },
    showModal: function() {
      $('.yumModal').off();
      $('.yumModal').on('hide.bs.modal', function() {
        $('.yumModal .button.save').removeData('action').removeClass("create").addClass("save");
      });
      $('.yumModal').modal('show');
    },
    loadMore: function(type) {
      if (!(window.app && window.app.routes && window.app.routes[Backbone.history.getFragment()])) {
        return;
      }
      var loadType = window.app.routes[Backbone.history.getFragment()];
      switch (loadType) {
        case "load_user":
          break;
        case "load_user_group":
          break;
        case "load_modulegroup":
          break;
        case "load_module_users":
          break;
        case "load_module_user_groups":
          break;
        case "load_module_groups":
          break;
        default:
          break;
      }

      console.log('loadMore', type, window.app.routes[Backbone.history.getFragment()]);
      //      window.YUMEVENTS.on("loadmore", function(arg){console.log(11111111, arg);});


    },
    changeTitle: function(title, isRemove) {
      if (title) {
        $('.cotainer_title').text(title);
      } else {
        if (isRemove) {
          $('.cotainer_title').empty();
        }
      }
    },
    showButtons: function(title, isRemove, refId) {
      console.log('showButtons', title);
      $('.cotainer .buttons').empty();
    },
    showUserModules: function(data, userId) {
      this.changeTitle("showUserModules");
      this.showButtons("showUserModules");
      this.updateGrid({
        list: data || [],
        modalEditTitle: "模块权限",
        grid_type: "user_modules",
        routingid: userId
      });

      console.log("showUserModules", data)
    },
    showUserGroupModules: function(items, groupid) {
      this.changeTitle("showUserGroupModules");
      this.showButtons("showUserGroupModules");
      this.updateGrid({
        list: items,
        grid_type: "user_module_groups",
        buttons: [{
          kls: "add_modal",
          text: "添加用户",
          id: groupid,
          type: "add_user"

        }, {
          kls: "add_modal",
          text: "添加模块",
          id: groupid,
          type: "add_module"
        }, {
          kls: "create_modal",
          text: "新建用户组",
          id: groupid,
          type: "create_user_group"
        }]
      });
      // this.updateGrid({
      //   list: []
      // })
      console.log("    showUserGroupModules")
    },
    showModuleGroupModules: function(items, groupid, type) {
      this.changeTitle("showModuleGroupModules");
      this.showButtons("showModuleGroupModules");
      // $(this.el).find('.list').html(listTemplate({route_to:"module", list:items}));
      // $(this.el).find('.data-grid').html(gridTemplate({list:items}));
      // this.updateList({route_to:"usergroup", list:items});

      this.updateGrid({
        tabs: [{
            id: "user",
            text: "用户",
            active: type === "user" ? true : false,
            route_to: "modulegroup/" + groupid + "/type_user"
          }, {
            id: "module",
            text: "模块",
            active: type === "module" ? true : false,
            route_to: "modulegroup/" + groupid + "/type_module"
          }

        ],
        list: items,
        no_privilege: true,
        no_edit: true,
        grid_type: "moduleGroup_modules",
        buttons: [{
          kls: "add_modal",
          text: type === "module" ? "添加模块" : "添加用户",
          id: groupid,
          type: "add_moudle_groupModules_" + type
        }]
      });
      console.log("    showModuleGroupModules")
    },
    showModuleUsers: function(items, moduleId) {
      this.changeTitle("showModuleUsers");
      this.showButtons("showModuleUsers");
      // $(this.el).find('.list').html(listTemplate({route_to:"module", list:items}));
      // $(this.el).find('.data-grid').html(gridTemplate({route_to:"usergroup", list:items}));
      // this.updateList({route_to:"module", list:items});
      this.updateGrid({
        list: items,
        grid_type: "module_users",
        tabs: [{
            id: "user",
            text: "用户",
            active: true,
            route_to: "/modules/" + moduleId + "/user"
          }, {
            id: "user_group",
            text: "用户组",
            active: false,
            route_to: "/modules/" + moduleId + "/usergroup"
          }, {
            id: "module_group",
            text: "模块组",
            active: false,
            route_to: "/modules/" + moduleId + "/modulegroup"
          }

        ],
        buttons: [{
          kls: "add_modal",
          text: "添加用户",
          id: moduleId,
          type: "add_moudle_user"
        }]
      });
      console.log("    showModuleUsers")
    },
    showModuleUserGroups: function(items, moduleId) {
      this.changeTitle("showModuleUserGroups");
      this.showButtons("showModuleUserGroups");
      // $(this.el).find('.list').html(listTemplate({route_to:"module", list:items}));
      // $(this.el).find('.data-grid').html(gridTemplate({route_to:"usergroup", list:items}));
      // this.updateList({route_to:"module", list:items});
      this.updateGrid({
        list: items,
        grid_type: "module_user_groups",
        tabs: [{
            id: "user",
            text: "用户",
            active: false,
            route_to: "/modules/" + moduleId + "/user"
          }, {
            id: "user_group",
            text: "用户组",
            active: true,
            route_to: "/modules/" + moduleId + "/usergroup"
          }, {
            id: "module_group",
            text: "模块组",
            active: false,
            route_to: "/modules/" + moduleId + "/modulegroup"
          }

        ],
        buttons: [{
          kls: "add_modal",
          text: "添加用户组",
          id: moduleId,
          type: "add_moudle_user_group"
        }]
      });
      console.log("    showModuleUserGroups")
    },
    showModuleModuleGroups: function(items, moduleId) {
      this.changeTitle("showModuleModuleGroups");
      this.showButtons("showModuleModuleGroups");
      // $(this.el).find('.list').html(listTemplate({route_to:"module", list:items}));
      // $(this.el).find('.data-grid').html(gridTemplate({route_to:"usergroup", list:items}));
      // this.updateList({route_to:"module", list:items});
      this.updateGrid({
        list: items,
        grid_type: "module_moduleGroups",
        tabs: [{
            id: "user",
            text: "用户",
            active: false,
            route_to: "/modules/" + moduleId + "/user"
          }, {
            id: "user_group",
            text: "用户组",
            active: false,
            route_to: "/modules/" + moduleId + "/usergroup"
          }, {
            id: "module_group",
            text: "模块组",
            active: true,
            route_to: "/modules/" + moduleId + "/modulegroup"
          }

        ],
        buttons: [{
          kls: "add_modal",
          text: "添加模块组",
          id: moduleId,
          type: "add_moudle_moduleGroups"
        }]
      });
      console.log("    showModuleModuleGroups")
    },
    showInitUserScreen: function(users, modules) {
      this.changeTitle("showInitUserScreen");
      this.showButtons("showInitUserScreen");
      // $(this.el).find('.list').html(listTemplate({route_to:"module", list:items}));
      // $(this.el).find('.data-grid').html(gridTemplate({route_to:"users", list:items}));
      console.log(users)
      this.updateList({
        route_to: "user",
        list: users,
        name_field: 'username',
        key_field: 'id'
      });
      this.updateGrid({
        grid_type: "user_modules",
        list: modules
      });
      console.log("    showInitUserScreen")
    },
    showInitUserGroupScreen: function(groups, items) {
      this.changeTitle("showInitUserGroupScreen");
      this.showButtons("showInitUserGroupScreen");
      // $(this.el).find('.list').html(listTemplate({route_to:"module", list:items}));
      // $(this.el).find('.data-grid').html(gridTemplate({route_to:"usergroups", list:items}));
      this.updateList({
        route_to: "usergroup",
        list: groups,
        name_field: 'name',
        key_field: 'id'

      });
      this.updateGrid({
        grid_type: "user_groups",
        list: items,
        type: "user"
      });
      console.log("    showInitUserGroupScreen")
    },
    showModules: function(modules, groupid, type) {
      var type = "user";
      this.changeTitle("showModuleGroupScreen");
      this.showButtons("showModuleGroupScreen");
      this.updateList({
        route_to: "module_user",
        list: modules,
        name_field: 'name',
        key_field: 'id',
      });
      this.updateGrid({
        grid_type: "dynamic_module_" + type,
        list: [],
        tabs: [],
      })
      console.log("    showModules")
    },
    showModuleGroupScreen: function(groups, modules) {
      this.changeTitle("showModuleGroupScreen");
      this.showButtons("showModuleGroupScreen");
      this.updateList({
        route_to: "modulegroup",
        list: groups,
        name_field: 'name',
        key_field: 'id',
      });
      this.updateGrid({
        grid_type: "modulegroup",
        list: []
      })
      console.log("    showModuleGroupScreen")
    },
    onScroll: function(e) {
      if (e.target.scrollTop === 0) {
        // $('.scroll.icon.up').addClass('inactive');
        if (e.target.offsetHeight + e.target.scrollTop + e.target.offsetTop >= e.target.scrollHeight) {
          // $('.scroll.icon.down').removeClass('inactive');
        }
      } else if (e.target.offsetHeight + e.target.scrollTop >= e.target.scrollHeight) {
        window.YUMEVENTS.trigger('loadmore', Backbone.history.getFragment());
        // $('.scroll.icon.up').removeClass('inactive');
        // $('.scroll.icon.down').addClass('inactive');
      } else {
        // $('.scroll.icon.up, .scroll.icon.down').removeClass('inactive');
      }
    },
    updateList: function(data) {
      $(this.el).find('.list').html(listTemplate(data));
    },
    updateGrid: function(data) {
      data = _.extend({
        modalEditTitle: "",
        tabs: [],
        userInfo: this.userInfo,
        buttons: []
      }, data);
      $(this.el).find('.data-grid').empty();
      $(this.el).find('.data-grid').html(gridTemplate(data));
    }
  })
  module.exports = Screen;