//processes milestones
function processMilestone(ms, parentDivID) {
	$('#'+parentDivID).append('<div id="goal_milestones'+ms.milestone_id+'"> </div>');
	$('#goal_milestones'+ms.milestone_id).append('<p>'+ms.milestone_title+'</p>');
	var subs = ms.submilestones ;
	var arrayLength = subs.length;
	for (var i = 0; i < arrayLength; i++) {
		processMilestone(subs[i],'goal_milestones'+ms.milestone_id);
	}
	return 0;
};	