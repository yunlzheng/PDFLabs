/**
 * Created by zheng on 13-11-7.
 */
var app = app || {}

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
        app.appView.trigger('navigate',"index");
    },

    books: function(){
        app.appView.trigger('navigate',"books");
    },

    book_category: function(){
        app.appView.trigger('navigate',"categorys");
    },

    groups: function(){
        app.appView.trigger('navigate',"groups");
    },

    posts: function(){
        app.appView.trigger('navigate',"posts");
    },

    users: function(){
        app.appView.trigger('navigate',"users");
    },

    settings: function(){
        app.appView.trigger('navigate',"settings");
    }

});

app.TodoRouter = new Workspace();
Backbone.history.start();