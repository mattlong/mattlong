// based on http://benalman.com/projects/run-jquery-code-bookmarklet/
(function(e,a,g,h,f,c,b,d){if(!(f=e.jQuery)||g>f.fn.jquery||h(f)){c=a.createElement("script");c.type="text/javascript";c.src="http://ajax.googleapis.com/ajax/libs/jquery/"+g+"/jquery.min.js";c.onload=c.onreadystatechange=function(){if(!b&&(!(d=this.readyState)||d=="loaded"||d=="complete")){h((f=e.jQuery).noConflict(1),b=1);f(c).remove()}};a.documentElement.childNodes[0].appendChild(c)}})(window,document,"1.7.2",function($,L){

    var l = document.location;
    var title = document.title;
    var url = l.href;
    var metaurl = null;

    // http://news.ycombinator.com/item?id=4245982
    if (l.hostname === 'news.ycombinator.com' && l.pathname === "/item") {
        metaurl = url;
        suffix = ' | Hacker News';
        if (title.indexOf(suffix) + suffix.length === title.length) {
            title = title.substring(0,title.indexOf(suffix));
        }
        url = $('td.title a').attr('href');
    }

    $.ajax({
          url: "//mattlong.org:8000/bookmarks/add",
          data: {title:title, url:url, metaurl:metaurl},
          success: onBookmarkAdd,
          dataType: "jsonp"
    });

    function onBookmarkAdd(data, textStatus, jqXHR) {
        var message, color;
        if (data['status'] === 'ok') {
            message = "Groovy, baby!";
            color = '#0a0';
        } else {
            message = "Oh noes!";
            color = '#a00';
        }

        var style = 'color:black;font-weight:bold;position:fixed;top:20px;left:20px;margin:0;padding:10px;background-color:'+color+';border:3px solid #333';
        var html = '<div style="'+style+'">'+message+'</div>';

        $(html).appendTo('body').fadeOut(4000, function() {
            console.warn("YO");
        });
    }
});
