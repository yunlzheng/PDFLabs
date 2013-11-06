/**
 * Created by zheng on 13-11-5.
 */
var app = app || {}

var CategoryList = Backbone.Collection.extend({

    url: "/api/rest/categorys",

    model:app.BookCategoryModel

});

app.Categorys = new CategoryList();
