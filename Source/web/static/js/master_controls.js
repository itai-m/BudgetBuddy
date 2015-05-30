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

function submitNewEntry()
{
	var description = $('#desc-textbox').val();
	var price = $('#price-textbox').val();
	var tagname = $('#tag-combobox option:selected').text();
	var budgetId = $('#budgetId').val();

	if (false)
	{
		alert("There appears to be a field missing from the form.");
	}
	else
	{
		$.ajax({
		url:'/SubmitEntry',
		type:'GET',
		dataType:'json',
		data:{description: description, price:price, tagname: tagname, budgetId: budgetId},
		success:function(data, status, xhr)
		{
			document.location.href = '/Budgets';

		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
		});
	}

	
}
function submitRegistration() {
    var FirstName = $('FirstName').val();
    var LastName = $('LastName').val();
    var email = $('email').val();
    var BirthMonth = $('BirthMonth').val();
    var BirthDay = $('BirthDay').val();
    var BirthYear = $('BirthYear').val();
    var gender = $('gender').val();
	var username = $('#username').val();
	var password = $('#password').val();
	if (username == null || username == "" || password == null || password == "")
	{
		alert("There appears to be a field missing from the form.");
	}
	else
	{
		$.ajax({
		url:'/RegistrationCheck',
		type:'GET',
		dataType:'json',
		data:{username:username, password:password},
		success:function(data, status, xhr)
		{
			document.location.href = '/Registration';

		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
		});
	}
}