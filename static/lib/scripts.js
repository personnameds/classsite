$(document).ready(function() {
	
	$('#nav li:has(> ul)').hover(
	function() {
		$('ul', this).stop().animate({'height': ($('li', this).length * 40) + 'px'}, 500, "easeOutCubic");
		$('ul', this).css('border-style', 'none solid solid solid');
	},
	function() {
		$('ul', this).stop().animate({'height':'0px'}, 400, "easeOutSine", function() {$(this).css('border-style', 'none')});
	}
	);
	
	$('#to_top').hide(0);
	
	$(window).scroll(function() {
		if ($(this).scrollTop() != 0) {
			$('#to_top').fadeIn();
		} else {
			$('#to_top').fadeOut();
		}
	});
	
	$('#nav li:has(ul)').children('a').append('<span class="arrow"></span>');

	
	$('#to_top').click(function() {
		$('html, body').animate({scrollTop:0});
	});	
	
	$('#event-thumbs li:has(.thumb-text)').hover(
	function() {
		$('.thumb-text', this).stop().animate({'bottom': '0px'}, 300, "easeOutSine");
	},
	function() {
		$('.thumb-text', this).stop().animate({'bottom': '-200px'}, 400, "easeOutSine");
	}
	);
	
	if ($('#footer .credit1').length == 0) {
		$("#footer").prepend("<span class='credit1'><a href='http://sasha.yaro.cc' target='_blank'>Design and Development: Sasha Y.</a></span>");
	}
	
	if (!($('#footer .credit1').find == "<a href='http://sasha.yaro.cc' target='_blank'>Design and Development: Sasha Y.</a>")) {
		$("#footer .credit1").html("<a href='http://sasha.yaro.cc' target='_blank'>Design and Development: Sasha Y.</a>");
	}
});