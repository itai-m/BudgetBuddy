$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#loginBtn').on('click', submitLogin);
	$('#RegistrationSubmit').on('click', submitRegistration);

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
function submitEditedEntry()
{
	var description = $('#desc-textbox').val();
	var price = $('#price-textbox').val();
	var tagname = $('#tag-combobox option:selected').val();
	var budgetId = $('#budgetId').val();
	var entryId = $("#entryId").val();
	if (isNumber(price) == false)
	{
		document.getElementById("errorText").innerHTML = "Price must be a positive number.";
		return;
	}
	if (tagname == "disabled")
	{
		document.getElementById("errorText").innerHTML = "No tag was selected.";
		return;
	}
	if (description.length == 0)
	{
		document.getElementById("errorText").innerHTML = "The description field is mandatory.";
		return;
	}
	else
	{

		document.getElementById("editBudgetEntry").disabled = true;
		$.ajax({
			url:'/SubmitEditedEntry',
			type:'GET',
			dataType:'json',
			data:{description: description, price:price, tagname: tagname, budgetId: budgetId, entryId: entryId},
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
		document.getElementById("editBudgetEntry").disabled = false;
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
		document.getElementById("errorText").innerHTML = "Price must be a positive number.";
		return;
	}
	if (tagname == "disabled")
	{
		document.getElementById("errorText").innerHTML = "No tag was selected.";
		return;
	}
	if (description.length == 0)
	{
		document.getElementById("errorText").innerHTML = "The description field is mandatory.";
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
	var repassword =$('#repassword').val();
	if (BirthMonth == -1)
	{
		alert("Invalid Month Name");
		return false;
	}
	var js_date = new Date(parseInt(BirthYear),parseInt(BirthMonth),parseInt(BirthDay),0,0,0,0);
	if (username == null || username == "" || password == null || password == "")
	{
		alert("There appears to be a missing field");
	}
	else if (repassword != password)
	{
		alert("Password don't match");
	}
	else if (!((js_date.getUTCDate() == BirthDay-1)|| (BirthDay==1)) || (js_date.getFullYear() != BirthYear) || (js_date.getFullYear() != BirthYear))
	{
		alert("Wrong Date Input");
	}
	else if (gender==null)
	{
		alert("Wrong Gender Input");
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
function removeEntry(entryId,budgetId) {
	$.ajax({
		url:'/RemoveEntryFromBudget',
		type:'GET',
		dataType:'json',
		data:{entryId: entryId, budgetId:budgetId},
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
function removeBudget(budgetId) {
	$.ajax({
		url:'/RemoveBudgetFromBudget',
		type:'GET',
		dataType:'json',
		data:{budgetId:budgetId},
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
function ExitBudget(budgetId) {
	$.ajax({
		url:'/ExitBudget',
		type:'GET',
		dataType:'json',
		data:{budgetId:budgetId},
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
	var repassword =$('#repassword').val();
	var js_date = new Date(parseInt(BirthYear),parseInt(BirthMonth),parseInt(BirthDay),0,0,0,0);

	if (repassword!=password)
	{
		alert("passwords don't matching");
	}
	else if (!((js_date.getUTCDate() == BirthDay-1)|| (BirthDay==1)) || (js_date.getFullYear() != BirthYear) || (js_date.getFullYear() != BirthYear))
	{
		alert("Wrong Date Input");
	}
	else
	{
		$.ajax({
			url:'/ProfileSettingsCheck',
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
// Create Budget page functions.
function usernameExist()
{
	var usernameExist = $('#checkUsernameExist').val();
	$.ajax({
		url:'/CreateCheck',
		type:'GET',
		dataType:'json',
		data:{username: usernameExist},
		success:function(data, status, xhr)
		{
			document.getElementById("usernameExistField").style.color = "green";
			document.getElementById("usernameExistField").innerHTML = "Username exist!"
		},
		error:function(xhr, status, error)
		{
			document.getElementById("usernameExistField").style.color = "red";
			document.getElementById("usernameExistField").innerHTML = "Username doesnt exist!"
			console.error(xhr, status, error);
		}
	});
}
function addRow()
{

	var username = $('#checkUsernameExist').val();
	document.getElementById("Add").disabled = true;
	if (checkBudgeteerInTable(username))
	{
		document.getElementById("usernameExistField").style.color = "red";
		document.getElementById("usernameExistField").innerHTML = "Budgeteer already exist in table!";
		document.getElementById("Add").disabled = false;
		return;
	}
	$.ajax({
		url:'/CreateCheck',
		type:'GET',
		dataType:'json',
		data:{username: username},
		success:function(data, status, xhr)
		{
			tableID = 'budgeteerTable';
			var table=document.getElementById(tableID);
			var rowCount=table.rows.length;
			var row=table.insertRow(rowCount);
			var cell1=row.insertCell(0);
			cell1.innerHTML = rowCount;
			var cell2=row.insertCell(1);
			cell2.innerHTML = username;
			var cell3=row.insertCell(2);
			if($('#partner').is(':checked')) { cell3.innerHTML = "Budget Partner"; }
			if($('#viewer').is(':checked')) { cell3.innerHTML = "Budget Viewer"; }
			var cell4=row.insertCell(3);
			cell4.innerHTML =  '<button type="button" class="btn btn-danger btn-cons" onclick="delRow(\'' + username + '\');">Remove</button>';
		},
		error:function(xhr, status, error)
		{
			document.getElementById("usernameExistField").style.color = "red";
			document.getElementById("usernameExistField").innerHTML = "Username doesnt exist!";
			console.error(xhr, status, error);
		}
	});
	document.getElementById("Add").disabled = false;

}
function delAllRowsFromChatTable(tableID){
	var table=document.getElementById(tableID);
	var rowCount=table.rows.length;
	while(table.rows.length >0)
	{
		table.deleteRow(0);
	}
}
function delRow(username){
	tableID = 'budgeteerTable';
	var table=document.getElementById(tableID);
	var rowCount=table.rows.length;
	for(var i=0;i<rowCount;i++)
	{
		var row=table.rows[i];
		var text=row.cells[1].innerHTML;
		if(username.localeCompare(text) == 0)
		{
			table.deleteRow(i);
			reorderRows();
			return;
		}
	}

}
function reorderRows()
{
	tableID = 'budgeteerTable';
	var table=document.getElementById(tableID);
	var rowCount=table.rows.length;
	for(var i=0;i<rowCount;i++)
	{
		if (i == 0)
		{
			continue;
		}
		var row=table.rows[i];
		row.cells[0].innerHTML = i;
	}
}
function checkBudgeteerInTable(username){
	tableID = 'budgeteerTable';
	var table=document.getElementById(tableID);
	var rowCount=table.rows.length;
	for(var i=0;i<rowCount;i++)
	{
		var row=table.rows[i];
		var text=row.cells[1].innerHTML;
		if(username.localeCompare(text) == 0)
		{
			return true;
		}
	}
	return false;
}
function submitBudget(urladdress)
{
	budgetName = $('#budgetName').val();
	tagList = getCheckedTags(); // [tag],[tag],[tag] string
	participantList = getParticipants(); // [participant name]:[permission],[participant name][[:permission]
	$.ajax({
		url:urladdress,
		type:'GET',
		dataType:'json',
		data:{tagList: tagList, budgetName: budgetName, participantList: participantList},
		success:function(data, status, xhr)
		{
			document.location.href = '/Budgets';
		},
		error:function(xhr, status, error)
		{
			document.getElementById("submitError").style.color = "red";
			document.getElementById("submitError").innerHTML =  xhr.responseText;
			console.error(xhr, status, error);
		}
	});
}
function getCheckedTags()
{
	tags = $('.tagCheckbox:checkbox:checked');
	taglist = ""
	var rowCount=tags.length;
	for(var i=0;i<rowCount;i++)
	{
		taglist += tags[i].value;
		if (i != rowCount-1)
		{
			taglist+= ",";
		}
	}
	return taglist;
}
function getParticipants()
{
	tableID = 'budgeteerTable';
	var table=document.getElementById(tableID);
	var rowCount=table.rows.length;
	var retString = "";
	for(var i=1;i<rowCount;i++)
	{
		var row=table.rows[i];
		var budgeteerName=row.cells[1].innerHTML;
		var budgeteerPerm= row.cells[2].innerHTML;
		if(budgeteerPerm.localeCompare("Budget Partner") == 0)
		{
			budgeteerPerm="Partner";
		}
		else if(budgeteerPerm.localeCompare("Budget Viewer") == 0)
		{
			budgeteerPerm="Viewer";
		}
		else if(budgeteerPerm.localeCompare("Budget Manager") == 0)
		{
			budgeteerPerm="Manager";
		}
		else
		{
			alert(budgeteerPerm);
		}
		retString += budgeteerName +":"+budgeteerPerm;
		if (i != rowCount-1)
		{
			retString += ",";
		}
	}
	return retString;
}
function sendNewChatMessage()
{
	var button = $('#submitChatMessage');
	var message = $('#ChatMessage').val();
	//$('#ChatMessage')[0].value = "";
	var budgetId = $('#hiddenBudgetId').val();
	$.ajax({
		url:'/SendChatMessage',
		type:'POST',
		dataType:'json',
		data:{message: message, budgetId: budgetId },

		success:function(data, status, xhr)
		{
			delAllRowsFromChatTable("ChatTable");
			for(var i=0;i<data.list.length;i++)
			{

				$("#ChatTable").prepend("" +
					"<tr>" +
					"<td width='10%' height='50px'>&nbsp;<span id='chatUsernameSpan' style='font-size: 14px;'>["+data.list[i].time+"]</span></td>" +
					"<td width='7%' height='50px'>&nbsp;<span id='chatUsernameSpan' style='font-size: 14px;'>["+data.list[i].username+"]</span></td>" +
					"<td width='83%' height='50px'>&nbsp;<span id='chatMessageSpan' style='font-size: 14px;'>"+data.list[i].text+"</span></td>" +
					"</tr>");
			}
			$("#ChatTable").prepend("" +
				"<tr>" +
				"<td width='10%' height='50px'>&nbsp;<span id='chatUsernameSpan' style='font-size: 14px;'>["+data.time+"]</span></td>" +
				"<td width='7%' height='50px'>&nbsp;<span id='chatUsernameSpan' style='font-size: 14px;'>["+data.username+"]</span></td>" +
				"<td width='83%' height='50px'>&nbsp;<span id='chatMessageSpan' style='font-size: 14px;'>"+data.text+"</span></td>" +
				"</tr>");
			//setTimeout(function reload_page(){ 	location.reload(); }, 800);
		},
		error:function(xhr, status, error)
		{
			alert("error");
			console.error(xhr, status, error);
		}
	});
}
function clearChatMessage()
{
	var budgetId = $('#hiddenBudgetId').val();
	$.ajax({
		url:'/ClearChatMessages',
		type:'POST',
		dataType:'json',
		data:{budgetId: budgetId },
		success:function(data, status, xhr)
		{
			setTimeout(function reload_page(){ 	location.reload(); }, 2000);
		},
		error:function(xhr, status, error)
		{
			alert( xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
function ShowNotification(notification_id,row_number) {
	$.ajax({
		url:'/RemoveNotification',
		type:'GET',
		dataType:'json',
		data:{notification_id:notification_id},
		success:function(data, status, xhr)
		{
			var ul = document.getElementById("notificationsList");
			var li_list = ul.getElementsByTagName("li");
			for(var i=0;i<li_list.length;i++)
			{
				if (li_list[i].hasAttribute("id") == true)
				{
					if (li_list[i].getAttribute("id") == row_number)
					{
						var str = li_list[i].getElementsByTagName("a")[0].getAttribute("href");
						var js_notification_id = str.substring(str.indexOf("(")+1,str.lastIndexOf(","));
						if (js_notification_id == notification_id)
						{
							li_list[i].remove();
							var notificationNumber = document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText;
							var num = parseInt(notificationNumber) - 1;
							document.getElementById("headerNotificationNumber").innerText = "You Have " + num + " New Notifications";
							document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText = num;
						}
						else
						{
							return;
						}
					}
				}
			}
			setTimeout(function reload_page(){
				if (document.location.href.substring(document.location.href.lastIndexOf("/")+1) != data.link.substring(data.link.lastIndexOf("/")+1)) {
					document.location.href = data.link;
				}
			}, 500);
		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
function removeAllNotifications() {
	var ul = document.getElementById("notificationsList");
	var li_list = ul.getElementsByTagName("li");
	for(var i=0;i<li_list.length;i++)
	{
		li_list[i].remove();
	}
	document.getElementById("headerNotificationNumber").innerText = "You Have 0 New Notifications";
	document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText = 0;
	$.ajax({
		url:'/RemoveAllNotifications',
		type:'GET',
		dataType:'json',
		data:{},
		success:function(data, status, xhr)
		{
			location.reload();
		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}