var toastCount = 0;

function createToast(message, autoclose = true, duration = 2000){
    var id = 'toast'+parseInt($('atoast-container').length + 1);
    var toast = '<div id="'+id+'" class="atoast-container"><div class="atoast">'+message+'</div></div>';


    //var toastCount = $('.atoast-container').length;

    if(toastCount < 1){
        toastCount++;
        $('body').append(toast);
    }
    else{
        pushToastsUp();
        setTimeout(function(){
            $('body').append(toast);
        }, 300 * toastCount);
    }

    TweenMax.from('#'+id, .3, {y:50});

    if(autoclose){
        setTimeout(function(){
            hideToast(id);
            toastCount--;
        }, duration);
    }else{
        return id;
    }
}

function pushToastsUp(){
    var toastsArray = $('.atoast-container').length;

    $('.atoast-container').each(function(index, el) {
        if($('this').css('opacity') !== 0){
            id = $(this).prop('id');
            var newTop = $('#'+id).position().top - $('#'+id).height() - 10;

            $('#'+id).css({top : newTop}, 350);
            // console.log();
            // TweenMax.to('#'+id, .3, {y:-180});
        }
    });
}

function hideToast(toastId, duration = 300, down = false){
    var duration = duration / 1000;

    if(!down)
        TweenMax.to('#'+toastId+'', duration, {y:-50, opacity: 0});
    else
        TweenMax.to('#'+toastId+'', duration, {y:+50, opacity: 0});

    setTimeout(function(){
        $('#'+toastId+'').remove();
    }, 200);
}

// OPEN FEEDBACK MODAL
function sendFeedback(){
    $('#contact-modal').openModal();
}

$('.js-menu-shower').click(function(e){
    var target = $(this).data('target');
    var dynamicPositioning = $('#'+target).hasClass('static-menu');

    if(!dynamicPositioning){
        var topPos = $(this).position().top + $(this).parent().offset().top - $(window).scrollTop();
        var leftPos = $(this).position().left + $(this).parent().position().left;
        var cardPos = $(this).offset().top;

        var botEdge = $(window).scrollTop() + window.innerHeight - 200;
        var fromBot = cardPos - botEdge;
        var toSroll = $(window).scrollTop() + fromBot;

        if(fromBot > 0){
            $('body').scrollTo(toSroll, 500, { axis:'y' });
            setTimeout(function(){
                $("#"+target).find('.some-menu').css({top: topPos + 15 - fromBot, left: leftPos - 200});
                $("#"+target).show();

                setTimeout(function(){
                    $("#"+target).find('.some-menu').addClass("open");
                });
            }, 600);
        }else{
            fromBot = 0;
            $("#"+target).find('.some-menu').css({top: topPos + 15 - fromBot, left: leftPos - 200});
            $("#"+target).show();

            setTimeout(function(){
                $("#"+target).find('.some-menu').addClass("open");
            });
        }
    }else{
        $("#"+target).find('.some-menu').css({top: topPos + 15 - fromBot, left: leftPos - 200});
        $("#"+target).show();

        setTimeout(function(){
            $("#"+target).find('.some-menu').addClass("open");
        });
    }
});

$('.some-menu-container').click(function(){
    var mimi = $(this);
    var menu = $(this).find('.some-menu');
    $(this).find('.some-menu').removeClass("open");

    setTimeout(function(){
        mimi.hide();
    });
});

$(window).scroll(function(){
    $('.some-menu-container').each(function(){
        var mimi = $(this);
        var menu = $(this).find('.some-menu');
        $(this).find('.some-menu').removeClass("open");

        setTimeout(function(){
            mimi.hide();
        });
    });
});

$.fn.followTo = function ( elem ) {
    var $this = this,
        $elem = $(elem),
        $window = $(window),
        $bumper = $(elem),
        bumperPos = 400,
        thisHeight = $this.outerHeight(),
        setPosition = function(){
            if ($window.scrollTop() > (bumperPos - thisHeight)) {
                $elem.addClass('show-tabs');
                $('.sidemenu').css({'padding-top' : 110+'px'}, 200);
            } else {
                $elem.removeClass('show-tabs');
                $('.sidemenu').css({'padding-top' : 60+'px'}, 200);
            }
        };
    $window.resize(function()
    {
        //bumperPos = elem.offset().top;
        //thisHeight = $this.outerHeight();
        setPosition();
    });
    $window.scroll(setPosition);
    setPosition();
};