//Fill display with text
var fillDisplayNote = function(title, notes) {
	$("#note-container").html("");
	$("#note-container").append('<br><h3>'+title+' Notes</h3><br>');
	for (var i=0; i<notes.length; i++) {
		var id = notes[i].note_id;
		var note = notes[i].note_note;
		$("#note-container").append('<li id="unote'+id+'">'+note+'<br><a id="enote-btn'+id+'" href="#">Edit</a>\t<a id="dnote-btn'+id+'" href="#">Delete</a></li>');
		$("#note-container").append('<li id="enote'+id+'">'+note+'</li>');
		$("#enote"+id).hide();
		$("#enote-btn"+id).click(function() {
			$("#unote"+id).hide();
			$("#enote"+id).show();
		});
		$("#dnote-btn"+id).click(function() {
		});
	}
	$("#visual_notes").hide();
};