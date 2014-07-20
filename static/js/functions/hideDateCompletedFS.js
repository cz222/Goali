//hide date_completed if not completed for formsets
function hideDateCompletedFS(divID,type,num){
	if ($('#id_'+type+'-'+num+'-completed', '#'+divID).is(':checked')) {
		$("#"+divID+" label[for='id_"+type+"-"+num+"-date_completed']").show();
		$('#id_'+type+'-'+num+'-date_completed', '#'+divID).show();
	}
	else {
		$("#"+divID+" label[for='id_"+type+"-"+num+"-date_completed']").hide();
		$('#id_'+type+'-'+num+'-date_completed', '#'+divID).hide();
	}
}