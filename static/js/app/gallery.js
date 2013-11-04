/**
 * Created by zheng on 13-11-1.
 * 从1开始 至 任意值     parseInt(Math.random()*上限+1);
 * parseInt(Math.random()*(上限-下限+1)+下限);
 */
$(function(){
    var tpl_gallery_box = $("#tpl_gallery_box").html();
    var $container = $("#gallery");
    var rotate_top = 50;
    var rotate_limit = -50;
    var position_top = 300;
    var position_left = $container.innerWidth()-210;//减去相框自身长度
    $.ajax({
        url:"/gallery/api",
        success:function(data, textStatus, jqXHR){
                for(var i= 0; i<data.length; i++){
                    var rotate = parseInt(Math.random()*(rotate_top-rotate_limit+i)+rotate_limit);
                    var top = parseInt(Math.random()*position_top+i);
                    var left = parseInt(Math.random()*position_left+i);
                    var gallery = data[i];
                    var tpl = tpl_gallery_box
                        .replace("{type}",gallery['type'])
                        .replace("{name}", gallery['name']);
                    var gallery_box = $(tpl)[0];
                    gallery_box.setAttribute("id", gallery._id.$oid);
                    $container.append(gallery_box);
                    $(gallery_box).css({
                        "top":top,
                        "left":left,
                        "background-image":"url('"+gallery['avatar']+"')",
                        "background-repeat":"no-repeat no-repeat",
                        "background-position":"50% 50%",
                        "transform": "rotate("+rotate+"deg)",
                        "-webkit-transform":"rotate("+rotate+"deg)",
                        "z-index":i
                    });
                }
        },
        error: function(jqXHR, textStatus, error){}
    });

    //TODO: 用户信息
    $("body").delegate('.gallery_box','mouseenter mouseleave', function(e){
        var id = $(this).attr('id');
        if(e.type=="mouseenter"){
            $(this).find('.gallery_ajax').fadeIn(500);
        }else{
            $(this).find('.gallery_ajax').fadeOut(500);
        }
    });

    //TODO: 头像拖动

    var params = {
        left: 0,
        top: 0,
        currentX: 0,
        currentY: 0,
        flag: false
    };

    var $target = null;

    var startDrop = function(e){

        return false;

    }


    $("body").delegate(".gallery_box", "mousedown", function(e){

         params.currentX = e.clientX;
		 params.currentY = e.clientY;

        $target = $(this);
        $(this).bind("mousemove",startDrop);
        return false;

    });


    $("body").delegate(".gallery_box", "mouseup", function(){

        $(this).unbind("mousemove", startDrop);
        return false;

    });


});
