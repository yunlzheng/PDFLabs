/**
 * Created by zheng on 13-10-30.
 */
var Workspace = Backbone.View.extend({

    el: $('#app_home'),
    events: {
        "keypress #input_search": "search_page",
        "blur #input_search": "search_page"
    },
    initialize: function(){
        return this;
    },
    search_page: function(event){

        var value = $("#input_search").val().trim().toUpperCase();
        $(".book_thing").removeClass('focus');
        if(value){
            $("#hot-container").hide();
        }else{
            $("#input_search").attr('placeholder',"检索");
            $("#hot-container").show();
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