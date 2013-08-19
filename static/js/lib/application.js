define(["jquery"], function($) {
    
    var navigation = $("#main_nav");

    return {
    	
    	navigationTo:function(dataitem){

    		navigation.find('li').each(function(){

    			var item = $(this);
    			var href = item.find('a').attr('href');
                                      if(dataitem){
                                            if(href.indexOf(dataitem)!=-1){
                                                item.addClass('active');
                                            }else{
                                                item.removeClass('active');
                                            }
                                      }
    			
    			

    		});

    	},
             alert:function(message,error){

                if(error){
                    $("#ajax_message").addClass('err');
                }else{
                    $("#ajax_message").removeClass('err')
                }
                $("#ajax_message").text(message).fadeIn(500);

             },
             hide_alert:function(){

                $("#ajax_message").empty().fadeOut(400);

             }

    }

});