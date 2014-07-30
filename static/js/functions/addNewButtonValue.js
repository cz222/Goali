//dynamically adds buttons
function addNewButton(type, id, ref, rel, message, value, desc) {
	$("body").append('<a style="display:none" href="#'+ref+'" class="pure-button" rel="'+rel+'" id="'+type+'-'+id+'-btn">'+message+'</a>');
	$("#"+type+"-"+id+"-btn").click(function() {
		$('#id_'+type+'_id').val(id);
		if (type === 'editupdate') { 
			prefillEditFormValue(value, desc)
		}
	});
}