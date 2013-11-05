/**
 * Created by zheng on 13-11-5.
 */
var app = app || {}

var BookList = Backbone.Collection.extend({

    url: "/api/rest/books",
    model:app.BookCategoryModel

});

app.books = new BookList();
