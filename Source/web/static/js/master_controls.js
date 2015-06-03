/**
 * Created by liran.ben-gida on 5/27/2015.
 */

$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#loginBtn').on('click', submitLogin);
    $('#RegistrationSubmit').on('click', submitRegistration);
    $('#profilesettingsubmit').on('click',submitProfile );
});


function submitLogin() {
	var username = $('#loginUN').val();
	var password = $('#loginPSW').val();
	if (username == null || username == "" || password == null || password == "")
	{
		document.getElementById("errorText").innerHTML = "Please fill both fields.";
		return;
	}
	else
	{
		document.getElementById("errorText").style.color = "green";
		document.getElementById("errorText").innerHTML = "Logging in...";
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
			document.getElementById("errorText").style.color = "red";
			document.getElementById("errorText").innerHTML = xhr.responseText;
			console.error(xhr, status, error);
		}
		});
	}
}

function submitNewEntry()
{
	var description = $('#desc-textbox').val();
	var price = $('#price-textbox').val();
	var tagname = $('#tag-combobox option:selected').val();
	var budgetId = $('#budgetId').val();
	if (isNumber(price) == false)
	{
		document.getElementById("errorText").innerHTML = "Price must be a positive number."
		return;
	}
	if (tagname == "disabled")
	{
		document.getElementById("errorText").innerHTML = "No tag was selected."
		return;
	}
	if (description.length == 0)
	{
		document.getElementById("errorText").innerHTML = "The description field is mandatory."
		return;
	}
	else
	{
		$('#addBudgetEntry').attr('disabled', 'disabled');
		$.ajax({
		url:'/SubmitEntry',
		type:'GET',
		dataType:'json',
		data:{description: description, price:price, tagname: tagname, budgetId: budgetId},
		success:function(data, status, xhr)
		{
			document.location.href = '/Budget/' + budgetId;

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
    var FirstName = $('#FirstName').val();
    var LastName = $('#LastName').val();
    var email = $('#email').val();
    var BirthMonth = $('#BirthMonth').val();
    var BirthDay = $('#BirthDay').val();
    var BirthYear = $('#BirthYear').val();
    var gender = $('#gender').val();
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
		data:{username:username, password:password, FirstName:FirstName, LastName:LastName, email:email, BirthMonth:BirthMonth, BirthDay:BirthDay, BirthYear:BirthYear, gender:gender},
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

function submitProfile() {
    var FirstName = $('#FirstName').val();
    var LastName = $('#LastName').val();
    var email = $('#email').val();
    var BirthMonth = $('#BirthMonth').val();
    var BirthDay = $('#BirthDay').val();
    var BirthYear = $('#BirthYear').val();
    var gender = $('#gender').val();
	var password = $('#password').val();
    var oldpassword = $('#oldpassword').val();
	if (password == null || password == "")
	{
		alert("There appears to be a field missing from the form.");
	}
	else
	{
		$.ajax({
		url:'/RegistrationCheck',
		type:'GET',
		dataType:'json',
		data:{oldpassword:oldpassword, password:password, FirstName:FirstName, LastName:LastName, email:email, BirthMonth:BirthMonth, BirthDay:BirthDay, BirthYear:BirthYear, gender:gender},
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

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

