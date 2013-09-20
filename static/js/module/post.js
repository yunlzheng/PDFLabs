define(["jquery"], function($) {
    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
    $(function() {

        $("#publish-post-form").submit(function(){
            content = $("#editor").html();
            $("#editor_content").val(content);
            $("#publish-post-form").submit();
            return false;
        });

        $("#btn-create").click(function(){

            $("#post-mode").val('new');
            $("#editor").html("");
            $("#post_title").val("");
            $("#model_title").val("发表帖子");
            $("#model_title").val("编辑帖子");

        });

        $("#btn-edit").click(function(){
            $("#post-mode").val('update');
            content = $("#old_post_content").html();
            title=$("#old_post_title").text();
            $("#editor").html(content);
            $("#post_title").val(title);
        });

        $("#btn_delete_post").click(function(){

            if(confirm("确认删除本帖？")){
                $.ajax({
                    url:'',
                    method:'delete',
                    success:function(){
                        location.reload();
                    },
                     error:function(){
                        location.reload();
                     }
                });

            }

        });

    });
});
