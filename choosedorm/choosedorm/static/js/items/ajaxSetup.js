//在 其他使用 .ajax的模块 函数运行前，这段代码先运行，就将jQuery返回的对象修改设置了
define(["jquery"], function ($) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

//设置 url, beforeSend
    $.ajaxSetup({
	url:"/choosedorm/",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));  
        }
    });
});
