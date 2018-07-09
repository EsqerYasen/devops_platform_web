var Backbone = require('backbone');
var _ = require('underscore');

var View = require('./view');
var model = require('./model');
var view = new View(window.currentUser, window.currentUserId, model);

Backbone.fixtures = true;
var currentUserInfo = window.currentUser;
var AppRouter = Backbone.Router.extend({
    routes: {}
});
var app_router = new AppRouter();
window.app = app_router;
app_router.on('route:load_user', function(userId) {
    console.log('route:load_user', userId);
});



Backbone.history.start();
window.Backbone = Backbone;
module.exports = app_router;
