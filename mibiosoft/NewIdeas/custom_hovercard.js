$(document).ready(function(){
	// Basic hovercard
	$('.basic-hovercard').popover({ 
		html : true,
		trigger: 'manual',
		placement: function (context, source) {
			var get_position = $(source).position();
			if (get_position.left > 515) {
				return "left";
			}
			if (get_position.left < 515) {
				return "right";
			}
			if (get_position.top < 110){
				return "bottom";
			}
			return "top";
		},
		content: function() {
			return $('.basic-content').html();   
		}
	}).on("click", function(e) {
		e.preventDefault();
	}).on("mouseenter", function() {
		var _this = this;
		$(this).popover("show");
		$(this).siblings(".popover").on("mouseleave", function() {
			$(_this).popover('hide');
		});
	}).on("mouseleave", function() {
		var _this = this;
		setTimeout(function() {
			if (!$(".popover:hover").length) {
				$(_this).popover("hide")
			}
		}, 100);
	});
	
	
	
	$('.advance-hovercard').popover({ 
		html : true,
		trigger: 'manual',
		placement: function (context, source) {
			var get_position = $(source).position();
			if (get_position.left > 515) {
				return "left";
			}
			if (get_position.left < 515) {
				return "right";
			}
			if (get_position.top < 110){
				return "bottom";
			}
			return "top";
		},
		content: function() {
			return $('.advance-content').html();   
		}
	}).on("click", function(e) {
		e.preventDefault();
	}).on("mouseenter", function() {
		var _this = this;
		$(this).popover("show");
		$(this).siblings(".popover").on("mouseleave", function() {
			$(_this).popover('hide');
		});
	}).on("mouseleave", function() {
		var _this = this;
		setTimeout(function() {
			if (!$(".popover:hover").length) {
				$(_this).popover("hide")
			}
		}, 100);
	});
});