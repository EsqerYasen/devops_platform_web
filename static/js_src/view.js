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
  var menuListItem = require('./templates/partials/list_menu.ejs');

  var gridItem = require('./templates/partials/grid_row.ejs');

  var commonAddTemplate = require('./templates/partials/modal_common_add.ejs');
  var commonCreateTemplate = require('./templates/partials/modal_common_create.ejs');


  var selectAddSelectTemplate = require('./templates/partials/modal_add_sub_template.ejs');
  var selectAddInputAndSelectTemplate = require('./templates/partials/modal_add_input_sub_template.ejs');
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
      window.YUMEVENTS.on("closeModal", this.closeModal.bind(this));
      // $('#yumModal').modal({show: false});
    },
    closeModal: function() {
      $('#yumModal').modal('hide');
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
        case "modules_for_user_group":
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
              valField: "name",
              keyField: "id",
            });
          })
          break;
        case "add_moudle_groupModules_module":
          // this.prepareModalUserGroups(btn.data());
          this.prepareAddModalModuleGroupModules(btn.data());

          $.when(this.model.getModules()).then(function(modules) {
            dfd.resolve({
              type: type,
              list: modules,
              valField: "alias",
              keyField: "id",
              disable_privilege: true
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
              disable_privilege: true
            });
          })
          break;
        case "create_moduleGroup":
          this.prepareCreateModalModuleGroup(btn.data());
          $.when(this.model.getUsers()).then(function(users) {
            dfd.resolve({
              type: type,
              list: users,
              selectTitle: "管理员",
              inputTitle: "模块组名",
              valField: "username",
              keyField: "id",
            });
          })
          break;
        case "create_module":
          this.prepareCreateModalModule(btn.data());
          $.when(this.model.getUsers()).then(function(users) {
            dfd.resolve({
              type: type,
              list: users,
              selectTitle: "管理员",
              inputTitle: "模块名",
              inputTitle2: "模块别名",
              inputTitle3: "模块URL",
              inputTitle4: "数据库名称",
              inputTitle5: "数据表名称",
              inputTitle6: "数据记录ID",
              valField: "username",
              keyField: "id",
              disable_privilege: true
            });
          })
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

          case "add_moudle_user":
          case "add_moudle_user_group":
          case "add_moudle_moduleGroups":
            // case "create_moduleGroup":
            $('.yumModal .modal-body').html(selectAddSelectTemplate(data));
            break;
          case "create_moduleGroup":
            $('.yumModal .modal-body').html(selectAddInputAndSelectTemplate(data));
            break;
          case "add_moudle_groupModules_user":
            $('.yumModal .modal-body').html(selectAddSelectTemplate(data));
            break;
          case "create_module":
            $('.yumModal .modal-body').html(selectAddInputAndSelectTemplate(data));
            break;
          default:
            break;
        }
        this.showModal();
      }.bind(this))

    },

    doGgetUserModules: function(userId) {
      return this.model.getUserModules({
        id: userId ? userId : -1
      }).then(function(items) {
        this.showUserModules(items, userId)
      }.bind(this))

    },
    doGetUserGroupModules: function(groupid) {
      return this.model.getUserGroupModules({
        id: groupid
      }).then(function(items) {
        this.showUserGroupModules(items, groupid)
      }.bind(this));
    },
    doGetModules: function(groupid) {
      this.model.getModules({}).then(function(items) {
        this.showModules(items, groupid)
      }.bind(this));
    },
    doGetModuleGroups: function(groupid, type) {
      this.model.getModuleGroups({
        id: groupid,
        type: type
      }).then(function(items) {
        this.showModuleGroupModules(items, groupid, type)
      }.bind(this));
    },
    doGetModuleUsers: function(moduleid) {
      this.model.getModuleUsers({
        id: moduleid

      }).then(function(items) {
        this.showModuleUsers(items, moduleid)
      }.bind(this));
    },
    doGetModulesUserGroups: function(moduleid) {
      this.model.getModulesUserGroups({
        id: moduleid
      }).then(function(items) {
        this.showModuleUserGroups(items, moduleid)
      }.bind(this));
    },
    doGetModulesModuleGroups: function(moduleid) {
      this.model.getModulesModuleGroups({
        id: moduleid,
        type: 'module_id'
      }).then(function(items) {
        this.showModuleModuleGroups(items, moduleid)
      }.bind(this));
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
      this.model.addToModel(param).then(function() {
        console.log('removed', param)
      });
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
      this.model.createModel(param).then(function() {
        console.log('created', param)
      });
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
      this.model.removeModel(param).then(function() {
        console.log('removed', param)
        switch (param.type) {
          case "moduleGroup_modules":
            this.doGetModuleUsers(param.item.module_id);
            break;
          default:
            break;
        }
      }.bind(this));
    },
    checkModalHasError: function() {
      return $('.modal .alert').length > 0;
    },
    handleChange: function(e) {
      var privilege = $('.yumModal .btn-group input:checked').val();
      if ($(e.target).hasClass('create')) {
        return;
      }
      var inputs = $('.modal input.select_name:visible');
      var item;
      for (var i = 0; i < inputs.length; i++) {
        item = inputs[i];
        if ($(item).val() === "") {
          $(item).closest('.input').find('.modal_error_msg').addClass('alert alert-danger');
        } else {
          $(item).closest('.input').find('.modal_error_msg').removeClass('alert alert-danger');
        }
      }

      // if ($('.modal input.select_name:visible').length) {
      //   if ($('.modal input.select_name:visible').length && $.trim($('.modal input.select_name:visible').val()) === "") {
      //     $('.modal .input .modal_error_msg').addClass('alert alert-danger');
      //   } else {
      //     $('.modal .input .modal_error_msg').removeClass('alert alert-danger');
      //   }
      // }

      if ($('.modal select.select_module:visible').length) {
        if ($('.modal select.select_module:visible').length && parseInt($('.modal select.select_module:visible').val()) === -1) {
          $('.modal .select .modal_error_msg').addClass('alert alert-danger');
        } else {
          $('.modal .select .modal_error_msg').removeClass('alert alert-danger');
        }
      }
      if ($('.modal .privilege input[type="radio"]:visible').length) {
        if ($('.modal .privilege input[type="radio"]:checked').length) {
          $('.btn-privilege  .modal_error_msg').removeClass('alert alert-danger');
        } else {
          $('.btn-privilege  .modal_error_msg').addClass('alert alert-danger');
        }
      }
      if (this.checkModalHasError()) {
        return;
      }
      var id = $(e.target).data('id');
      var type = $(e.target).data('type');
      var targetId = $(e.target).data('targetId');
      var targetType = $(e.target).data('targetType');
      var selectionVal = $('.modal select').val();
      var inputVal = $('.modal input.inputTitle').val();
      var param = {
        privilege: privilege,
        id: id,
        type: type,
        targetId: targetId,
        targetType: targetType,
        routingid: $(e.target).data('routingid'),
        item: $(e.target).data('item'),
        selectionVal: $('.modal select').val(),
        inputVal: $('.modal input.inputTitle').val(),
        inputVal2: $('.modal input.inputTitle2').val(),
        inputVal3: $('.modal input.inputTitle3').val(),
        inputVal4: $('.modal input.inputTitle4').val(),
        inputVal5: $('.modal input.inputTitle5').val(),
        inputVal6: $('.modal input.inputTitle6').val()

      }
      this.model.updateModel(param).then(function(res) {
        console.log('handleChange---', res, param, "updateModel");
        this.updateResult(res, param.type, "updateModel", param);
      }.bind(this));
    },
    updateResult: function(res, type, source, param) {


      console.log("updateResult", res, type, source, param);

      // window.location.reload();
      var nextAction = source + '_' + type;

      console.log('nextAction', nextAction);
      //showModules
      switch (nextAction) {
        case "updateModel_add_moudle_groupModules_module":
          this.doGetUserGroupModules(res.info.group_id, param.id);
          break;
        case "updateModel_create_moduleGroup":
          break;
        case "updateModel_create_module":
          this.doGetModules();
          break;
        case "updateModel_add_moudle_user":
          this.doGetModuleUsers(param.module_id);
          break;
        case "updateModel_add_moudle_user_group":
          this.doGetModulesUserGroups(res.info.module_id);
          break;
        case "updateModel_add_moudle_moduleGroups":
          this.doGetModulesModuleGroups(param.id);
          // doGetModuleGroups(groupid, type)
          break;
        case "updateModel_add_moudle_groupModules_user":
          this.doGetModuleGroups(res.info.group_id, 'user');
          break;
        case "updateModel_add_module":
          this.doGetUserGroupModules(res.info.group_id);
          break;
        default:
          break;
          //doGetUserGroupModules
      }
      return

    },

    showModalAddTouserGroup: function() {
      $('.yumModal .modal-title').text('添加模块');
      $('.yumModal .modal-body').html(
        selectAddSelectTemplate({}));
      this.showModal();
    },
    prepareCreateModalModuleGroup: function(data) {
      $('.yumModal .modal-title').text('创建模块组');
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type).data("routingid", data.routingid).data('item', data.item);

    },
    prepareCreateModalModule: function(data) {
      $('.yumModal .modal-title').text('创建模块');
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type).data("routingid", data.routingid).data('item', data.item);

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
        case "modules_for_user_group":
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
          diable_privilege: true
        }
      }));
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type);
    },

    prepareAddModalModuleGroupModules: function(data) {
      $('.yumModal .modal-title').text("添加模块");
      $('.yumModal .modal-body').html(modalEditCommonTemplate({
        data: {
          privilege: data.privilege,
          diable_privilege: true,
          name: data.name,
          hidden: '.privilege'
        }
      }));
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type);
    },
    prepareModalUserGroups: function(data) {
      $('.yumModal .modal-title').text("编辑用户组");
      $('.yumModal .modal-body').html(modalEditCommonTemplate({
        data: data
      }));
      $('.yumModal.modal button.save').data("id", data.id).data("type", data.type).data("item", data.item);
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
        $('.yumModal .hide').removeClass('hide');
      });
      $('.yumModal').modal('show');
    },
    loadMore: function(type) {
      // if (!(window.app && window.app.routes && window.app.routes[Backbone.history.getFragment()])) {
      //   return;
      // }
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
        grid_type: "modules_for_user_group",
        buttons: [
          /*        {
                    kls: "add_modal",
                    text: "添加用户",
                    id: groupid,
                    type: "add_user"

                  },
                  */
          {
            kls: "add_modal",
            text: "添加模块",
            id: groupid,
            type: "add_module"
          }
          /*        , {
                    kls: "create_modal",
                    text: "新建用户组",
                    id: groupid,
                    type: "create_user_group"
                  }*/
        ]
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
        moduleId: moduleId,
        buttons: [{
          kls: "add_modal",
          text: "添加用户",
          id: moduleId,
          type: "add_moudle_user"
        },{
          kls: "add_modal",
          text: "新建模块组",
          id: -1,
          type: "create_moduleGroup"
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
        buttons: [{
          kls: "add_modal",
          text: "新建模块",
          id: -1,
          type: "create_module"
        }]
      })
      console.log("showModules");
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
        list: [],
        buttons: [{
          kls: "add_modal",
          text: "新建模块组",
          id: -1,
          type: "create_moduleGroup"
        }]
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
    checkIsOwner: function(data) {
      var isOwner = false;
      switch (data.grid_type) {
        case "module_users":
          var module = this.model.getItemByIdFromCache('modules', data.moduleId, true);
          if (module && module.owner_id == this.userInfo.userid) {
            isOwner = true;
          }
          break;
        default:
          break;
      }
      console.log('checkIsOwner', data, this.userInfo);
      return isOwner;
    },
    updateList: function(data) {
      $(this.el).find('.list').html(listTemplate(data));
    },
    appendList: function(data) {
      $(this.el).find('.list .list-group').append(menuListItem(data));
    },
    appendGrid: function(data) {
      $(this.el).find('.data-grid').data('recentData');
      $(this.el).find('.data-grid table tbody').append(
        gridItem(
          $.extend({
            isOwner: this.checkIsOwner($(this.el).find('.data-grid').data('recentData'))
          }, data)
        )
      );
      //
      //{"id":4,"user_id":1,"name":"1312","module_id":1,"owner_id":1,"privilege":1}
      console.log('appendGrid', data);
      // data = _.extend({
      //   modalEditTitle: "",
      //   tabs: [],
      //   userInfo: this.userInfo,
      //   buttons: []
      // }, data);
      // $(this.el).find('.data-grid').empty();
      // $(this.el).find('.data-grid').html(gridTemplate(data));
    },
    updateGrid: function(data) {
      data = _.extend({
        modalEditTitle: "",
        tabs: [],
        userInfo: this.userInfo,
        isOwner: this.checkIsOwner(data),
        buttons: []
      }, data);
      $(this.el).find('.data-grid').empty();
      $(this.el).find('.data-grid').html(gridTemplate(data));
      $(this.el).find('.data-grid').data('recentData', data);
    }
  })
  module.exports = Screen;
