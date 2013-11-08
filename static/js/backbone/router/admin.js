/**
 * Created by zheng on 13-11-7.
 */
var app = app || {};

var Workspace = Backbone.Router.extend({

    routes: {
        "index":"index",//#index
        "settings":"settings",//#settings
        "books":"books",//#books
        "books/category":"book_category",
        "groups":"groups",
        "groups/post": "posts",
        "users":"users"
    },

    index: function(){
        app.appView.navigate_to_index();
    },

    books: function(){
        app.appView.navigate_to_books();
    },

    book_category: function(){
        app.appView.navigate_to_category();
    },

    groups: function(){
        app.appView.navigate_to_groups();
    },

    posts: function(){
        app.appView.navigate_to_posts();
    },

    users: function(){
        app.appView.navigate_to_users();
    },

    settings: function(){
        app.appView.navigate_to_settings();
    }

});
