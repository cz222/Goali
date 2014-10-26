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