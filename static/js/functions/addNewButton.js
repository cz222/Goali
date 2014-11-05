//dynamically adds buttons
function addNewButton(type, id, isSub, message, ttl, desc, pri, comp, dcomp) {
	$("body").append('<a style="display:none" class="pure-button" id="'+type+'-'+id+'-btn">'+message+'</a>');
	$("#"+type+"-"+id+"-btn").on('click', function() {
		$('#id_'+type+'_id').val(id);
		$('#id_'+type+'_isSub').val(isSub);
		if (type === "editmilestone") { 
			prefillEditForm(ttl, desc, pri, comp, dcomp);
		}
	});
}

//prefills milestone edit forms
function prefillEditForm(ttl, desc, pri, comp, dcomp) {
	$("#id_title","#editmilestoneform").val(ttl);
	$("#id_title","#editmilestoneform").val(ttl);
	$("#id_description", "#editmilestoneform").val(desc);
	$("#id_private", "#editmilestoneform").val(pri);
	$("#id_completed", "#editmilestoneform").val(comp);
	$("#id_date_completed", "#editmilestoneform").val(dcomp);
	checkCompletedCheckbox("editmilestoneform", comp);
	hideDateCompleted("editmilestoneform");
}