//hides date_completed if it is not completed
function hideDateCompletedEdit(divID){
	$("#"+divID+" label[for='id_completed']").hide();
	$('#id_completed', '#'+divID).hide();
}