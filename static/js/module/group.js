define(["jquery"], function($) {
    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
    $(function() {
        $("#publish-post-form").submit(function(){
            content = $("#editor").html();
            $("#editor_content").val(content);
        });
    });
});
