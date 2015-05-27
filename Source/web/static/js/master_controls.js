/**
 * Created by liran.ben-gida on 5/27/2015.
 */
$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#login').on('click', submitLogin);
});

function submitLogin() {
	var username = $('#loginUN').val();
	var password = $('#loginPSW').val();
	$.ajax({
		url:'/LoginCheck',
		type:'GET',
		dataType:'json',
		data:{username:username, password:password},
		success:function(data, status, xhr)
		{
			document.location.href = '/Budgets';
			//location.reload();
		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}