var visualOneShot = function(divID, wWidth, wHeight, goal){
	var wMax = Math.max(wWidth, wHeight);
	var cColor = 'lightgreen';
	//draw svg
	var width = wMax*.67708333,
		height = wMax*.52083333,
		radius = Math.min(width, height)/2 - 10;

	var svgWidth = wMax,
		svgHeight = wMax*.52083333;

	var svg = d3.select("#"+divID).append("svg")
		.attr("width", svgWidth)
		.attr("height", svgHeight);
	
	var clipBox = svg.append("clipPath")
		.attr("id", "clip-box");
	
	clipBox.append("rect")
		.attr("class", "glass")
		.attr("width", width+50)
		.attr("height", height)
		.attr("fill", "none")
		.attr("rx", "10px");
	
	var visualContainer = svg.append("g");
	
	visualContainer.attr("clip-path", "url(#clip-box)");
	
	var backdrop = visualContainer.append("rect")
		.attr("width", svgWidth)
		.attr("height", svgHeight)
		.attr("fill", "white");
	
	var full = 2*Math.PI;
	
	//Draw outer circle
	var arc = d3.svg.arc().innerRadius(radius*.9).outerRadius(radius).startAngle(0);
	
	var goalArc = visualContainer.append("path")
		.datum({endAngle: 0})
		.style("fill", function() { 
			if (goal.goal_completed) {
				return cColor;
			} else {
				return "#ff9896";
			};})
		.attr("d", arc)
		.attr("transform", "translate(" + width/2 + "," + height/2+")");
	
	goalArc.transition()
		.duration(1000)
		.call(tweenCircle, full);
	
	function tweenCircle(transition, newAngle) {
		transition.attrTween("d", function(d) {
			var interpolate = d3.interpolate(d.endAngle, newAngle);
			return function(t) {
				d.endAngle = interpolate(t);
				return arc(d);
			};
		});
	};
	
	//Draw inner circle
	var arcb = d3.svg.arc().innerRadius(0).outerRadius(radius*.87).startAngle(0);
	
	var goalArcb = visualContainer.append("path")
		.datum({endAngle: 0})
		.style("fill", function() { 
			if (goal.goal_completed) {
				return cColor;
			} else {
				return "#ff9896";
			};})
		.attr("d", arcb)
		.attr("transform", "translate(" + width/2 + "," + height/2+")");
	
	function tweenCircleB(transition, newAngle) {
		transition.attrTween("d", function(d) {
			var interpolate = d3.interpolate(d.endAngle, newAngle);
			return function(t) {
				d.endAngle = interpolate(t);
				return arcb(d);
			};
		});
	};
	
	goalArcb.transition()
		.duration(1000)
		.call(tweenCircleB, full);
	
	var isComplete = goal.goal_completed;
	
	//draw buttons
	var buttonWidth = wMax*.0448;
	var buttonHeight = wMax*.04375;
	var iconPadding = wMax*.00625;
	var displayBarWidth = (svgWidth-buttonWidth+iconPadding-(wMax*.00208));
	var displayBarHeight = (iconPadding+(wMax*.003125));
	
	//additional padding for aesthetic reasons
	var bttPad = wMax*.0125;
	var icnPad = wMax*.00833;
	var hPad = wMax*.004167;
	
	//Text Buttons
	var detailsContainer = svg.append("g");
	var detailsIcon = detailsContainer.append("rect")
		.attr("id", "details-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#detailsSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(iconPadding+icnPad)+")");
	var displayRectDetails = detailsContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(displayBarHeight)+")");
	detailsContainer.on("mouseover", function() {
		displayRectDetails
			.attr("display", "block");
	});
	detailsContainer.on("mouseout", function() {
		displayRectDetails
			.attr("display", "none");
	});
	detailsContainer.on("click", function() {
		$("#visual_notes").hide();
		$("#visual_journal").hide();
		$("#visual_details").fadeIn();
	});
	
	var noteContainer = svg.append("g");
	var noteIcon = noteContainer.append("rect")
		.attr("id", "convert-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#noteSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight+iconPadding+icnPad)+")");
	var displayRectNote = noteContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight+displayBarHeight)+")");
	noteContainer.on("mouseover", function() {
		displayRectNote
			.attr("display", "block");
	});
	noteContainer.on("mouseout", function() {
		displayRectNote
			.attr("display", "none");
	});
	noteContainer.on("click", function() {
		$("#visual_journal").hide();
		$("#visual_details").hide();
		$("#visual_notes").fadeIn();
	});
	
	var journalContainer = svg.append("g");
	var journalIcon = journalContainer.append("rect")
		.attr("id", "convert-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#journalSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*2+iconPadding+icnPad)+")");
	var displayRectJournal = journalContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*2+displayBarHeight)+")");
	journalContainer.on("mouseover", function() {
		displayRectJournal
			.attr("display", "block");
	});
	journalContainer.on("mouseout", function() {
		displayRectJournal
			.attr("display", "none");
	});
	journalContainer.on("click", function() {
		$("#visual_notes").hide();
		$("#visual_details").hide();
		$("#visual_journal").fadeIn();
	});
	
	//goal buttons
	var convertContainer = svg.append("g");
	var convertIcon = convertContainer.append("rect")
		.attr("id", "convert-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#convertSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*4+iconPadding+icnPad)+")");
	var displayRectConvert = convertContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*4+displayBarHeight)+")");
	convertContainer.on("mouseover", function() {
		displayRectConvert
			.attr("display", "block");
	});
	convertContainer.on("mouseout", function() {
		displayRectConvert
			.attr("display", "none");
	});
	convertContainer.on("click", function() {
	});
	
	var visualsContainer = svg.append("g");
	var visualsIcon = visualsContainer.append("rect")
		.attr("id", "convert-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#visualsSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*5+iconPadding+icnPad)+")");
	var displayRectVisuals = visualsContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*5+displayBarHeight)+")");
	visualsContainer.on("mouseover", function() {
		displayRectVisuals
			.attr("display", "block");
	});
	visualsContainer.on("mouseout", function() {
		displayRectVisuals
			.attr("display", "none");
	});
	visualsContainer.on("click", function() {
	});
	
	var editContainer = svg.append("g");
	var editIcon = editContainer.append("rect")
		.attr("id", "edit-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#editSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*6+iconPadding+icnPad)+")");
	var displayRectEdit = editContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*6+displayBarHeight)+")");
	editContainer.on("mouseover", function() {
		displayRectEdit
			.attr("display", "block");
	});
	editContainer.on("mouseout", function() {
		displayRectEdit
			.attr("display", "none");
	});
	editContainer.on("click", function() {
		$("#editoneshot-form-btn").click();
	});
	
	var deleteContainer = svg.append("g");
	var deleteIcon = deleteContainer.append("rect")
		.attr("id", "delete-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#deleteSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*7+iconPadding+icnPad)+")");
	var displayRectDelete = deleteContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*7+displayBarHeight-1)+")");
	deleteContainer.on("mouseover", function() {
		displayRectDelete
			.attr("display", "block");
	});
	deleteContainer.on("mouseout", function() {
		displayRectDelete
			.attr("display", "none");
	});
	deleteContainer.on("click", function() {
		$("#deleteoneshot-form-btn").click();
	});
	
	var downloadContainer = svg.append("g");
	var downloadIcon = downloadContainer.append("rect")
		.attr("id", "download-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#downloadSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*8+iconPadding+icnPad)+")");
	var displayRectDownload = downloadContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*8+displayBarHeight)+")");
	downloadContainer.on("mouseover", function() {
		displayRectDownload
			.attr("display", "block");
	});
	downloadContainer.on("mouseout", function() {
		displayRectDownload
			.attr("display", "none");
	});
	downloadContainer.on("click", function() {
	});
	
	var completeArc;
	var completeArcb;
	var completeContainer = svg.append("g");
	var completeIcon = completeContainer.append("rect")
		.attr("id", "complete-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#uncompleteSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*9+iconPadding+icnPad)+")");
	var displayRectComplete = completeContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*9+displayBarHeight)+")");
	completeContainer.on("mouseover", function() {
		displayRectComplete
			.attr("display", "block");
	});
	completeContainer.on("mouseout", function() {
		displayRectComplete
			.attr("display", "none");
	});
	if (goal.goal_completed) {
		completeContainer.on("click", function() {
			$("#uncomplete-form-btn").click();
		});
	} else {
		completeContainer.on("click", function() {
			$("#completed-form-btn").click();
			if (!(isComplete)) {
				completeArc = svg.append("path")
					.datum({endAngle: 0})
					.style("fill", cColor)
					.attr("d", arc)
					.attr("transform", "translate(" + width/2 + "," + height/2+")");
				
				completeArc.transition()
					.duration(1000)
					.call(tweenCircle, full);
					
				completeArcb = svg.append("path")
					.datum({endAngle: 0})
					.style("fill", cColor)
					.attr("d", arcb)
					.attr("transform", "translate(" + width/2 + "," + height/2+")");
					
				completeArcb.transition()
					.duration(1000)
					.call(tweenCircleB, full);
				
				isComplete = true;
			} else {
			}
		});
	}
	//draw display
	//background color #cccccc e9eaed
	var displayClipBox = svg.append("clipPath")
		.attr("id", "display-clip");
	var displayWidth = wMax*.278125;
	var bckgrdPad = wMax*.03125;
	
	displayClipBox.append("rect")
		.attr("class", "glass")
		.attr("width", displayWidth)
		.attr("height", svgHeight)
		.attr("fill", "none")
		.attr("rx", "10px");
	
	var display = svg.append("g")
		.attr("id", "visual_text_display");
	var display1 = display.append("rect")
		.attr("id", "visual_text_display_main")
		.attr("width", displayWidth)
		.attr("height", svgHeight)
		.attr("fill", "#e9eaed")
		.attr("transform", "translate("+width+",0)")
		.attr("rx", "10px");
	var display2 = display.append("rect")
		.attr("id", "visual_text_display_square")
		.attr("width", bckgrdPad)
		.attr("height", svgHeight)
		.attr("fill", "#e9eaed")
		.attr("transform", "translate("+width+",0)");
	
	//resize function
	$(window).resize(function() {
		var currentHeight = $(window).height()*.8;
		var currentWidth = $(window).width()*.8;
		var windowMax = Math.max(currentHeight, currentWidth);
		wWidth = windowMax;
		wHeight = windowMax*.5208;
		resizeGoalDivs(wWidth, wHeight);
		width = wWidth*.67708333;
		height = wWidth*.52083333;
		radius = Math.min(width, height)/2 - 10;
		svgWidth = wWidth;
		svgHeight = wWidth*.52083333;
		displayWidth = wWidth*.278125;
		bckgrdPad = wWidth*.03125;
		buttonWidth = wWidth*.0448;
		buttonHeight = wWidth*.04375;
		iconPadding = wWidth*.00625;
		displayBarWidth = (svgWidth-buttonWidth+iconPadding-(wWidth*.00208));
		displayBarHeight = (iconPadding+(wWidth*.003125));
		bttPad = wWidth*.0125;
		icnPad = wWidth*.00833;
		hPad = wWidth*.004167;
		
		//resize svg, clipBox, backdrop, text area, and buttons
		svg.attr("width", svgWidth).attr("height", svgHeight);
		clipBox.selectAll("rect").attr("width", width+50).attr("height", height);
		backdrop.attr("width", svgWidth).attr("height", svgHeight);
		displayClipBox.selectAll("rect").attr("width", displayWidth).attr("height", svgHeight);
		display1.attr("width", displayWidth)
			.attr("height", svgHeight)
			.attr("transform", "translate("+width+",0)");
		display2.attr("width", bckgrdPad)
			.attr("height", svgHeight)
			.attr("transform", "translate("+width+",0)");
		d3.selectAll("v-button").attr("width", buttonWidth).attr("height", buttonHeight)
			.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(iconPadding+icnPad)+")");
		d3.selectAll("details-button")
			.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(iconPadding+icnPad)+")");
		detailsIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(iconPadding+icnPad)+")");
		displayRectDetails.attr("transform", "translate("+displayBarWidth+","+(displayBarHeight)+")");
		noteIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight+iconPadding+icnPad)+")");
		displayRectNote.attr("transform", "translate("+displayBarWidth+","+(buttonHeight+displayBarHeight)+")");
		journalIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*2+iconPadding+icnPad)+")");
		displayRectJournal.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*2+displayBarHeight)+")");
		convertIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*4+iconPadding+icnPad)+")");
		displayRectConvert.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*4+displayBarHeight)+")");
		visualsIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*5+iconPadding+icnPad)+")");
		displayRectVisuals.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*5+displayBarHeight)+")");
		editIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*6+iconPadding+icnPad)+")");
		displayRectEdit.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*6+displayBarHeight)+")");
		deleteIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*7+iconPadding+icnPad)+")");
		displayRectDelete.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*7+displayBarHeight-1)+")");
		downloadIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*8+iconPadding+icnPad)+")");
		displayRectDownload.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*8+displayBarHeight)+")");
		completeIcon.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*9+iconPadding+icnPad)+")");
		displayRectComplete.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*9+displayBarHeight)+")");
		//resize goalArc and goalArcb
		arc = d3.svg.arc().innerRadius(radius*.9).outerRadius(radius).startAngle(0);
		goalArc.attr("d", arc).attr("transform", "translate(" + width/2 + "," + height/2+")");
		arcb = d3.svg.arc().innerRadius(0).outerRadius(radius*.87).startAngle(0);
		goalArcb.attr("d", arcb).attr("transform", "translate(" + width/2 + "," + height/2+")");
		
		if ((isComplete)&&(!(goal.goal_completed))) {
			completeArc.attr("d", arc).attr("transform", "translate(" + width/2 + "," + height/2+")");
			completeArcb.attr("d", arcb).attr("transform", "translate(" + width/2 + "," + height/2+")");
		}
	});
};