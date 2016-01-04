// I am so proud i wrote some js!
$(function() {
	$(".typed").hide();
});

$( document ).ready(function() {
	setTimeout(function(){
	  $(".typed").typed({
		strings: [$(".typed").html()],
		typeSpeed: 10,
		showCursor: false,
		contentType: 'html',
	  });
	}, 100);
	setTimeout(function(){
		$(".typed").show();
	}, 300);
    $( ".nav li" ).mouseenter(function() {
        console.log("got here!");
        $( this ).siblings().each(function() {
            if ($( this ).hasClass("active")) {
                $( this ).removeClass("active").addClass("inactive");
            }
        });
    });
    $( ".nav li" ).mouseleave(function() {
        $( this ).siblings().each(function() {
            if ($( this ).hasClass("inactive")) {
                $( this ).removeClass("inactive").addClass("active");
            }
        });
    });
});
