/**
 * Created by zheng on 13-11-1.
 * 从1开始 至 任意值     parseInt(Math.random()*上限+1);
 * parseInt(Math.random()*(上限-下限+1)+下限);
 */
$(function(){
    
    var tpl_gallery_box = $("#tpl_gallery_box").html();
    var $container = $("#gallery");
    var rotate_top = 60;
    var rotate_limit = -60;
    var position_top = 300;
    var position_left = $container.innerWidth()-110;//减去相框自身长度
    $.ajax({
        url:"/gallery/api",
        success:function(data, textStatus, jqXHR){
                for(var i= 0; i<data.length; i++){
                    var rotate = parseInt(Math.random()*(rotate_top-rotate_limit+i)+rotate_limit);
                    var top = parseInt(Math.random()*position_top+i);
                    var left = parseInt(Math.random()*position_left+i);
                    var gallery = data[i];
                    var gallery_box = $(tpl_gallery_box)[0];
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

    var params = {
        left: 0,
        top: 0,
        currentX: 0,
        currentY: 0,
        flag: false
    };

    var $target = null;

    var startDrop = function(e){

        var nowX = e.clientX;
        var nowY = e.clientY;
        var disX = nowX - params.currentX;
        var disY = nowY - params.currentY;

        var left = parseInt(params.left) + disX + "px";
        var top = parseInt(params.top) + disY + "px";

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
