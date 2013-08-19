define(["jquery","application", "module/ajax_client" ,"bootstrap/bootstrap"], function($,application,client) {
    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
    $(function() {
    	application.navigationTo('home');

    	$('[img-load]').each(function(){

    		id = $(this).attr('img-load');
    		client.load_book(id,success);

    	});
    });

    function success(result,statusText,jqXHR){

    	$("[img-load='"+result.id+"']").attr('src',result.images.large);

    }

});