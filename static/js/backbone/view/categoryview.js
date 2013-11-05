/**
 * Created by zheng on 13-11-5.
 */

var app = app || {};

app.BookCategoryView = Backbone.View.extend({

    tagName:"div",

    className:"bookcase_category",

    template: _.template( $("#tpl_bookcase_category").html() ),

    initialize: function() {
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destory', this.remove);
    },

    render: function() {
        this.$el.html( this.template(this.model.toJSON()) );
        return this;
    }

});