// This is this the js file for global functions
$(document).ready(function () {
	$('.page-scroll').bind('click', function(event) {
		var $anchor = $(this);
		$('html, body').stop().animate({
			scrollTop: $($anchor.attr('href')).offset().top
		}, 750);
		event.preventDefault();
		window.history.pushState(null, null, $($anchor.attr('href')).selector);
	});
});
