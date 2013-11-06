$(function(){

	$.ajax({
      type:"get",
      url:"/api/book/"+bookid,
      contentType:'application/json',
      success: load_success,
      error:function(jqXHR,textStatus,errorThrown){
        console.log(textStatus);
      }
  });

	$("#btn_ilike").click(function(){

        $("#btn_like_icon").attr("disabled",true);
        $.ajax({
          type:"post",
          url:"/api/like/"+bookid,
          success:function(result,statusText,jqXHR){
              if(jqXHR.responseText.indexOf("登录")!=-1){
                    window.location="/sigin?next="+window.location.pathname;
              }else{

                    $("#btn_like_icon").attr("disabled",false);
                    _class = $("#btn_like_icon").attr('class')

                    if(_class=="icon-heart-empty"){
                        $("#btn_like_icon")
                            .removeClass("icon-heart-empty")
                            .addClass("icon-heart");
                    }else{

                        $("#btn_like_icon")
                            .removeClass("icon-heart")
                            .addClass("icon-heart-empty");
                    }
              }
          },
          error:function(error,jqXHR){
              $("#alert-error").show();
              setTimeout(function(){
                $("#alert-error").hide(1000);
              },2000)
          }
      });

  });


	function load_success(result,statusText,jqXHR){

        $("#book_img").attr('src',result.images.large);
        $("#book_authors").empty().append('<b>作者:</b>');
        for(var i=0;i<result.author.length;i++){
           $("#book_authors").append('<span>'+result.author[i]+'</span>&nbsp;');
        }
        $("#book_subtitle").text(result.subtitle);
        $("#book_publisher").text(result.publisher);
        $("#book_pubdate").text(result.pubdate);
        $("#book_isbn13").text(result.isbn13);
        $("#book_summary").text(result.summary);

        for(var i=0;i<result.tags.length;i++){
            var tag = result.tags[i];
            $("#book_tags").append('<span class="label">'+tag.name+'</span>&nbsp;');
        }

    }

});
