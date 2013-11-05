/**
 * Created by zheng on 13-11-5.
 */
var app = app || {}

app.BookCategoryModel = Backbone.Model.extend({
    urlRoot:"/api/rest/categorys",
    parse: function(response){
        response.id = response._id.$oid;
        delete response._id;
        return response;
    }
});