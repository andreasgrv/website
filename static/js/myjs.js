// I am so proud i wrote some js!
$(function() {
	$(".typed").hide();
});
$( document ).ready(function() {
	console.log( "document loaded" );
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
});
