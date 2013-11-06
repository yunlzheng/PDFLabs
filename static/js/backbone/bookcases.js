/**
 * Created by zheng on 13-11-5.
 */
var app = app || {};


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
