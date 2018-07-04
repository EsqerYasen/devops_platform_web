var Backbone = require('backbone');
var _ = require('underscore');

var View = require('./view');
var model = require('./model');
var view = new View(window.currentUser, window.currentUserId, model);

Backbone.fixtures = true;
var currentUserInfo = window.currentUser;
var AppRouter = Backbone.Router.extend({
    routes: {
        // "user/:userid": "load_user",
        // "usergroup/:groupid": "load_user_group",
        // "modulegroup/:groupid": "load_modulegroup",
        // "modulegroup/:groupid/type_:type": "load_module_groups_by_type",
        // "module_user/:moduleid": "load_module_users",

        // "module_usergroup/:moduleid": "load_module_user_groups",
        // "module_modulegroup/:moduleid": "load_module_groups",
        // "module_group/:moduleid/type_:type": "load_module_groups_by_type",
        // "users": "init_user_screen",
        // "usergroups": "init_usergroups_screen",
        // "modulegroups": "init_modulegroup_screen",
        // "modules": "load_modules",
        // "search/:query/p:page": "search", // #search/kiwis/
        // // "modules/user/:moduleid": "load_module_users",
        // // "modules/usergroup/:moduleid": "load_module_user_groups",
        // // "modules/modulegroup/:moduleid": "load_module_groups",
        // "modules/t_:type/:moduleid": "load_module_users",
        // "modules/:moduleid/user": "load_module_users",
        // "modules/:moduleid/usergroup": "load_module_user_groups",
        // "modules/:moduleid/modulegroup": "load_module_groups",
    },
});
var app_router = new AppRouter();
window.app = app_router;
app_router.on('route:load_user', function(userId) {
    console.log('route:load_user', userId);

});



Backbone.history.start();
window.Backbone = Backbone;
module.exports = app_router;
