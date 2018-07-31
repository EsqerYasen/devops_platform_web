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

function parseMenuItem(m) {
    return {
        "has_sub_menu": m.has_sub_menu,
        "id": m.id,
        "menu": m.menu,
        "name": m.name,
        "order_index": m.order_index,
        "parent_id": m.parent_id,
    }
}

module.exports = {
    config: config,
    getUserMenus: function(user) {
        var menu = {};
        return get('/menu/rest/menuItems/').then(function(data) {
            if (parseInt(data.status) === 0) {
                if (data.info && data.info.length) {

                    $.each(data.info, function(_i, _m) {
                        if (_m.parent_id !== -1) {
                            if (typeof menu[_m.parent_id] === "undefined" && _m.parent_id !== -1) {
                                menu[_m.parent_id] = {};
                                menu[_m.parent_id].subMenu = [];
                                menu[_m.parent_id].subMenu.push(parseMenuItem(_m));
                            } else {
                                menu[_m.parent_id].subMenu.push(parseMenuItem(_m));
                            }
                        } else {
                            if (typeof menu[_m.id] !== "undefined") {
                                if (typeof menu[_m.id].id !== "undefined") {
                                    console.log("item existed");
                                } else {
                                    menu[_m.id] = $.extend(true, menu[_m.id], parseMenuItem(_m));
                                    console.log("item updated");
                                }
                            } else {
                                menu[_m.id] = $.extend(true, {
                                    subMenu: []
                                }, parseMenuItem(_m));
                            }
                        }
                    })
                }
                return Object.values(menu).sort(function(a, b) {
                    return a.order_index < b.order_index
                });
            } else {
                return [];
            }
        });
    },
    getMenuParentItems: function(user) {
        return get('/menu/rest/menuItems/', {
            isParent: true
        }).then(function(data) {
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
    changeOrder: function(param) {
        return post('/menu/rest/menuItems/changeOrder/', param).then(function(data) {
            if (parseInt(data.status) === 0) {
                return data.info;
            } else {
                return [];
            }
        });
    },
};