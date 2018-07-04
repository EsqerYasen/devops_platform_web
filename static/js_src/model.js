var Backbone = require('backbone');
var $ = require('jquery');

function defaultCallBack() {
    window.YUMEVENTS.trigger('closeModal', {});
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function request(url, type, data) {
    var urlString = url;
    console.debug('Call URL: ' + urlString);
    var _data = {
        url: urlString,
        data: data,
        dataType: 'json',
        contentType: type == 'POST' ? 'application/x-www-form-urlencoded' : null,
        method: type,
        timeout: 30e3
    };
    return $.ajax(_data).fail(function(e) {
        alert(e.responseText);
    });
}
var currentUserid = window.currentUserId;

function get(url, data) {
    return request(url, 'GET', data);
}

function post(url, data) {
    return request(url, 'POST', data);
}

module.exports = {
    getItemByIdFromCache: function(key, id, isStatic) {
        var dfd = $.Deferred();
        var cache = localStorage.getItem(key) || "[]";
        var list = JSON.parse(cache);
        $(list).filter(function(i, item) {
            console.log(i, item);
            return item.id == 3
        });
        var founds = [];
        if (list.length) {
            founds = $(list).filter(function(i, item) {
                return parseInt(id) === parseInt(item.id);
            })
        }
        if (founds.length) {
            dfd.resolve(founds[0]);
        } else {
            dfd.reject(id);
        }
        if (isStatic) {
            if (founds.length) {
                return founds[0];
            } else {
                return false;
            }
        }
        return dfd;
    },
    getModuleByIdFromCache: function(id) {
        return this.getItemByIdFromCache('modules', id);
    },
    getModuleGroupByIdFromCache: function(id) {
        return this.getItemByIdFromCache('module_group', id);
    },
    getUserByIdFromCache: function(id) {
        return this.getItemByIdFromCache('users', id);
    },
    getGroupByIdFromCache: function(id) {
        return this.getItemByIdFromCache('groups', id);
    },
    //getSysUserGroups
    getUsers: function() {
        localStorage.setItem('lastQuery', 'getUsers');
        return get('/auth/rest/user/list').then(function(data) {
            if (parseInt(data.status) === 0) {
                localStorage.setItem('users', JSON.stringify(data.info));
                return data.info;
            } else {
                return [];
            }
        });
    },

    getSysUserGroups: function(data) {
        localStorage.setItem('lastQuery', 'getSysUserGroups');
        return get('/auth/rest/user_group/list', $.param($.extend({
            limit: 100
        }, data || {}))).then(function(data) {
            if (parseInt(data.status) === 0) {
                localStorage.setItem('groups', JSON.stringify(data.info));
                return data.info;
            } else {
                return [];
            }
        });
    },
    getUserGroups: function(user) {
        localStorage.setItem('lastQuery', 'getUserGroups');
        return get('/auth/rest/permission/user_group/',
            encodeURI("id=" + user.id)
        ).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
    getModuleUsers: function(param) {
        localStorage.setItem('lastQuery', 'getModuleUsers');
        return get('/auth/rest/permission/module/',
            $.param($.extend(true, {
                type: 'module_id',
                order_by: "id",
                limit: 100,
                offset: 0
            }, param))
        ).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
    getUserModules: function(param) {
        localStorage.setItem('lastQuery', 'getUserModules');
        return get('/auth/rest/permission/module/',
            $.param(param)
        ).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
    getModulesUserGroups: function(param) {
        localStorage.setItem('lastQuery', 'getModulesUserGroups');
        return get('/auth/rest/permission/user_group/',
            $.param($.extend(true, {
                type: 'module_id',
                order_by: "id",
                limit: 100,
                offset: 0
            }, param))
        ).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
    getUserGroupModules: function(param) {
        localStorage.setItem('lastQuery', 'getUserGroupModules');
        return get('/auth/rest/permission/user_group/',
            $.param(param)
        ).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
    removeModel: function(param) {
        switch (param.type) {
            case "user_modules":
            case "module_users":
                return this.disableModulePrivilegeForUser(param).then(function(res) {
                    $('.btn_edit[data-id="' + param.id + '"]').closest('tr').hide();
                    return res;
                });
                break;
            case "module_user_groups":
                return this.disableUserGroupsForMoudle(param).then(function(res) {
                    $('.btn_edit[data-id="' + param.id + '"]').closest('tr').hide();
                    return res;
                });
                break;
            case "module_moduleGroups":
                return this.disableModuleGroupToModule(param).then(function(res) {
                    $('.btn_edit[data-id="' + param.id + '"]').closest('tr').hide();
                    return res;
                });
                break;
            case "modules_for_user_group":
                return this.disableModuleForUserGroup(param).then(function(res) {
                    $('.btn_edit[data-id="' + param.id + '"]').closest('tr').hide();
                    return res;
                });
                break;
            case "moduleGroup_modules":
                return this.disableUserForModuleGroup(param).then(function(res) {
                    $('.btn_edit[data-id="' + param.id + '"]').closest('tr').hide();
                    return res;
                });
                break;
            default:
                console.log('++++++++++!!!!', param);
                break;
        }
        console.log(param);
    },
    updateModel: function(param) {
        switch (param.type) {
            case "user_modules":
                return this.updateModulePrivilegeForUser(param).then(function(res) {
                    $('.btn_edit[data-id="' + param.id + '"]').closest('tr').find('input[type="radio"][value="' + param.privilege + '"]').click();
                    defaultCallBack();
                    return res;
                });
                break;
            case "add_moudle_user":
                return this.addUserToModule(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            case "add_moudle_user_group":
                //addUserGroupToModule
                //addModuleForUserGroup
                return this.addUserGroupToModule(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            case "module_user_groups":
                return this.updateUserGroupToModule(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            case "add_moudle_moduleGroups":
                return this.addModuleGroupToModule(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            case "module_moduleGroups":
                // {"privilege":"2","id":1,"type":"module_moduleGroups"}
                return this.updateModuleGroupToModule(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            case "add_moudle_groupModules_user":
                return this.addUserToModuleGroup(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            case "add_moudle_groupModules_module":
                return this.addModuleToModuleGroup(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            case "modules_for_user_group":
                return this.updateModulesForUserGroup(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                //"{"privilege":"2","id":1,"type":"modules_for_user_group"}"
                break;
            case "add_module":
                return this.addModuleForUserGroup(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            case "create_moduleGroup":
                return this.createModuleGroup(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
            case "create_module":
                return this.createModule(param).then(function(res) {
                    defaultCallBack();
                    return res;
                });
                break;
            default:
                console.log('-----------!!!!', param);
                break;
        }
        console.log(param);
    },

    addToModel: function(param) {
        console.log(param);
    },
    createModel: function(param) {
        console.log(param);
    },
    disableUserForModuleGroup: function(param) {
        console.log('createModuleGroup', param);
        var data = {};
        data.id = param.id;
        data.is_enabled = 0;
        return post('/auth/rest/module_group/users/', data);
    },
    createModule: function(param) {
        console.log('createModuleGroup', param);
        var data = {};
        data.name = param.inputVal;
        data.alias = param.inputVal2;
        data.url = param.inputVal3;

        data.open_db = param.inputVal4;
        data.open_table = param.inputVal5;
        data.open_id = param.inputVal6;
        data.owner_id = param.selectionVal;
        return post('/auth/rest/module/', data);
    },
    createModuleGroup: function(param) {
        console.log('createModuleGroup', param);
        var data = {};
        data.name = param.inputVal;
        data.owner_id = param.selectionVal;
        data.value = param.privilege;
        return post('/auth/rest/module_group/', data);
    },
    addModuleForUserGroup: function(param) {
        console.log(param);
        var data = {};
        data.group_id = param.id;
        data.module_id = param.selectionVal;
        data.value = param.privilege;
        return post('/auth/rest/permission/user_group/', data);
    },
    addUserGroupToModule: function(param) {
        console.log(param);
        var data = {};
        data.group_id = param.selectionVal;
        data.module_id = param.id;
        data.value = param.privilege;
        return post('/auth/rest/permission/user_group/', data);
    },
    //permission/user_group
    disableModuleForUserGroup: function(param) {
        var data = {};
        // data.id = param.id;
        data.id = param.item.user_group_permission_id;
        data.is_enabled = 0;
        return post('/auth/rest/permission/user_group/', data)
    },
    updateModulesForUserGroup: function(param) {
        //"{"privilege":"4","id":1,"type":"add_moudle_groupModules_module","selectionVal":"3"}"
        var data = {};
        data.id = param.item.user_group_permission_id;
        data.value = param.privilege;
        console.log("pending");
        return post('/auth/rest/permission/user_group/', data)
    },
    // updateUserGroup
    addModuleToModuleGroup: function(param) {
        //"{"privilege":"4","id":1,"type":"add_moudle_groupModules_module","selectionVal":"3"}"
        var data = {};
        data.group_id = param.id;
        data.module_id = param.selectionVal;
        console.log("pending");
        return post('/auth/rest/module_groups/', data)
    },
    addUserToModuleGroup: function(param) {
        //"{"privilege":"4","id":1,"type":"add_moudle_groupModules_user","selectionVal":"2"}"
        var data = {};
        data.user_id = param.selectionVal;
        data.group_id = param.id;
        delete data.id;
        return post('/auth/rest/module_group/users/', data)
    },
    addUserToModule: function(param) {
        //{"privilege":"4","id":1,"type":"add_moudle_user","selectionVal":"6"}
        var data = param;
        data.user_id = param.selectionVal;
        data.module_id = param.id;
        data.value = param.privilege;
        data.is_enabled = 1;
        delete data.id;
        return post('/auth/rest/permission/module/', data)
    },
    addUserTOGroup: function(param) {

        var data = {};
        data.user_id = param.item.uesr_id;
        data.module_id = param.item.module_id;
        data.value = param.privilege;
        return post('/auth/rest/module_group/', data);
    },
    updateModuleGroupToModule: function(param) {
        // {"privilege":"2","id":1,"type":"module_moduleGroups"}
        var data = {};
        data.group_id = param.selectionVal;
        data.value = param.privilege;
        data.id = param.id;
        return post('/auth/rest/permission/module_group/', data);
    },
    addModuleGroupToModule: function(param) {
        // {"privilege":"1","id":1,"type":"add_moudle_moduleGroups","selectionVal":"1"}
        var data = {};
        data.group_id = param.selectionVal;
        data.value = param.privilege;
        data.module_id = param.id;
        return post('/auth/rest/permission/module_group/', data);
    },
    disableModuleGroupToModule: function(param) {
        // "{"id":1,"type":"module_moduleGroups","item":{"id":1,"name":"module_group_tg1","module_id":1,"privilege":4,"owner_id":1}}"
        var data = {};
        data.is_enabled = 0;
        data.id = param.id;
        return post('/auth/rest/permission/module_group/', data);
    },
    // updateModuleGroupToModule: function() {
    //     var data = {};
    //     data.user_id = param.item.uesr_id;
    //     data.module_id = param.item.module_id;
    //     data.value = param.privilege;
    //     return post('/auth/rest/permission/module_group/', data);
    // },
    updateUserGroupToModule: function(param) {
        //"{"privilege":"1","id":1,"type":"module_user_groups"}"
        var data = param;
        data.id = param.id;
        data.value = param.privilege;
        return post('/auth/rest/permission/user_group/', data)
    },
    disableUserGroupsForMoudle: function(param) {
        var data = {};
        data.is_enabled = 0;
        data.id = param.id;
        return post('/auth/rest/permission/user_group/', data);
    },
    updateModulePrivilegeForUser: function(param) {
        var data = param;
        data.user_id = param.item.uesr_id;
        data.module_id = param.item.module_id;
        data.value = param.privilege;
        data.id = param.item.id;
        return post('/auth/rest/permission/module/', data)
    },
    disableModulePrivilegeForUser: function(param) {
        var data = param;
        data.user_id = param.item.uesr_id;
        data.module_id = param.item.module_id;
        data.is_enabled = 0;
        data.id = param.item.id;
        return post('/auth/rest/permission/module/', data);
    },
    getModulesModuleGroups: function(param) {
        localStorage.setItem('lastQuery', 'getUserGroupModules');
        return get('/auth/rest/permission/module_group',
            $.param($.extend(true, {
                type: 'module_id',
                order_by: "id",
                limit: 100,
                offset: 0
            }, param))
        ).then(function(msg) {
            if (parseInt(msg.status) === 0) {
                return msg.info;
            } else {
                return [];
            }
        });
    },
    getModuleGroups: function(param) {
        return get('/auth/rest/module_group/list/',
            $.param(param || {})
        ).then(function(msg) {
            if (parseInt(msg.status) === 0) {
                localStorage.setItem('module_group', JSON.stringify(msg.info));
                return msg.info;
            } else {
                return [];
            }
        });
    },
    getModules: function(param) {
        return get('/auth/rest/module/list/',
            $.param($.extend(true, {
                order_by: "id",
                limit: 100,
                offset: 0
            }, param))
        ).then(function(msg) {
            if (parseInt(msg.status) === 0) {
                localStorage.setItem('modules', JSON.stringify(msg.info));
                return msg.info;
            } else {
                return [];
            }
        });
    }
};
