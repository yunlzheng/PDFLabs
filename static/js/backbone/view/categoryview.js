/**
 * Created by zheng on 13-11-5.
 */

var app = app || {};

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
                 "limit":20
             }
        });
        return this;
    }

});