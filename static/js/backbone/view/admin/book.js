/**
 * Created by zheng on 13-11-8.
 */
var app = app || {};

var BookView = Backbone.View.extend({

    template: _.template( $("#tpl_stage_item").html() ),

    initialize: function(){

    }

});

var BooksView = Backbone.View.extend({
    tag: 'div',
    className:"books",

    template: _.template( $("#tpl_stage_books").html() ),

    initialize: function(){

        this.listenTo(app.books, 'add', this.addOne);

    },

    render: function(){

        this.el.innerHTML = this.template();
        this.$container = this.$('#page-container');
        app.books.fetch();
        return this;

    },

    addOne: function( model ){

        console.log(model.toJSON());

    }

});