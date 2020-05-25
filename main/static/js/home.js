$(".swipeBtn").on("click",function(){
    console.log("click click");
    if($('.swiper-button-next').hasClass('swiper-button-disabled')){
            $('.swipeBtn').html("<a href='http://vishwastest.pythonanywhere.com/user/signup/'><div class='swiper-button-next swiper-button-disabled'></div></a>");
    }
});