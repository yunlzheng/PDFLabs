/**
 * Created by zheng on 13-11-5.
 */
var app = app || {};


var BookView = Backbone.View.extend({

    tag: 'div',

    className: 'span2 book',

    template: _.template( $("#tpl_book").html() ),

    initialize: function(){

    },

    render: function(){
        this.$el.html( this.template(this.model.toJSON()) );
        return this;
    }

});

var Workspace = Backbone.View.extend({

    el: $("#bookcase-details"),

    initialize: function(){

        this.listenTo(app.books, 'add', this.addOne);
        app.books.fetch();

    },

    addOne: function(book){

        var bookView = new BookView({ model:book });
        $("#contents").append( bookView.render().el );
    }

});

$(function(){

    var workspace = new Workspace();

});