$( document ).ready(function() {
    $(".typed").css("visibility", "hidden");
    setTimeout(function(){
      $(".typed").typed({
        strings: [$(".typed").html()],
        typeSpeed: 10,
        showCursor: false,
        contentType: 'html'
      });
    }, 100);
    setTimeout(function(){
        $(".typed").css("visibility", "visible");
    }, 300);
});
