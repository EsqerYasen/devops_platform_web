var Backbone = require('backbone');
var view = require('./view');
var AppRouter = Backbone.Router.extend({

  routes: {
    "user/:userid":                     "load_user",
    "usergroup/:groupid":               "load_user_group",
    "modulegroup/:groupid":             "load_modulegroup",
    "module/:moduleid/user":            "load_module_users",
    "module/:moduleid/usergroup":       "load_module_user_groups",
    "module/:moduleid/modulegroup":     "load_module_groups",
    "users":                            "init_user_screen",
    "usergroups":                       "init_usergroups_screen",
    "modulegroups":                     "init_modulegroup_screen",
    "search/:query/p:page":             "search"   // #search/kiwis/p7
  },
});
var app_router = new AppRouter;

app_router.on('route:load_user', function(userId) {
    console.log('route:load_user', userId);
});

app_router.on('route:load_user_group', function(groupid) {
    console.log('route:load_user_group', groupid);
});

app_router.on('route:load_modulegroup', function(groupid) {
    console.log('route:load_modulegroup', groupid);
});

app_router.on('route:load_module_users', function(moduleid) {
    console.log('route:load_module_users', moduleid);
});

app_router.on('route:load_module_user_groups', function(moduleid) {
    console.log('route:load_module_user_groups', moduleid);
});

app_router.on('route:load_module_groups', function(moduleid) {
    console.log('route:load_module_groups', moduleid);
});

app_router.on('route:init_user_screen', function(moduleid) {
    console.log('route:init_user_screen', moduleid);
});

app_router.on('route:init_usergroups_screen', function(moduleid) {
    console.log('route:init_usergroups_screen', moduleid);
});

app_router.on('route:init_modulegroup_screen', function(moduleid) {
    console.log('route:init_modulegroup_screen', moduleid);
});


Backbone.history.start();
module.exports = app_router;
