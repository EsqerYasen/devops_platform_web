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
    return request(url, 'GET', data);
}

function post(url, data) {
    return request(url, 'POST', data);
}


module.exports = {
    config: config,
    getUserMenus: function(user) {
        return get('/menu/rest/menuItems/').then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
    getMenuParentItems: function(user) {
        return get('/menu/rest/menuItems/', {isParent: true}).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
    updateMenu: function(param) {
        return this.createMenu(param)
    },
    createMenu: function(param) {
        return post('/menu/rest/menuItems/', param).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
};
