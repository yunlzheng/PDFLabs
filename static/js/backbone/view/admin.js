/**
 * Created by zheng on 13-11-7.
 */
var app = app || {};

var IndexView = Backbone.View.extend({
    tag: 'div',
    className:"dashbord",

    template: _.template( $("#tpl_stage_dashbord").html() ),

    render: function(){

        this.el.innerHTML = this.template();
        this.$container = this.$('#page-container');
        return this;

    }
});

var AppView = Backbone.View.extend({

    el: 'body',

    initialize: function(){

        this.$stage = this.$('#stage');
        this.on('navigate', this.navigate);
        this.navigate_to_index();

    },

    navigate_to_index: function(){
        var view = new IndexView();
        this.$stage.html( view.render().el );
    },

    navigate_to_books: function(){
        var view = new BooksView();
        this.$stage.html( view.render().el );
    },

    navigate_to_category: function(){
        var view = new CategorysView();
        this.$stage.html( view.render().el );
    },

    navigate_to_groups: function(){

    },

    navigate_to_posts: function(){

    },

    navigate_to_users: function(){

    },

    navigate_to_settings: function(){

    }



});


