/**
 * Created by zheng on 13-11-8.
 */
var app = app || {};

var BookView = Backbone.View.extend({

    tag: "div",

    className: "book_item",

    template: _.template( $("#tpl_book_item").html() ),

    events: {

        'click .menu': 'contextMenu'
    },

    initialize: function(){

    },

    render: function(){

        this.el.innerHTML = this.template( this.model.toJSON() );
        return this;

    },

     contextMenu: function(e){
         $('body').foggy(false);
         return false;

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

        app.books.reset();
        this.el.innerHTML = this.template();
        this.$container = this.$('#page-container');
        app.books.fetch();
        return this;

    },

    addOne: function( model ){

        var view = new BookView({ model:model });
        this.$container.append( view.render().el );

    }

});