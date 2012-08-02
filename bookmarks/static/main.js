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

    var style = 'font-size:16px;font-family:verdana;color:black;font-weight:bold;position:fixed;top:20px;left:20px;margin:0;padding:10px;background-color:lightGreen;border:3px solid #333';
    var inputStyle = 'font-size:16px;font-family:verdana;padding:1px;';
    var html = '<div style="'+style+'">tags: <input style="'+inputStyle+'" class="ml-tag-input" type="text" /></div>';

    var addBookmarkTimeout = setTimeout(function(){addBookmark();},5000);

    var jBox = $(html).appendTo('body').find('.ml-tag-input').focus().on('keyup change', function(e) {
        clearTimeout(addBookmarkTimeout);
        if (e.keyCode === 13) {
            var tags = $(this).val();
            addBookmark(tags);
        }
    }).end();

    var addBookmarkCalled = false;
    function addBookmark(tags) {
        if (addBookmarkCalled) { /*return;*/ }

        addBookmarkCalled = true;
        var data = {'title':title, 'url':url, 'metaurl':metaurl};
        if (tags) { data['tags'] = tags; }

        $.ajax({
              url: "//"+window.mlong_host+"/bookmarks/add",
              data: data,
              success: onBookmarkAdd,
              dataType: "jsonp"
        });
        jBox.html('calculating...');
    }

    function onBookmarkAdd(data, textStatus, jqXHR) {
        var message, color;
        if (data['status'] === 'ok') {
            message = "Groovy, baby!";
            color = '#0a0';
        } else {
            message = "Oh noes!";
            color = '#a00';
        }

        jBox.html(message).css({'background-color':color}).fadeOut(4000, function() {

        });
    }
});
