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

function request(url, type, data) {
    var urlString = url;
    console.debug('Call URL: ' + urlString);
    var _data = {
        url: '/forward_to_service/?',
        data: data,
        dataType: 'json',
        contentType: type == 'POST' ? 'application/x-www-form-urlencoded' : null,
        method: type,
        timeout: 30e3
    };

    console.debug('Call URL with Data ', _data);
    return $.ajax(_data).fail(function(e) {
        alert(e.responseText);
    });

}
var currentUserid = window.currentUserId;

function get(url, data) {
    var _data = {
        serivceName: "p_job",
        restName: url+'?'+ $.param(data),
        req_data: ''
    }
    return request(url, 'GET', _data);
}

function post(url, data) {
    var _data = {
        serivceName: "p_job",
        restName: url,
        req_data: (data)
    }
    return request(url, 'POST', _data);
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
        return get('/rest/appmanage/list/', {
                limit: limit,
                offset: offset,
                id: id
            }).then(function(data) {
            return data;
        });

    }

};
