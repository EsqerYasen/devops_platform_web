  var Backbone = require('backbone');
  Backbone.$ = exports.$ = window.jQuery;
  var _ = require('underscore');
  var config = require('../config.json');
  // var listTemplate = require('./templates/list.ejs');
  // var gridTemplate = require('./templates/grid.ejs');
  window.YUMEVENTS = _.extend({}, Backbone.Events);
  var gridTemplate = require('./templates/partials/grid.ejs');
  var commonCreateTemplate = require('./templates/partials/modal_common_create.ejs');
  var gridTemplate = require('./templates/partials/grid.ejs');
  var buildDragger = function() {

      $('.can_drag').on("dragstart", function(ev) {
          ev.stopPropagation();
          ev.originalEvent.dataTransfer.setData("item", ev.target.id);
          ev.originalEvent.dataTransfer.setData("data", JSON.stringify($(ev.target).data()));
          $('.draging').removeClass('draging');
          $(ev.target).addClass("draging");
      });
      $('.can_drag').on("dragenter", function(ev) {
          ev.preventDefault();
          ev.stopPropagation();
          console.log('dragenter');
      });
      $('.can_drag').on("dragover", function(ev) {
          ev.preventDefault();
          ev.stopPropagation();
          $('.overlap').removeClass("overlap");
          if ($(ev.target).hasClass('can_drag')) {
              $(ev.target).addClass("overlap");
          } else {
              $(ev.target).closest('.can_drag').addClass("overlap");
          }
      });
      $('.can_drag').on("dragleave", function(ev) {
          $(ev.target).removeClass("overlap");
      });
      $('.can_drag').on("dragend", function(ev) {
          ev.preventDefault();
          $('.overlap').removeClass("overlap");
          $(ev.target).removeClass("draging");
      });
      $('.can_drag').on("drop", function(ev) {
          ev.preventDefault();
          ev.stopPropagation();
          ev.originalEvent.dataTransfer.getData("item");
          ev.originalEvent.dataTransfer.getData("data");
          var row;
          if ($(ev.target).hasClass('can_drag')) {
              row = $(ev.target);
          } else {
              row = $(ev.target).closest('.can_drag');
          }
          var elementId = ev.originalEvent.dataTransfer.getData("item");
          var currentTargetData = row.data(),
              eleData = JSON.parse(ev.originalEvent.dataTransfer.getData("data"));
          if (currentTargetData.parent == eleData.parent && eleData.type === 'sub_menu') {
              $('#' + elementId).insertBefore(row);
              window.YUMEVENTS.trigger('orderChanged', {
                  to: row.data(),
                  from: eleData
              });
          } else {
              if (eleData.type === 'parent') {
                  if (currentTargetData.type === 'sub_menu') {
                      row = row.closest('.menu_section');
                  }
                  $('#' + elementId).insertBefore(row);
                  window.YUMEVENTS.trigger('orderChanged', {
                      to: row.data(),
                      from: eleData
                  });
              }
          }

      });
  }
  var Screen = Backbone.View.extend({
      el: '.menu-app',
      userInfo: false,
      model: false,
      permssions: [],
      events: {
          'click .addMenu': 'addMenu',
          'click .save': 'handleSave',
          'click .menu_row .oper button': 'handleOper'
      },
      initialize: function(user, userId, model) {

          console.log('view inited');
          this.model = model;
          this.showMenu();
          // $('.cotainer').scroll(this.onScroll.bind(this));
          $('.cotainer').scroll(_.debounce(this.onScroll.bind(this), 1000));
          window.YUMEVENTS.on("loadmore", this.loadMore.bind(this));
          window.YUMEVENTS.on("closeModal", this.closeModal.bind(this));
          window.YUMEVENTS.on("orderChanged", this.changeOrder.bind(this));
      },
      onScroll: function() {

      },
      loadMore: function() {

      },
      changeOrder: function(data) {
          this.model.changeOrder({
              from: JSON.stringify(data.from),
              to: JSON.stringify(data.to)
          }).then(function(res) {
              this.showMenu();
          }.bind(this))
      },
      closeModal: function() {
          $('#yumModal').modal('hide');
      },
      handleOper: function(e) {
          var action = $(e.target).data('action');
          var parent = $(e.target).closest('.oper');
          console.log(action, parent.data());
          switch (action) {
              case "edit":
                  this.showEditPopup(parent.data('item'));
                  break;
              case "remove":
                  this.removeMenu(parent.data('id'));
                  break;
          }
      },
      showEditPopup: function(item) {
          this.addMenu(item, "updateMenuItem")
      },
      removeMenu: function(id) {
          this.model.updateMenu({
              id: id,
              is_enabled: 0
          }).then(function(res) {
              this.showMenu();
          }.bind(this))
      },
      createMenu: function() {
          var data = {
              name: $('.menu_name').val(),
              menu: $('.menus_data').val(),
              parentId: $('.parent_menu').val(),
              has_sub: $('.has_sub_menu:checked').val(),
          }
          console.log(data);
          this.model.createMenu(data).then(function(res) {

              this.closeModal();
              this.showMenu();
          }.bind(this))
      },
      updateMenu: function() {
          var data = {
              name: $('.menu_name').val(),
              menu: $('.menus_data').val(),
              parentId: $('.parent_menu').val(),
              has_sub: $('.has_sub_menu:checked').val(),
              id: $('.modal-body .menu').data('id')
          }
          console.log(data);
          this.model.updateMenu(data).then(function(res) {
              this.closeModal();
              this.showMenu();
          }.bind(this))
      },
      handleSave: function(e) {
          var action = $(e.target).data('action');
          switch (action) {
              case "createMenu":
                  this.createMenu();
                  break;
              case "updateMenuItem":
                  this.updateMenu();
                  break;
          }
      },
      addMenu: function(item, action) {
          console.log('addMenu');
          data = {
              text_label: "菜单名",
              texts_label: "菜单数据",
              list_label: "父菜单",
              checkbox_label: "含有子菜单",
              text_kls: "menu_name",
              text_name: "menu_name",
              texts_kls: "menus_data",
              list_name: "parent_menu",

              list_kls: "parent_menu",
              checkbox_name: "has_sub_menu",
              checkbox_kls: "has_sub_menu",
              keyField: "id",
              valField: "name",
              item: item || false
          };
          this.model.getMenuParentItems().then(function(res) {
              console.log(res);
              data.list = res;
              $('.yumModal .modal-body').html(commonCreateTemplate(data));
              $('.yumModal.modal button.save').data("action", action ? action : "createMenu");
              this.showModal();
          }.bind(this))

      },
      showModal: function() {
          $('.yumModal').off();
          $('.yumModal').on('hide.bs.modal', function() {
              $('.yumModal .button.save').removeData('action').removeClass("create").addClass("save");
              $('.yumModal .hide').removeClass('hide');
          });
          $('.yumModal').modal('show');
      },
      showMenu: function(limit, offset) {
          $('.data-grid').empty();
          this.model.getUserMenus().then(function(res) {
              var currentSubMenuLength = 0;
              $.each(res || [], function(idx) {
                  $('.data-grid').append(gridTemplate({
                      idx: idx + 1,
                      item: res[idx]
                  }));
                  currentSubMenuLength = res[idx].subMenu.length;
              })
              buildDragger();

          }.bind(this));
      },
      appendToGrid: function(param) {
          console.log(111111111);
      }

  })
  module.exports = Screen;