define(["jquery","application", "module/ajax_client" ,"bootstrap/bootstrap","flexpaper","flexpaper_handlers"], function($,application,client) {
    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
    $(function() {

    	client.load_book(bookid,success);
            $('#documentViewer').FlexPaperViewer(
                    { config : {
                             
                             SwfFile : escape('/static/doc/'+bookid+'.swf'),
                             localeChain: '/en_US/'
                }});
    
    });

    function success(result,statusText,jqXHR){

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