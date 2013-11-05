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
        console.log(this.model.toJSON());
        this.$el.html( this.template(this.model.toJSON()) );
        return this;
    }

});