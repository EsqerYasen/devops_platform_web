var Backbone = require('backbone');
var $ = require('jquery');
var config = require('../config.json');
function defaultCallBack() {
    window.YUMEVENTS.trigger('closeModal', {});
}

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
    var host = config.url.job;
    var _data = {
        url: host + urlString,
        data: data,
        dataType: 'json',
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
    getJobList: function(id, limit = 10, offset = 0) {
        ///rest/appmanage/list/?offset=0&limit=10&id=1
        return get('/rest/flowcontrol/list/', {
                limit: limit,
                offset: offset,
                id: id
            },
            config.url.job).then(function(data) {
            return data;
        });

    }

};
