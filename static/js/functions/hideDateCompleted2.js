//hides date_completed if it is not completed
function hideDateCompleted(divID){
	if ($('#id_completed', '#'+divID).is(':checked')) {
		$("#"+divID+" label[for='id_date_completed_month']").show();
		$('#id_date_completed_month', '#'+divID).show();
		$('#id_date_completed_day', '#'+divID).show();
		$('#id_date_completed_year', '#'+divID).show();
	}
	else {
		$("#"+divID+" label[for='id_date_completed_month']").hide();
		$('#id_date_completed_month', '#'+divID).hide();
		$('#id_date_completed_day', '#'+divID).hide();
		$('#id_date_completed_year', '#'+divID).hide();
	}
}