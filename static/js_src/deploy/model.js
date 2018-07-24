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
    data = data || {};
    var _data = {
        serivceName: "p_job",
        restName: url+'?'+ $.param(data),
        t: new Date().getTime()

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


module.exports = {
    config: config,
    getJobList: function(name, id, limit = 10, offset = 0) {
        return get('/rest/deploytool/list/', {
                limit: limit,
                offset: offset,
                id: id,
                name: name
            },
            config.url.job).then(function(data) {
            return data;
        });

    },
    getVersionLists: function(toolIds = []) {
        return get('/rest/deploytool/versionlist/', {deploy_tool_ids: JSON.stringify(toolIds)}).then(function(data) {
            return data;
        });
    }
};
