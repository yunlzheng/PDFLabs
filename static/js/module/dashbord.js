define(["jquery", "application","module/ajax_client","bootstrap/bootstrap","jquery.form"], function($,application,client) {
    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
    $(function() {
    	
    	application.navigationTo('dashbord');

            var options = {
                success:showResponse
            }

            $('#form-preview').ajaxForm(options); 

    	$("#btn_submit_form").click(function(){

    	       $("#form_regist").submit();
    	});

    	$("#txt_icon_file").change(function(){

    	       $("#form-preview").submit();

    	});
    });


    function showResponse(responseText, statusText, xhr, $form){

        $("#img-preview").attr('src',responseText);
        $("#form_icon_normal").attr('value',responseText)

    }

});