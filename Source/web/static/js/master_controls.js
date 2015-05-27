/**
 * Created by liran.ben-gida on 5/27/2015.
 */

$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#loginBtn').on('click', submitLogin);
});


function submitLogin() {
	var username = $('#loginUN').val();
	var password = $('#loginPSW').val();
	if (username == null || username == "" || password == null || password == "")
	{
		alert("There appears to be a field missing from the form.");
	}
	else
	{
		$.ajax({
		url:'/LoginCheck',
		type:'GET',
		dataType:'json',
		data:{username:username, password:password},
		success:function(data, status, xhr)
		{
			//location.reload();
			document.location.href = '/Budgets';
			//window.location='/Budgets';

		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
		});
	}
}