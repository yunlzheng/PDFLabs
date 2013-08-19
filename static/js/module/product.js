define(["jquery","application", "module/ajax_client" ,"bootstrap/bootstrap"], function($,application,client) {
    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
   $(function() {
    	
    	application.navigationTo('dashbord');

    	$('#btn_trash').click(function(e){

	       e.preventDefault();
	       $('#modal_sure').modal()

    	});

    	$("#btn_trash_sure").click(function(e){

    	       e.preventDefault();
    	       client.removeApp(appKey,
    	       	function(result,statusText,jqXHR){

	       	    if(result['code']=='000000'){
	       	    	$('#modal_sure').modal('hide');
	       	    	location.href="../dashbord"
	       	    }else{
	       	    	alert("delete error")
	       	    }
    	       		
    	       	},function(jqXHR,textStatus,errorThrown){
    	       		alert("delete error")
    	       	}
    	       )
    	       

    	});

    });
});