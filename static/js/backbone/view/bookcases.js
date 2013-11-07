/**
 * Created by zheng on 13-11-5.
 */
var app = app || {};

app.BookView = Backbone.View.extend({

    tag:"div",

    className:"bookcase_item",

    template : _.template( $("#tpl_bookcase_book_item").html() ),

    initialize: function(){

    },

    render: function(){
        var _model = this.model.toJSON();
        var img = parseInt(Math.random()*(10-0+1)+0);
        _model.img = img
        this.$el.html( this.template(_model) );
        return this;
    }

});

app.BookCategoryView = Backbone.View.extend({

    tagName:"div",

    className:"bookcase_category",

    template: _.template( $("#tpl_bookcase_category").html() ),

    initialize: function() {

        this.models =  new BookList();
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destory', this.remove);
        this.listenTo(this.models, 'add', this.addBook);

    },

    addBook: function(book){
        var view = new app.BookView( {model: book} );
        this.$books.append(view.render().el);
    },

    render: function() {
        this.$el.html( this.template(this.model.toJSON()) );
        this.$books = this.$('.list');
        this.models.fetch({
             "data": {
                "category": this.model.attributes.id,
                 "skip":0,
                 "limit":14
             }
        });
        return this;
    }

});

var Workspace = Backbone.View.extend({

    el: $("#app-bookcase"),
    initialize: function(){

        this.$bookcases = this.$("#bookcase_category_list");

        this.listenTo(app.Categorys,'add', this.addCategory);

        app.Categorys.fetch();

    },
    addCategory: function(category){
        var view = new app.BookCategoryView( {model: category} );
        this.$bookcases.append(view.render().el);
    }

});

$(function(){

    var workspace = new Workspace();

});
