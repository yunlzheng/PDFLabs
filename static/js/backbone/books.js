/**
 * Created by zheng on 13-10-30.
 */
var Workspace = Backbone.View.extend({

    el: $('#app-books'),
    events: {
        "keypress #input_search": "search_page",
        "blur #input_search": "search_page"
    },
    initialize: function(){
        console.log(this.el);
        return this;
    },
    search_page: function(){
        var $input_search =  $("#input_search");
        var value = $input_search.val().trim().toUpperCase();
        $(".book_thing").removeClass('focus');
        if(!value){
            $input_search.attr('placeholder',"检索");
            return;
        }
        $(".book_intro").each(function(){
            var txt = $(this).html().trim().toUpperCase();
            if(txt.indexOf(value)!=-1){
                $(this).parents('.book_thing').addClass('focus');
            }
        });

    }
});

$(function(){

    var workspace = new Workspace();

});