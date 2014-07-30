//prefills milestone edit forms
function prefillEditForm(ttl, desc, pri, comby, comp, dcomp) {
	$("#id_title","#editmilestoneform").val(ttl);
	$("#id_description", "#editmilestoneform").val(desc);
	$("#id_private", "#editmilestoneform").val(pri);
	$("#id_complete_by", "#editmilestoneform").val(comby);
	$("#id_completed", "#editmilestoneform").val(comp);
	$("#id_date_completed", "#editmilestoneform").val(dcomp);
	checkCompletedCheckbox("editmilestoneform", comp);
	//hideDateCompleted("editmilestoneform");
}