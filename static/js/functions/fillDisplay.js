//Fill display with text
var fillDisplay = function(title, description, complete, date_completed, last_updated) {
	$("#visual_title").html("");
	$("#visual_title").html("");
	$("#visual_title").append('<h1>'+title+'</h1>');
	$("#visual_title").append('<p>Description: '+description+'</p>');
	if (complete) {
		$("#visual_title").append('<p>Completed: '+date_completed+'</p>');
	} else {
		$("#visual_title").append('<p>Last Updated: '+last_updated+'</p>');
	};
};