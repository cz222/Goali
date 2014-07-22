//Fill display with text
var fillDisplay = function(title, description, complete, date_completed, last_updated) {
	$("#visual_title").html("");
	$("#visual_body").html("");
	$("#visual_title").append('<h1>'+title+'</h1>');
	$("#visual_body").append('<p>Description: '+description+'</p>');
	if (complete) {
		$("#visual_body").append('<p>Completed: '+date_completed+'</p>');
	} else {
		$("#visual_body").append('<p>Last Updated: '+last_updated+'</p>');
	};
};