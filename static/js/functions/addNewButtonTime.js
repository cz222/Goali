//dynamically adds buttons
function addNewButton(type, id, isSub, ref, rel, message, ttl, desc, pri, comp, dcomp) {
	$("body").append('<a style="display:none" href="#'+ref+'" class="pure-button" rel="'+rel+'" id="'+type+'-'+id+'-btn">'+message+'</a>');
	$("#"+type+"-"+id+"-btn").click(function() {
		$('#id_'+type+'_id').val(id);
		$('#id_'+type+'_isSub').val(isSub);
		if (type === "editmilestone") { 
			prefillEditForm(ttl, desc, pri, comp, dcomp)
		}
	});
}