//dynamically adds buttons
function addNewButton(type, id, message, value, desc) {
	$("body").append('<a style="display:none" class="pure-button" id="'+type+'-'+id+'-btn">'+message+'</a>');
	$("#"+type+"-"+id+"-btn").on('click', function() {
		$('#id_'+type+'_id').val(id);
		if (type === 'editupdate') { 
			$("#id_value", "#editupdateform").val(value);
			$("#id_description", "#editupdateform").val(desc);
		}
	});
}