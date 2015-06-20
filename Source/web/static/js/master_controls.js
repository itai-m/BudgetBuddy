$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#loginBtn').on('click', submitLogin);
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
function submitEditedEntry(){
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
function submitNewEntry(){
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
	var email = $('#email').val();
	var username = $('#username').val();
	var password = $('#password').val();
	var repassword =$('#repassword').val();
	if (username == null || username == "" || password == null || password == "")
	{
		document.getElementById("displayError").innerHTML("There appears to be a missing field");
	}
	else if (repassword != password)
	{
		document.getElementById("displayError").innerHTML = ("Password don't match");
	}
	else
	{
		$.ajax({
			url:'/RegistrationCheck',
			type:'GET',
			dataType:'json',
			data:{username:username, password:password, email:email},
			success:function(data, status, xhr)
			{
				document.location.href = '/Budgets';

			},
			error:function(xhr, status, error)
			{
				document.getElementById("displayError").innerHTML = (xhr.responseText);
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
	var email = $('#email').val();
	var password = $('#password').val();
	var oldpassword = $('#oldpassword').val();
	var repassword =$('#repassword').val();

	if (repassword!=password)
	{
		document.getElementById("displayError").innerHTML = ("passwords don't matching");
	}
	else
	{
		$.ajax({
			url:'/ProfileSettingsCheck',
			type:'GET',
			dataType:'json',
			data:{oldpassword:oldpassword, password:password, email:email},
			success:function(data, status, xhr)
			{
				document.location.href = '/Budgets';
			},
			error:function(xhr, status, error)
			{
				document.getElementById("displayError").innerHTML = (xhr.responseText);
			}
		});
	}
}
function isNumber(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}
// Create Budget page functions.
function usernameExist(){
	var usernameExist = $('#checkUsernameExist').val();
	document.getElementById("usernameExistField").innerHTML = '';
	document.getElementById("usernameExistField").style.color = '';
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
			document.getElementById("usernameExistField").innerHTML = "Username doesnt exist!";
			console.error(xhr, status, error);
		}
	});
}
function addRow(){
	usernameExist();
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
function reorderRows(){
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
function submitBudget(urladdress){
	budgetName = $('#budgetName').val();
	tagList = getTagList(); // [tag],[tag],[tag] string
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
function getTagList(){
	var ret_string = "";
	var values = $("#TagSelect>option").map(function() { return $(this).val(); }).get();
	for (var i = 0; i < values.length ; i++)
	{
		ret_string += values[i] + ","
	}
	ret_string = ret_string.substring(0, ret_string.length -1 )

	return ret_string;

}
function getParticipants(){
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
function sendNewChatMessage(){
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
			for(var i=data.list.length-1;i >= 0;i--) {
				$("#ChatTable").prepend("" +
					"<tr>" +
					"<td width='10%' height='50px'>&nbsp;<span id='chatUsernameSpan' style='font-size: 14px;'>[" + data.list[i].time + "]</span></td>" +
					"<td width='7%' height='50px'>&nbsp;<span id='chatUsernameSpan' style='font-size: 14px;'>[" + data.list[i].username + "]</span></td>" +
					"<td width='83%' height='50px'>&nbsp;<span id='chatMessageSpan' style='font-size: 14px;'>" + data.list[i].text + "</span></td>" +
					"</tr>");
			}
		},
		error:function(xhr, status, error)
		{
			location.reload();
			//console.error(xhr, status, error);
		}
	});
}
function refreshChat(){
	var budgetId = $('#hiddenBudgetId').val();
	$.ajax({
		url:'/SendChatMessage',
		type:'POST',
		dataType:'json',
		data:{budgetId: budgetId },

		success:function(data, status, xhr)
		{

			delAllRowsFromChatTable("ChatTable");
			for(var i=data.list.length-1;i >= 0;i--) {
				$("#ChatTable").prepend("" +
					"<tr>" +
					"<td width='10%' height='50px'>&nbsp;<span id='chatUsernameSpan' style='font-size: 14px;'>[" + data.list[i].time + "]</span></td>" +
					"<td width='7%' height='50px'>&nbsp;<span id='chatUsernameSpan' style='font-size: 14px;'>[" + data.list[i].username + "]</span></td>" +
					"<td width='83%' height='50px'>&nbsp;<span id='chatMessageSpan' style='font-size: 14px;'>" + data.list[i].text + "</span></td>" +
					"</tr>");
			}
		},
		error:function(xhr, status, error)
		{
			console.error(xhr, status, error);
		}
	});
}
function clearChatMessage(){
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
function toggleChat(){
	var button = document.getElementById("ToggleChat");
	var val = button.value;
	var chatStatus;
	if (val.localeCompare("disabled") == 0)
		chatStatus = true;
	else
		chatStatus = false;
	var budgetId = $('#hiddenBudgetId').val();

	$.ajax({
		url:'/ToggleChat',
		type:'POST',
		dataType:'json',
		data:{budgetId: budgetId, chatStatus: chatStatus},
		success:function(data, status, xhr)
		{
			if (chatStatus)
			{
				// chatStatus = True -> Tell server that chat is now enabled.
				button.value = "enabled";
				button.innerHTML= "Disable";
			}
			else
			{
				button.value = "disabled";
				button.innerHTML = "Enable";
			}
		},
		error:function(xhr, status, error)
		{
			alert( xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
function checkNotification(notification_id, index_in_table) {
	//removes from drop down menu
	var ul = document.getElementById("notificationsList");
	var li_list = ul.getElementsByTagName("li");
	if (index_in_table < li_list.length)
	{
		li_list[index_in_table].remove();
	}
	//update number of notification badge
	decreaseNotificationAmountFromMenuBar();
	//setAsRead
	$.ajax({
		url:'/ReadNotification',
		type:'GET',
		dataType:'json',
		data:{notification_id:notification_id},
		success:function(data, status, xhr)
		{
			document.location.href = data.link;
		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
function getNotificationForMenuBar()
{
	var current_length = document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText;
	current_length = parseInt(current_length);
	if (isNaN(current_length) == true)
	{
		current_length = 0;
	}
	$.ajax({
		url:'/GetAllNotification',
		type:'GET',
		dataType:'json',
		data:{},
		success:function(data, status, xhr) {
			if ((data.notifications.length > current_length) || (isNaN(current_length) == true))
			{
				removeAllNotificationFromMenuBar();
				for (var i = 0; i < data.notifications.length; ++i)
				{
					$("#notificationsList").prepend(
						'<li id=" + i.toString() +">' +
						'<a href="javascript: checkNotification(' + data.notifications[i].id + ',' + i.toString() + ');">'+
						'<i class="fa fa-users text-aqua"></i>'+
						'<span class="notifications">'+data.notifications[i].message +
						'</span></a><li>'
					);
				}
			}
			var notification_amount = (data.notifications.length ? data.notifications.length.toString() : "");
			document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText = notification_amount;
		},
		error:function(xhr, status, error)
		{

		}
	});

}
function removeAllNotifications() {

	removeAllNotificationFromMenuBar();
	if (location.href.includes("/ShowNotifications") == true)
	{
		removeAllNotificationFromNotificationsPage();
	}
	$.ajax({
		url:'/RemoveAllNotifications',
		type:'GET',
		dataType:'json',
		data:{},
		success:function(data, status, xhr)
		{
		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
function removeAllNotificationFromMenuBar(){
	var ul = document.getElementById("notificationsList");
	var li_list = ul.getElementsByTagName("li");
	for (var i=0;i<li_list.length;i++)
	{
		li_list[i].remove();
	}
	document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText = '';
}
function removeAllNotificationFromNotificationsPage() {
	var table = document.getElementById('notificationstablebody');
	while (table.rows.length > 0) {
		table.deleteRow(0);
	}
}
function readAllNotifications() {
	removeAllNotificationFromMenuBar();
	$.ajax({
		url:'/MarkAllAsRead',
		type:'GET',
		dataType:'json',
		data:{},
		success:function(data, status, xhr)
		{
		},
		error:function(xhr, status, error)
		{
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
function decreaseNotificationAmountFromMenuBar(){
	var numOfNotification = parseInt(document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText);
	if (numOfNotification > 1)
		document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText = numOfNotification-1;
	else
		document.getElementById("notificationNumberSpan").getElementsByTagName("Span")[0].innerText = '';
}
function changeAvatar() {
	var avatar_num = 1;
	avatar_num = $('input[name=radioName]:checked').val();
	var location = "/ChangeAvatar/" + avatar_num;
	window.location.href = location;
}
function radioButtonSelectedValueSet(selectedValue, name){
	$('input[name="' + name+ '"][value="' + selectedValue + '"]').prop('checked', true);
}

function getNewTagFromUser()
{
	$.msgbox("Insert tag name to add.", {
		type: "prompt"
	}, function(result) {
		if (result) {
            if (result.length > 20)
            {
                alert("Error: Max letters exceeded");
                return;
            }
			var check_in_list = false;
			var x = document.getElementById("TagSelect");
			for (var i = 0; i < x.options.length; ++i) {
				if (result.toString() == x.options[i].value.toString())
				{
					check_in_list = true;
					break;
				}
			}
			if (check_in_list == false)
			{
				$('#TagSelect').append("<option value="+result+">"+result+"</option>");
			}

		}
	});
}

function removeTagFromSelectBox()
{
	var x = document.getElementById("TagSelect");
	x.remove(x.selectedIndex);
}