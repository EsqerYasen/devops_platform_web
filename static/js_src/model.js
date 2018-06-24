var Backbone = require('backbone');
var $ = require('jquery');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
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
    if (data) {
        data.csrfmiddlewaretoken = window.csrf_token;
    }
    var _data = {
        url: urlString,
        data: data,
        // data: type == 'POST' ? JSON.stringify(data) : data,
        dataType: 'json',
        // contentType: type == 'POST' ? 'application/json' : null,
        contentType: type == 'POST' ? 'application/x-www-form-urlencoded' : null,
        method: type,
        timeout: 30e3
    };

    if (1) {
        console.debug('Call URL with Data ', _data);
        return $.ajax(_data).fail(function(e) {
            console.warn('Failed request to "' + url + '": ' + JSON.stringify(e));
        });
    } else {
        console.log("skip api call=>", url, data);
        return $.when(fixture.getFixture(url, data));
    }
}
var currentUserid = window.currentUserId;

function get(url, data) {
    return request(url, 'GET', data);
}

function post(url, data) {
    //var csrftoken = getCookie('csrftoken');

    return request(url, 'POST', data);
}
module.exports = {
    getUsers: function() {
        return get('/auth/rest/user/list').then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },

    getSysUserGroups: function(data) {
        return get('/auth/rest/user_group/list', $.param($.extend({
            limit: 100
        }, data || {}))).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
    getUserGroups: function(user) {
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
                this.disableModulePrivilegeForUser(param).then(function() {
                    $('.btn_edit[data-id="' + param.id + '"]').closest('tr').hide();
                });
                break;
            default:
                break;
        }
        console.log(param);
    },
    updateModel: function(param) {
        switch (param.type) {
            case "user_modules":
                this.updateModulePrivilegeForUser(param).then(function() {
                    $('.btn_edit[data-id="' + param.id + '"]').closest('tr').find('input[type="radio"][value="' + param.privilege + '"]').click();
                });
                break;
            default:
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
    addUserTOGroup: function() {

        var data = param;
        data.user_id = param.item.uesr_id;
        data.module_id = param.item.module_id;
        data.value = param.privilege;
        data.id = param.item.id;
        return post('/auth/rest/module_group/', data)
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
                return msg.info;
            } else {
                return [];
            }
        });
    }

};