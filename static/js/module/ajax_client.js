/*====================================
* VMS-Client Rest API client v0.0.1
* http://www.chinacloud.com.cn
* ====================================
* Copyright 2013 cetc32, Inc.
* Author: zhengyunlong
*====================================*/

define(["jquery"],function($){

    /**********************
    *** Jquery Ajax Utils
    ***********************/
    var _http_client = (function() {

	return {

	    ajax:function(option,success,error) {

		$.ajax($.extend(true,{},{

			type:"post",
			contentType:'application/json',
			timeout:1000000,
			error:function(jqXHR,textStatus,errorThrown){
				console.log(textStatus);
			}
			},option));
		}
	    }

    }());

    $(function(){

    	if(USER_ID!='None'){
    		_http_client.ajax({
    		type:'get',
            url:"/api/account/"+USER_ID,
            success:function(result,statusText,jqXHR){

			$("#account_info")
				.attr('title', result['name'])
				.attr('src', result['avatar']);


            },
            error:function(error,jqXHR){
                console.log(error);
            }
            });
    	}else{

    	}

     });

    return {

	test:function(success,error) {

		_http_client.ajax({
			url:'/v2/xxx',
			success:success,
			error:error
		});

	},
	/**load account info*/
	load_account:function(uid,success,error){

		_http_client.ajax({
			url:"/api/account/"+uid,
			success:success,
			error:error
		});

	},
	seach_book:function(keyword,success,error){

		fields = "?fields=id,title,publisher,author,isbn13,image"
		_http_client.ajax({

			url:"/api/book/search/"+keyword+fields,
			success:success,
			error:error,
			type:'get'

		})

	},
	load_book:function(bookid,success,error){

		url = "/api/book/"+bookid
		_http_client.ajax({

			url:url,
			success:success,
			error:error,
			type:'get'

		});
	}


    }

});
