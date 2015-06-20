$(".controlTd").click(function () {
  $(this).children(".settingsIcons").toggleClass("display");
  $(this).children(".settingsIcon").toggleClass("openIcon");
});
$(function() {
    var moveLeft = 0;
    var moveDown = 0;
    var timeout;
    $('a.popper').hover(function(e) {

        var target = '#' + ($(this).attr('data-popbox'));

        $(target).show();
        moveLeft = $(this).outerWidth();
        moveDown = ($(target).outerHeight() / 2);
    }, function() {
        var target = '#' + ($(this).attr('data-popbox'));
        $(target).hide();
    });

    $('a.popper').mouseenter(function(e) {

        var target = '#' + ($(this).attr('data-popbox'));

        leftD = e.pageX-250;
        topD = e.pageY - parseInt(moveDown);
        maxBottom = parseInt(e.pageY + parseInt(moveDown) + 20);
        windowBottom = parseInt(parseInt($(document).scrollTop()) + parseInt($(window).height()));
        maxTop = topD;
        windowTop = parseInt($(document).scrollTop());
        if(maxBottom > windowBottom)
        {
            topD = windowBottom - $(target).outerHeight() - 20;
        } else if(maxTop < windowTop){
            topD = windowTop + 20;
        }
        $(target).css('top', topD).css('left', leftD);

    });
});