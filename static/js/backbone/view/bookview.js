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