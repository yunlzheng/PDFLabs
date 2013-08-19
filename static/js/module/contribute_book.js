define(["jquery","application", "module/ajax_client" ,"bootstrap/bootstrap"], function($,application,client) {
    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
    $(function() {
    	
    	$("#btn_search").click(function(){

    		var keyword = $("#txt_key").val();
             application.alert('Loading...')
    		client.seach_book(keyword,success)
    		 
    	});

      $("#contribute-submit").click(function(){

              $("#form-contribute").submit()

      });

    });

    function success(result,statusText,jqXHR){

           json = $.parseJSON(result)
          $("#books").empty()
           for(var i=0;i<json.books.length;i++){
                var book = json.books[i]
                var str = "<div class='well row-fluid'>"+
                  "<div class='span2'><img src='"+book.image+"'></div>"+
                  "<div class='span8'>"+
                    "<h4>"+book.title+"</h4>"+
                    "<label><b>作者</b>:"+book.author+"</label>"+
                    "<label><b>出版社</b>:"+book.publisher+"</label>"+
                    "<label><b>ISBN</b>:"+book.isbn13+"</label>"+
                  "</div>"+
                  "<div class='span2'><div class='btn-group'>"+
                "<a id='"+book.id+"' value='"+book.title+"'' class='btn btn-success'  href='#myModal'  data-toggle='modal'>共享资源</a>"+
                "<button class='btn btn-success dropdown-toggle' data-toggle='dropdown'><span class='caret'></span></button>"+
              "</div></div>"+
                  "</div><br/>"

                $("#books").append(str);

                (function(){

                    $("#"+book.id).click(function(){

                        var id = $(this).attr('id');
                        var title= $(this).attr('value');
                        $("#contribute-book-id").val(id)
                        $("#contribute-book-title").val(title)

                    });

                })(book.id);

                application.hide_alert();
              
           }
    }

});
