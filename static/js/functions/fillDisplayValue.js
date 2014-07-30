//Fill display with text
var fillDisplayGoal = function(title, description, startValue, currentValue, created, determinate, completeBy, complete, date_completed, last_updated) {
	$("#visual_title").html("");
	$("#visual_body").html("");
	$("#visual_title").append('<h1>'+title+'</h1>');
	$("#visual_body").append('<p>Description: '+description+'</p>');
	$("#visual_body").append('<p>Starting Value: '+startValue+'</p>');
	$("#visual_body").append('<p>Current Value: '+currentValue+'</p>');
	$("#visual_body").append('<p>Started: '+created+'</p>');
	if (determinate) {
		$("#visual_body").append('<p>Complete by: '+completeBy+'</p>');
		if (complete) {
			$("#visual_body").append('<p>Completed: '+date_completed+'</p>');
		} else {
			$("#visual_body").append('<p>Last Updated: '+last_updated+'</p>');
		};
	};
};

var fillDisplayUpdate = function(val, description, date) {
	$("#visual_title").html("");
	$("#visual_body").html("");
	$("#visual_title").append('<h1>Update on: '+date+'</h1>');
	$("#visual_body").append('<p>Value: '+val+'</p>');
	$("#visual_body").append('<p>Description: '+description+'</p>');
};