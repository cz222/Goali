//hides date_completed if it is not completed
function hideDateCompleted(divID){
	if ($('#id_completed', '#'+divID).is(':checked')) {
		$("#"+divID+" label[for='id_date_completed']").show();
		$('#id_date_completed', '#'+divID).show();
	}
	else {
		$("#"+divID+" label[for='id_date_completed']").hide();
		$('#id_date_completed', '#'+divID).hide();
	}
}