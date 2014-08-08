//Fill display with text
var fillDisplayDetails = function(title, description, priv, complete, date_created, date_completed, last_updated) {
	$("#visual_detailsPage1").html("");
	$("#visual_detailsPage1").append('<br><h3>'+title+'</h3><br>');
	$("#visual_detailsPage1").append('<p>Description: '+description+'</p>');
	$("#visual_detailsPage1").append('<p>Private: '+priv+'</p>');
	$("#visual_detailsPage2").html("");
	$("#visual_detailsPage2").append('<br><h3>'+title+'</h3><br>');
	$("#visual_detailsPage2").append('<p>Date Created: '+date_created+'</p>');
	if (complete) {
		$("#visual_detailsPage2").append('<p>Completed: True</p>');
	} else {
		$("#visual_detailsPage2").append('<p>Completed: False</p>');
	};
	if (complete) {
		$("#visual_detailsPage2").append('<p>Date Completed: '+date_completed+'</p>');
	};
	$("#visual_detailsPage2").append('<p>Last Updated: '+last_updated+'</p>');
};