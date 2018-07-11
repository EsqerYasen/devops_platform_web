var Backbone = require('backbone');
var $ = require('jquery');

var config = require('../config.json');
function request(url, type, data) {
    var urlString = url;
    console.debug('Call URL: ' + urlString);
    if (data) {
        data.csrfmiddlewaretoken = window.csrf_token;
    }
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
    data = data || {};
    var _data = {
        restName: url+'?'+ $.param(data),
        t: new Date().getTime()

    }
    return request(url, 'GET', _data);
}

function post(url, data) {
    var _data = {
        restName: url,
        req_data: (data)
    }
    return request(url, 'POST', _data);
}


module.exports = {
    config: config,
    getUserMenus: function() {
        return get('/menu/rest/menu/').then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
};
