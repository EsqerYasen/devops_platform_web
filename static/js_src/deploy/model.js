var Backbone = require('backbone');
var $ = require('jquery');

function defaultCallBack() {
    window.YUMEVENTS.trigger('closeModal', {});
}

var config = require('../config.json');


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

function request(url, type, data, server) {
    var urlString = url;
    console.debug('Call URL: ' + urlString);
    if (data) {
        data.csrfmiddlewaretoken = window.csrf_token;
    }
    var host = server ? server : '';
    var _data = {
        url: host + urlString,
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
            alert(e.responseText);
        });
    } else {
        console.log("skip api call=>", url, data);
        return $.when(fixture.getFixture(url, data));
    }
}
var currentUserid = window.currentUserId;

function get(url, data, server) {
    return request(url, 'GET', data, server);
}

function post(url, data, server) {
    return request(url, 'POST', data, server);
}

function filterPermissonByConfig(permissions, section) {
    console.log(5555555, section);
    var perms = [];
    var keys = Object.keys(permissions);
    var perm;
    for (var i = 0; i < keys.length; i++) {
        perm = permissions[keys[i]];
        if (perm.collection === section.collection && perm.dataset === section.dataset) {
            perm.id = parseInt(keys[i]);
            perms.push(perm);
        }
    }
    console.log(perms);
    return perms;
}

function filterIDFromPermission(permissions, section) {
    permissions = filterPermissonByConfig(permissions, section)
    var ids = [];
    var perm;
    for (var i = 0; i < permissions.length; i++) {
        ids.push(permissions[i].idx);
    }
    return ids;
}
module.exports = {
    config: config,
    filterPermissonByConfig: filterPermissonByConfig,
    filterIDFromPermission: function(permissions, section) {
        return filterIDFromPermission(permissions, section);
    },
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
    getJobList: function(permissions = {}, limit = 10, offset = 0) {
        return get('/rest/deploytool/list/', {
                limit: limit,
                offset: offset,
                p: JSON.stringify(filterIDFromPermission(permissions, config.type.job))
            },
            config.url.job).then(function(data) {
            return data;
        });

    },
    getVersionLists: function(toolIds) {
        var param = 'deploy_tool_ids=' + JSON.stringify(toolIds);
        return get('/rest/deploytool/versionlist/?' + param, {}, config.url.job).then(function(data) {
            return data;
        });
    },
    getPermssions: function() {
        return get('/auth/rest/modules_permission/').then(function(data) {
            console.log(data);
            return data;
        });
    },
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
    updateUserGroupToModule: function(param) {
        //"{"privilege":"1","id":1,"type":"module_user_groups"}"
        var data = param;
        data.id = param.id;
        data.value = param.privilege;
        return post('/auth/rest/permission/user_group/', data)
    }

};
