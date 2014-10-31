var visualProgress = function(divID, goal, updates, wWidth, wHeight){
	var wMax = Math.max(wWidth, wHeight);
	var cColor = "lightgreen";
	
	if (goal.goal_determinate) {
		if (goal.goal_completed) {
			var areacolor = cColor;
			var linecolor = "darkgreen";
		} else {
			var areacolor = "#ff9896";
			var linecolor = "red";
		}
	} else {
		var areacolor = "lightblue";
		var linecolor = "steelblue";
	}
	var transpeed = 1000;
	
	//add zoom
	var zoom = d3.behavior.zoom()
		.scaleExtent([1,10])
		.on("zoom", zoomed);
	
	//draw svg
	var width = wMax*.67708333,
		height = wMax*.52083333;
	
	var svgWidth = wMax,
		svgHeight = wMax*.52083333;
	
	var svg = d3.select("#"+divID).append("svg")
		.attr("width", svgWidth)
		.attr("height", svgHeight)
		.call(zoom);
	
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
	
	var container = visualContainer.append("g");
	
	var backdrop = container.append("rect")
		.attr("width", svgWidth*3)
		.attr("height", svgWidth*3)
		.attr("fill", "white")
		.attr("transform", "translate("+((0-svgWidth)*1.5)+","+((0-svgWidth)*1.5)+")");
	
	//Prepare Axis Data
	var getMaxMin = function(values, start, max, min) {
		var newmax = max;
		var newmin = min;
		for (var i = 0; i < values.length; i++) {
			var num = (parseFloat(values[i].update_value));
			if (num > newmax) {
				newmax = num;
			}
			if (num < newmin) {
				newmin = num;
			}
		}
		var maxmin = {max: newmax, min: newmin};
		if (goal.goal_determinate) {
			if (parseFloat(goal.goal_endValue) > maxmin.max) {
				maxmin = {max: parseFloat(goal.goal_endValue), min: maxmin.min};
			}
			if (parseFloat(goal.goal_endValue) < maxmin.min) {
				maxmin = {max: maxmin.max, min: parseFloat(goal.goal_endValue)}
			}
		}
		return maxmin;
	};
	var temp1 = parseFloat(goal.goal_startValue);
	var maxmin = getMaxMin(updates, temp1, temp1, temp1);
	var createDate = function(val) {
		return new Date(val.replace(/-/g, '/'));
	};
	var startDate = createDate(goal.goal_date_created);
	if (goal.goal_complete_by == null) {
		if (goal.goal_determinate) {
			if (goal.goal_completed) {
				var finishDate = createDate(goal.goal_date_completed);
			} else {
				var finishDate = new Date();
			}
		} else {
			var finishDate = new Date()
		}
	} else {
		var finishDate = createDate(goal.goal_complete_by);
	};
	var margin = {top: (0.052083*width), right: (0.041667*width), bottom: (0.1*height), left: (0.12*height)};
	
	//calculate x and y scales
	var totalRange = Math.abs(maxmin.max - maxmin.min);
	var rangePad = totalRange*.10;
	
	var xScale = d3.time.scale()
		.domain([startDate, finishDate])
		.range([margin.left, width-margin.right]);
	
	var yScale = d3.scale.linear()
		.domain([(maxmin.min-rangePad), (maxmin.max+rangePad)])
		.range([height-margin.bottom, margin.top]);
	
	//Draw Chart
	var radius = .00520833*width;
	var pointArray = [];
	var dataArrayLine = updates.slice();
	var goalUpdate = {update_value: goal.goal_startValue, 
		update_date_created: goal.goal_date_created};
	dataArrayLine.unshift(goalUpdate);

	var dataArrayArea = dataArrayLine.slice();
	var lastValue = dataArrayLine[dataArrayLine.length-1];
	var areaEnd = {update_date_created: lastValue.update_date_created,
		update_value: (maxmin.min-rangePad)};
	var area0 = {update_date_created: goal.goal_date_created,
		update_value: (maxmin.min-rangePad)};
	dataArrayArea.push(areaEnd);
	dataArrayArea.push(area0);
	
	var drawLine = d3.svg.line()
		.x(function(d) {return xScale(createDate(d.update_date_created))})
		.y(function(d) {return yScale(String(d.update_value))})
		.interpolate("linear");
	
	var drawArea = d3.svg.line()
		.x(function(d) {return xScale(createDate(d.update_date_created))})
		.y(function(d) {return yScale(String(d.update_value))})
		.interpolate("linear");
	
	//draw area
	var area = container.append("path")
		.attr("id", "updatearea")
		.attr("d", drawArea(dataArrayArea))
		.attr("stroke", "none")
		.style("fill", areacolor)
		.attr("transform", "translate("+(svgWidth*.75)+",0)");
	
	area.transition()
		.ease("elastic")
		.duration(transpeed)
		.attr("transform", "translate(0,0)");
	
	//draw area lines
	var tAxis = d3.svg.axis()
		.scale(xScale)
		.orient("bottom")
		.ticks(7)
		.tickSize(-height);
		
	var taxis = container.append("g")
		.attr("class", "t-axis")
		.attr("transform", "translate("+(0-svgWidth)+","+(height-margin.bottom)+")")
		.call(tAxis);
		
	taxis.transition()
		.duration(transpeed)
		.ease("elastic")
		.attr("transform", "translate(0,"+(height-margin.bottom)+")")
	
	//draw goal line and calculate complete
	var completed = false
	if (goal.goal_determinate) {
		var finishline = container.append("svg:line")
			.attr("x1", xScale(startDate))
			.attr("x2", xScale(finishDate))
			.attr("y1", yScale(parseFloat(goal.goal_endValue)))
			.attr("y2", yScale(parseFloat(goal.goal_endValue)))
			.attr("d", "line")
			.attr("stroke", "darkgreen")
			.attr("stroke-width", "1.5px")
			.style("opacity", 0.5);
	};
	
	//draw update line
	var line = container.append("path")
		.attr("id", "updateline")
		.attr("d", drawLine(dataArrayLine))
		.attr("stroke", linecolor)
		.attr("stroke-width", "2px")
		.style("fill", "none")
		.attr("transform", "translate("+(0-svgWidth*0.75)+",0)");
	
	line.transition()
		.ease("elastic")
		.duration(transpeed)
		.attr("transform", "translate(0,0)");
	
	var selected = -15;
	var goalSelected = true;
	var prevSelected = -15;
	
	//draw circles
	var circles = container.selectAll(".circles")
		.data(updates)
	  .enter().append("circle")
		.attr("id", function(d) { 
			addNewButton('editupdate', d.update_id, 'editupdate-form', 'editupdate-form', 'Edit Update'+d.update_id, d.update_value_nozero, d.update_description);
			return ("update_"+d.update_id);
		})
		.style("fill", "white")
		.attr("cx", function(d) { return xScale(createDate(d.update_date_created));})
		.attr("cy", function(d) { return yScale(String(d.update_value));})
		.attr("r", radius)
		.attr("stroke", linecolor)
		.attr("transform", "translate("+(svgWidth*0.75)+","+(0-svgWidth*.55)+")")
		.on("mouseover", function(d) {  
			d3.select("#update_"+d.update_id)
				.style("fill", linecolor);
			mouseText
				.attr("x", (xScale(createDate(d.update_date_created))+6))
				.attr("y", yScale(String(d.update_value))+5)
				.style("display", "block")
				.text(d.update_nozero);
		})
		.on("mouseout", function(d) {  
			d3.select("#update_"+d.update_id)
				.style("fill", "white");
			mouseText
				.style("display", "none");
		})
		.on("click", function(d) {
			if (selected === -15) {
				startPoint.transition()
					.attr("r", radius);
			} else {
				if (!(selected === d.update_id)) {
					d3.select("#update_"+selected)
						.transition()
						.attr("r", radius);
				}
			}
			d3.select("#update_"+d.update_id)
				.transition()
				.attr("r", radius+2);
			$("#visual_journal").hide();
			$("#visual_notes").hide();
			fillDisplayUpdate(d.update_value_nozero, d.update_description, d.update_date_created, goal.goal_currentNoZero);
			selected = d.update_id;
		});
	
	circles.transition()
		.duration(transpeed)
		.ease("elastic")
		.attr("transform", "translate(0,0)");
	
	//draw y axis
	var yAxis = d3.svg.axis()
		.scale(yScale)
		.orient("left")
		.ticks(5);
	
	var yaxis = container.append("g")
		.attr("class", "y-axis")
		.attr("transform", "translate("+(margin.left)+","+(0-svgWidth)+")")
		.call(yAxis);
	
	yaxis.transition()
		.duration(transpeed)
		.ease("elastic")
		.attr("transform", "translate("+(margin.left)+",0)")
	
	//draw x-axis
	var xAxis = d3.svg.axis()
		.scale(xScale)
		.orient("bottom")
		.ticks(7);
	
	var xaxis = container.append("g")
		.attr("class", "x-axis")
		.attr("transform", "translate("+(0-svgWidth)+","+(height-margin.bottom)+")")
		.call(xAxis);
		
	xaxis.transition()
		.duration(transpeed)
		.ease("elastic")
		.attr("transform", "translate(0,"+(height-margin.bottom)+")")
	
	var mouseText = container.append("text")
		.attr("class", "mouse-text")
		.style("display", "none")
		.style("opacity", 0.7);
	
	//draw Start
	var startPoint = container.append("circle")
		.attr("id", "startpoint")
		.attr("cx", xScale(startDate))
		.attr("cy", yScale(parseFloat(goal.goal_startValue)))
		.attr("r", radius+2)
		.style("fill", "white")
		.attr("stroke", linecolor)
		.on("mouseover", function() {
			startPoint
				.style("fill", linecolor);
			mouseText
				.attr("x", xScale(startDate)+6)
				.attr("y", yScale(parseFloat(goal.goal_startValue))+5)
				.style("display", "block")
				.text(goal.goal_nozero);
		})
		.on("mouseout", function() {  
			startPoint
				.style("fill", "white");
			mouseText
				.style("display", "none");
		})
		.on("click", function() {
			if (selected === -15) {
			} else {
				d3.select("#update_"+selected)
					.transition()
					.attr("r", radius);
			}
			startPoint
				.transition()
				.attr("r", radius+2);
			fillDisplayGoal(goal.goal_title, goal.goal_description, goal.goal_nozero, goal.goal_currentNoZero, goal.goal_date_created, 
				goal.goal_determinate, goal.goal_complete_by, goal.goal_completed, goal.goal_date_completed, goal.goal_last_updated,
				goal.goal_endNoZero, goal.goal_private, goal.goal_date_created);
			selected = -15;
		});
	
	//zoom function
	function zoomed() {
		container.attr("transform", "translate("+d3.event.translate+")scale(" + d3.event.scale + ")");
	}
	
	//labels
	var xlabel = container.append("text")
		.attr("class", "x-label")
		.attr("text-anchor", "end")
		.attr("x", (width-margin.right))
		.attr("y", (height-margin.bottom-6))
		.text("Date and Time");
		
	var ylabel = container.append("text")
		.attr("class", "y-label")
		.attr("text-anchor", "front")
		.attr("x", (margin.left))
		.attr("y", (margin.top-6))
		.text(goal.goal_valueType);
	
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
	
	//Goal Buttons
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
	
	var addContainer = svg.append("g");
	var addIcon = addContainer.append("rect")
		.attr("id", "add-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#addSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*6+iconPadding+icnPad)+")");
	var displayRectAdd = addContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*6+displayBarHeight)+")");
	addContainer.on("mouseover", function() {
		displayRectAdd
			.attr("display", "block");
	});
	addContainer.on("mouseout", function() {
		displayRectAdd
			.attr("display", "none");
	});
	addContainer.on("click", function() {
		$("#valueupdate-form-btn").click();
	});
	
	var editContainer = svg.append("g");
	var editIcon = editContainer.append("rect")
		.attr("id", "edit-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#editSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*7+iconPadding+icnPad)+")");
	var displayRectEdit = editContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*7+displayBarHeight)+")");
	editContainer.on("mouseover", function() {
		displayRectEdit
			.attr("display", "block");
	});
	editContainer.on("mouseout", function() {
		displayRectEdit
			.attr("display", "none");
	});
	editContainer.on("click", function() {
		if (selected === -15) {
			$("#editvalue-form-btn").click();
		} else {
			$("#editupdate-"+selected+"-btn").click();
		}
	});
	
	var deleteContainer = svg.append("g");
	var deleteIcon = deleteContainer.append("rect")
		.attr("id", "delete-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#deleteSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*8+iconPadding+icnPad)+")");
	var displayRectDelete = deleteContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*8+displayBarHeight)+")");
	deleteContainer.on("mouseover", function() {
		displayRectDelete
			.attr("display", "block");
	});
	deleteContainer.on("mouseout", function() {
		displayRectDelete
			.attr("display", "none");
	});
	deleteContainer.on("click", function() {
		$("#deletevalue-form-btn").click();
	});
	
	var downloadContainer = svg.append("g");
	var downloadIcon = downloadContainer.append("rect")
		.attr("id", "download-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#downloadSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*9+iconPadding+icnPad)+")");
	var displayRectDownload = downloadContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*9+displayBarHeight)+")");
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
	
	var completeContainer = svg.append("g");
	var completeIcon = completeContainer.append("rect")
		.attr("id", "complete-button")
		.attr("width", "50px")
		.attr("height", "50px")
		.attr("fill", "transparent")
		.style("fill", "url(#completeSVG)")
		.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+bttPad)+","+(buttonHeight*10+iconPadding+icnPad)+")");
	var displayRectComplete = completeContainer.append("rect")
		.attr("height", (buttonHeight-iconPadding/2-hPad))
		.attr("width", "5")
		.attr("display", "none")
		.attr("fill", "white")
		.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*10+displayBarHeight)+")");
	completeContainer.on("mouseover", function() {
		displayRectComplete
			.attr("display", "block");
	});
	completeContainer.on("mouseout", function() {
		displayRectComplete
			.attr("display", "none");
	});
	completeContainer.on("click", function() {
		$("#valueupdate-form-btn").click();
	});
	
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
	/*
	$(window).resize(function() {
		var currentHeight = $(window).height()*.8;
		var currentWidth = $(window).width()*.8;
		var windowMax = Math.max(currentHeight, currentWidth);
		wWidth = windowMax;
		wHeight = windowMax*.5208;
		resizeGoalDivs(wWidth, wHeight);
		width = wWidth*.67708333;
		height = wWidth*.52083333;
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
		
		//resize chart
		margin = {top: (0.052083*width), right: (0.041667*width), bottom: (0.1*height), left: (0.12*height)};
		xScale = d3.time.scale()
			.domain([startDate, finishDate])
			.range([margin.left, width-margin.right]);
		yScale = d3.scale.linear()
			.domain([(maxmin.min-rangePad), (maxmin.max+rangePad)])
			.range([height-margin.bottom, margin.top]);
		radius = .00520833*width;
		
		pointArray = [];
		dataArrayLine = updates.slice();
		goalUpdate = {update_value: goal.goal_stateValue,
			update_date_created: goal.goal_date_created};
		dataArrayLine.unshift(goalUpdate);
		
		dataArrayArea = dataArrayLine.slice();
		lastValue = dataArrayLine[dataArrayLine.length-1];
		areaEnd = {update_date_created: lastValue.update_date_created,
		update_value: (maxmin.min-rangePad)};
		area0 = {update_date_created: goal.goal_date_created,
		update_value: (maxmin.min-rangePad)};
		dataArrayArea.push(areaEnd);
		dataArrayArea.push(area0);
		drawLine = d3.svg.line()
			.x(function(d) {return xScale(createDate(d.update_date_created))})
			.y(function(d) {return yScale(String(d.update_value))});
		drawArea = d3.svg.line()
			.x(function(d) {return xScale(createDate(d.update_date_created))})
			.y(function(d) {return yScale(String(d.update_value))});
		
		$("#updatearea").("d", drawArea(dataArrayArea));
		tAxis = d3.svg.axis()
			.scale(xScale)
			.orient("bottom")
			.ticks(7)
			.tickSize(-height);
		taxis.attr("transform", "translate(0,"+(height-margin.bottom)+")")
			.call(tAxis);
	
		//draw goal line and calculate complete
		var completed = false
		if (goal.goal_determinate) {
			finishline.attr("x1", xScale(startDate))
				.attr("x2", xScale(finishDate))
				.attr("y1", yScale(parseFloat(goal.goal_endValue)))
				.attr("y2", yScale(parseFloat(goal.goal_endValue)))
				.attr("d", "line");
		};
		
	//draw update line
	var line = container.append("path")
		.attr("id", "updateline")
		.attr("d", drawLine(dataArrayLine))
		.attr("stroke", linecolor)
		.attr("stroke-width", "2px")
		.style("fill", "none")
		.attr("transform", "translate(750,0)");
	
	line.transition()
		.ease("elastic")
		.duration(transpeed)
		.attr("transform", "translate(0,0)");
	
	var selected = -15;
	var goalSelected = true;
	var prevSelected = -15;
	
	//draw circles
	var circles = container.selectAll(".circles")
		.data(updates)
	  .enter().append("circle")
		.attr("id", function(d) { 
			addNewButton('editupdate', d.update_id, 'editupdate-form', 'editupdate-form', 'Edit Update'+d.update_id, d.update_value_nozero, d.update_description);
			return ("update_"+d.update_id);
		})
		.style("fill", "white")
		.attr("cx", function(d) { return xScale(createDate(d.update_date_created));})
		.attr("cy", function(d) { return yScale(String(d.update_value));})
		.attr("r", radius)
		.attr("stroke", linecolor)
		.attr("transform", "translate(750,-550)")
		.on("mouseover", function(d) {  
			d3.select("#update_"+d.update_id)
				.style("fill", linecolor);
			mouseText
				.attr("x", (xScale(createDate(d.update_date_created))+6))
				.attr("y", yScale(String(d.update_value))+5)
				.style("display", "block")
				.text(d.update_nozero);
		})
		.on("mouseout", function(d) {  
			d3.select("#update_"+d.update_id)
				.style("fill", "white");
			mouseText
				.style("display", "none");
		})
		.on("click", function(d) {
			if (selected === -15) {
				startPoint.transition()
					.attr("r", radius);
			} else {
				if (!(selected === d.update_id)) {
					d3.select("#update_"+selected)
						.transition()
						.attr("r", radius);
				}
			}
			d3.select("#update_"+d.update_id)
				.transition()
				.attr("r", radius+2);
			$("#visual_journal").hide();
			$("#visual_notes").hide();
			fillDisplayUpdate(d.update_value_nozero, d.update_description, d.update_date_created, goal.goal_currentNoZero);
			selected = d.update_id;
		});
	
	circles.transition()
		.duration(transpeed)
		.ease("elastic")
		.attr("transform", "translate(0,0)");
	
	//draw y axis
	var yAxis = d3.svg.axis()
		.scale(yScale)
		.orient("left")
		.ticks(5);
	
	var yaxis = container.append("g")
		.attr("class", "y-axis")
		.attr("transform", "translate("+(margin.left)+",-1000)")
		.call(yAxis);
	
	yaxis.transition()
		.duration(transpeed)
		.ease("elastic")
		.attr("transform", "translate("+(margin.left)+",0)")
	
	//draw x-axis
	var xAxis = d3.svg.axis()
		.scale(xScale)
		.orient("bottom")
		.ticks(7);
	
	var xaxis = container.append("g")
		.attr("class", "x-axis")
		.attr("transform", "translate(-1000,"+(height-margin.bottom)+")")
		.call(xAxis);
		
	xaxis.transition()
		.duration(transpeed)
		.ease("elastic")
		.attr("transform", "translate(0,"+(height-margin.bottom)+")")
	
	var mouseText = container.append("text")
		.attr("class", "mouse-text")
		.style("display", "none")
		.style("opacity", 0.7);
	
	//draw Start
	var startPoint = container.append("circle")
		.attr("id", "startpoint")
		.attr("cx", xScale(startDate))
		.attr("cy", yScale(parseFloat(goal.goal_startValue)))
		.attr("r", radius+2)
		.style("fill", "white")
		.attr("stroke", linecolor)
		.on("mouseover", function() {
			startPoint
				.style("fill", linecolor);
			mouseText
				.attr("x", xScale(startDate)+6)
				.attr("y", yScale(parseFloat(goal.goal_startValue))+5)
				.style("display", "block")
				.text(goal.goal_nozero);
		})
		.on("mouseout", function() {  
			startPoint
				.style("fill", "white");
			mouseText
				.style("display", "none");
		})
		.on("click", function() {
			if (selected === -15) {
			} else {
				d3.select("#update_"+selected)
					.transition()
					.attr("r", radius);
			}
			startPoint
				.transition()
				.attr("r", radius+2);
			fillDisplayGoal(goal.goal_title, goal.goal_description, goal.goal_nozero, goal.goal_currentNoZero, goal.goal_date_created, 
				goal.goal_determinate, goal.goal_complete_by, goal.goal_completed, goal.goal_date_completed, goal.goal_last_updated,
				goal.goal_endNoZero, goal.goal_private, goal.goal_date_created);
			selected = -15;
		});
	});*/
};