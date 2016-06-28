$(".typed").css("visibility", "hidden");
$(".typed2").css("visibility", "hidden");
$( document ).ready(function() {
    setTimeout(function(){
      $(".typed").typed({
        strings: [$(".typed").html()],
        typeSpeed: 20,
        showCursor: false,
        contentType: 'html'
      });
    }, 100);
    setTimeout(function(){
        $(".typed").css("visibility", "visible");
    }, 250);
    setTimeout(function(){
      $(".typed2").typed({
        strings: [$(".typed2").html()],
        typeSpeed: 20,
        showCursor: false,
        contentType: 'html'
      });
    }, 3000);
    setTimeout(function(){
        $(".typed2").css("visibility", "visible");
    }, 3150);
});
