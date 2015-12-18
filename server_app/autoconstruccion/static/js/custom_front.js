$(function() {

    $('#login-form-link').click(function(e) {
		$("#login_form").delay(100).fadeIn(100);
 		$("#register_form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	
	$('#register-form-link').click(function(e) {
		console.log("register")
		$("#register_form").delay(100).fadeIn(100);
 		$("#login_form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	  

	$('.slider').slider().on('slide', function(ev){
		console.log(ev)
		console.log($(this).parent().parent())
		if(ev.value>0)
	    	$(this).parent().parent().find('.desc-text').html("nuevo mensaje")
	});
});