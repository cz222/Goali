//resizes divs and stuff on goal pages
function resizeGoalDivs(wWidth, wHeight) {
	$("#visual").width(wWidth).height(wHeight);
	$("#visual_texts").width(wWidth*.246875).height(wHeight*.96);
	$("#visual_details").width(wWidth*.246875).height(wHeight*.96);
	$("#visual_detailPages").width(wWidth*.246875).height((wHeight-25)*.94);
	$("#vdtabsid").width(wWidth*.246875).height(15);
	$("#page1").css("margin-left", (wWidth*.246875/2)-11.25);
	$("#page2").css("margin-left", (wWidth*.246875/2)+11.25);
	$("#visual_notes").width(wWidth*.246875).height(wHeight*.96);
	$("#note-container").width(wWidth*.246875).height((wHeight-25)*.94);
	$("#notebottom").width(wWidth*.246875).height(15);
	$("#noteadd").css("margin-left", (wWidth*.246875/2)-11.25);
	$("#notesettings").css("margin-left", (wWidth*.246875/2)+11.25);
	$("#visual_journal").width(wWidth*.246875).height(wHeight*.96);
	$("#journal-container").width(wWidth*.246875).height((wHeight-25)*.94);
	$("#journalbottom").width(wWidth*.246875).height(15);
	$("#entrybottom").width(wWidth*.246875).height(15)
	$("#journaladd").css("margin-left", (wWidth*.246875/2)-7.5);
	$("#journalsettings").css("margin-left", (wWidth*.246875/2)+11.25);
	$("#entryarrowl").css("margin-left", (wWidth*.246875/2)-50);
	$("#entryhome").css("margin-left", (wWidth*.246875/2)-26.25);
	$("#entrytrash").css("margin-left", (wWidth*.246875/2));
	$("#entryedit").css("margin-left", (wWidth*.246875/2)+23.25);
	$("#entryarrowr").css("margin-left", (wWidth*.246875/2)+50);
};