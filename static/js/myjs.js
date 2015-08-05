// I am so proud i wrote some js!
$(function(){
  $(".typed").typed({
	strings: [$(".typed").html()],
	typeSpeed: 10,
	showCursor: false,
	contentType: 'html',
  });
});
$( document ).ready(function() {
	console.log( "document loaded" );
});
