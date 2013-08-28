 //保存搜索的图书对象
var books;

function iWant(id){

	var book = books[id];	
	$("#contribute-book-id").val(book.id);     
	$("#contribute-book-title").val(book.title);     
	$("#contriibute-book-image").val(book.image);     
	$("#contribute-book-isbn13").val(book.isbn13);     
	$("#contribute-book-publisher").val(book.publisher);
        alert("iWant");


}

function iHave(id){

	var book = books[id];	
	console.log(book);
	$(".info-book-name").each(function(){
		$(this).val(book.title);	
	});;
	$("#contribute-book-id").val(book.id);     
	$("#contribute-book-title").val(book.title);     
	$("#contriibute-book-image").val(book.image);     
	$("#contribute-book-isbn13").val(book.isbn13);     
	$("#contribute-book-publisher").val(book.publisher);    

}


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

          var json = $.parseJSON(result);
          books = json.books;
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
                "<a id='want-"+i+"' value='"+book.title+"'' class='btn btn-success'>我想要</a>"+
                "<button class='btn btn-success dropdown-toggle' data-toggle='dropdown'>"+
              "<span class='caret'></span></button><ul class='dropdown-menu'>"+
                  "<li><a id='have-"+i+"' data-toggle='modal' href='#myModal'>我有</a></li>"+
                "</ul>"+
              "</div></div>"+
                  "</div><br/>"

                $("#books").append(str);

                (function(i){

                    $("#have-"+i).click(function(){

                       iHave(i);

                    });

		    $("#want-"+i).click(function(){

                       iWant(i);

                    });

                })(i);

                application.hide_alert();
              
           }
    }

});
