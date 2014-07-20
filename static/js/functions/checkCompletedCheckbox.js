//matches the checkbox with its value
function checkCompletedCheckbox(divID, val) {
	if (val) {
		$('#'+divID+' input[name=completed]').attr('checked', true);
	} else {
		$('#'+divID+' input[name=completed]').attr('checked', false);
	}
};