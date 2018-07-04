var Backbone = require('backbone');
var _ = require('underscore');

var View = require('./view');
var model = require('./model');
var view = new View(window.currentUser, model);

Backbone.fixtures = true;
var currentUserInfo = window.currentUser;
var AppRouter = Backbone.Router.extend({
    routes: {
        "user/:userid": "load_user",
        "usergroup/:groupid": "load_user_group",
        "modulegroup/:groupid": "load_modulegroup",
        "modulegroup/:groupid/type_:type": "load_module_groups_by_type",
        "module_user/:moduleid": "load_module_users",

        "module_usergroup/:moduleid": "load_module_user_groups",
        "module_modulegroup/:moduleid": "load_module_groups",
        "module_group/:moduleid/type_:type": "load_module_groups_by_type",
        "users": "init_user_screen",
        "usergroups": "init_usergroups_screen",
        "modulegroups": "init_modulegroup_screen",
        "modules": "load_modules",
        "search/:query/p:page": "search", // #search/kiwis/
        // "modules/user/:moduleid": "load_module_users",
        // "modules/usergroup/:moduleid": "load_module_user_groups",
        // "modules/modulegroup/:moduleid": "load_module_groups",
        "modules/t_:type/:moduleid": "load_module_users",
        "modules/:moduleid/user": "load_module_users",
        "modules/:moduleid/usergroup": "load_module_user_groups",
        "modules/:moduleid/modulegroup": "load_module_groups",
    },
});
var app_router = new AppRouter();
window.app = app_router;
app_router.on('route:load_user', function(userId) {
    console.log('route:load_user', userId);

    // model.getUserModules({
    //     id: userId ? userId : -1
    // }).then(function(items) {
    //     view.showUserModules(items, userId)
    // });
    view.doGgetUserModules(userId);

});

app_router.on('route:load_user_group', function(groupid) {
    console.log('route:load_user_group', groupid);

    // model.getUserGroupModules({
    //     id: groupid
    // }).then(function(items) {
    //     view.showUserGroupModules(items, groupid)
    // });
    view.doGetUserGroupModules(groupid);
});

app_router.on('route:load_modules', function(groupid) {
    console.log('route:load_modules', groupid);
    // view.showModuleGroupModules();
    // model.getModules({}).then(function(items) {
    //     view.showModules(items, groupid, 'user')
    // });
    view.doGetModules(groupid);
});
app_router.on('route:load_modulegroup', function(groupid) {
    console.log('route:load_modulegroup', groupid);
    // view.showModuleGroupModules();
    // model.getModuleGroups({
    //     id: groupid,
    //     type: 'user'
    // }).then(function(items) {
    //     view.showModuleGroupModules(items, groupid, 'user')
    // });
    view.doGetModuleGroups(
        groupid,
        'user'
    );
});
app_router.on('route:load_module_groups_by_type', function(groupid, type) {
    console.log('route:load_module_groups_by_type', groupid);
    // view.showModuleGroupModules();
    // model.getModuleGroups({
    //     id: groupid,
    //     type: type
    // }).then(function(items) {
    //     view.showModuleGroupModules(items, groupid, type)
    // });
    view.doGetModuleGroups(
        groupid,
        type
    );
});

app_router.on('route:load_module_users', function(moduleid) {
    console.log('route:load_module_users', moduleid);
    // view.showModuleUsers();

    // model.getModuleUsers({
    //     id: moduleid

    // }).then(function(items) {
    //     view.showModuleUsers(items, moduleid)
    // });
    view.doGetModuleUsers(moduleid);
});

app_router.on('route:load_module_user_groups', function(moduleid) {
    console.log('route:load_module_user_groups', moduleid);
    // view.showModuleUserGroups();

    // model.getModulesUserGroups({
    //     id: moduleid
    // }).then(function(items) {
    //     view.showModuleUserGroups(items, moduleid)
    // });
    view.doGetModulesUserGroups(moduleid);
});

app_router.on('route:load_module_groups', function(moduleid) {
    console.log('route:load_module_groups', moduleid);
    // view.showModuleModuleGroups();
    view.doGetModulesModuleGroups(moduleid);
    // model.getModulesModuleGroups({
    //     id: moduleid,
    //     type: 'module_id'
    // }).then(function(items) {
    //     view.showModuleModuleGroups(items, moduleid)
    // });
});

app_router.on('route:init_user_screen', function(moduleid) {
    console.log('route:init_user_screen', moduleid);
    // view.showInitUserScreen();
    // var dfdlist = [model.getUsers(), model.getUserModules({
    //     t: new Date()
    // })];
    var users, modules;
    $.when(model.getUsers())
        .then(
            function(data) {
                // if (parseInt(data.status) == 0) {
                //     users = data.info;
                // } else {
                //     users = [];
                // }
                users = data;
                return model.getUserModules({
                    id: -1
                })
            })
        .then(
            function(modules) {
                // modules = data;
                // if (parseInt(data.status) === 0) {
                //     modules = data.info;
                // } else {
                //     modules = [];
                // }
                console.log(users, modules);
                return view.showInitUserScreen(users, modules);
            });
});

app_router.on('route:init_usergroups_screen', function(moduleid) {
    console.log('route:init_usergroups_screen', moduleid);
    // view.showInitUserGroupScreen();
    $.when(
        model.getSysUserGroups({
            limit: 100
        }),
        model.getUserGroups({
            id: -1
        })
    ).then(function(groups, items) {
        console.log(groups, items);
        view.showInitUserGroupScreen(groups, items)
    });
});

app_router.on('route:init_modulegroup_screen', function(moduleid) {
    console.log('route:init_modulegroup_screen', moduleid);
    // view.showModuleGroupScreen();

    model.getModuleGroups({}).then(function(moduleGroups) {
        view.showModuleGroupScreen(moduleGroups)
    });
});


Backbone.history.start();
window.Backbone = Backbone;
module.exports = app_router;