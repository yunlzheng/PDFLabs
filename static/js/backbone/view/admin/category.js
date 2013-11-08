/**
 * Created by zheng on 13-11-8.
 */
var app = app || {};

var BookshelfView = Backbone.View.extend({

    tag: "div",
    className: "bookshelf",

    template: _.template( $("#tpl_bookshelf").html() ),

    initialize: function(){
        this.models =  new BookList();
        this.listenTo(this.models, 'add', this.addOne);
    },

    render: function(){

        this.el.innerHTML = this.template( this.model.toJSON() );
        this.models.fetch({
             "data": {
                "category": this.model.attributes.id,
                 "skip":0,
                 "limit":14
             }
        });
        return this;

    },

    addOne: function(){

    }

});

var CategorysView = Backbone.View.extend({

    tag: 'div',

    className:"books",

    template: _.template( $("#tpl_stage_categorys").html() ),

    events: {

    },

    initialize: function(){
        this.listenTo(app.Categorys, 'add', this.addOne)
    },

    render: function(){
        app.Categorys.reset();
        this.el.innerHTML = this.template();
        this.$container = this.$('#page-container');
        app.Categorys.fetch();
        return this;
    },

    addOne: function( model ){
        var view = new BookshelfView({ model:model });
        this.$container.append(view.render().el);
    }

});