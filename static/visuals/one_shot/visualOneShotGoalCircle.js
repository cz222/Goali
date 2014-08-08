	var visualOneShot = function(divID, goal, cColor){
			//draw svg
			var width = 650,
				height = 500,
				radius = Math.min(width, height)/2 - 10;

			var svgWidth = 960,
				svgHeight = 500;
		
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
			var buttonWidth = 43;
			var buttonHeight = 42;
			var iconPadding = 6;
			var displayBarWidth = (svgWidth-buttonWidth+iconPadding-2);
			var displayBarHeight = (iconPadding+3);
			
			//Text Buttons
			var detailsContainer = svg.append("g");
			var detailsButton = detailsContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(iconPadding+8)+")");
			var detailsIcon = detailsContainer.append("rect")
				.attr("id", "details-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#detailsSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(iconPadding+8)+")");
			var displayRectDetails = detailsContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			var noteButton = noteContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("stroke", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight)+")")
			var noteIcon = noteContainer.append("rect")
				.attr("id", "convert-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#noteSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight+iconPadding+8)+")");
			var displayRectNote = noteContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			var journalButton = journalContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("stroke", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*3)+")")
			var journalIcon = journalContainer.append("rect")
				.attr("id", "convert-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#journalSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*2+iconPadding+8)+")");
			var displayRectJournal = journalContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			var convertButton = convertContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("stroke", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*5)+")");	
			var convertIcon = convertContainer.append("rect")
				.attr("id", "convert-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#convertSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*4+iconPadding+8)+")");
			var displayRectConvert = convertContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			var visualsButton = visualsContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("stroke", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*6)+")");	
			var visualsIcon = visualsContainer.append("rect")
				.attr("id", "convert-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#visualsSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*5+iconPadding+8)+")");
			var displayRectVisuals = visualsContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			var editButton = editContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*7)+")");				
			var editIcon = editContainer.append("rect")
				.attr("id", "edit-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#editSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*6+iconPadding+8)+")");
			var displayRectEdit = editContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			var deleteButton = deleteContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*8)+")");
			var deleteIcon = deleteContainer.append("rect")
				.attr("id", "delete-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#deleteSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*7+iconPadding+8)+")");
			var displayRectDelete = deleteContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			var downloadButton = downloadContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*9)+")");
			var downloadIcon = downloadContainer.append("rect")
				.attr("id", "download-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#downloadSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*8+iconPadding+8)+")");
			var displayRectDownload = downloadContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			
			if (goal.goal_completed) {
				var completeContainer = svg.append("g");
				var completeButton = completeContainer.append("rect")
					.attr("id", "cmplt-tab")
					.attr("class", "v-button")
					.attr("width", buttonWidth)
					.attr("height", buttonHeight)
					.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*10)+")")
					.attr("fill", "none")
				var completeIcon = completeContainer.append("rect")
					.attr("id", "complete-button")
					.attr("width", "50px")
					.attr("height", "50px")
					.attr("fill", "transparent")
					.style("fill", "url(#uncompleteSVG)")
					.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*9+iconPadding+8)+")");
				var displayRectComplete = completeContainer.append("rect")
					.attr("height", (buttonHeight-iconPadding/2-4))
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
				completeContainer.on("click", function() {
					$("#uncomplete-form-btn").click();
				});
			} else {
				var completeContainer = svg.append("g");
				var completeButton = completeContainer.append("rect")
					.attr("id", "cmplt-tab")
					.attr("class", "v-button")
					.attr("width", buttonWidth)
					.attr("height", buttonHeight)
					.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*10)+")")
					.attr("fill", "none")
				var completeIcon = completeContainer.append("rect")
					.attr("id", "complete-button")
					.attr("width", "50px")
					.attr("height", "50px")
					.attr("fill", "transparent")
					.style("fill", "url(#completeSVG)")
					.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*9+iconPadding+8)+")");
				var displayRectComplete = completeContainer.append("rect")
					.attr("height", (buttonHeight-iconPadding/2-4))
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
				completeContainer.on("click", function() {
					$("#completed-form-btn").click();
					if (!(isComplete)) {
						var completeArc = svg.append("path")
							.datum({endAngle: 0})
							.style("fill", cColor)
							.attr("d", arc)
							.attr("transform", "translate(" + width/2 + "," + height/2+")");
			
						completeArc.transition()
							.duration(1000)
							.call(tweenCircle, full);
							
						var completeArcb = svg.append("path")
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
			//background color #cccccc
			var displayClipBox = svg.append("clipPath")
				.attr("id", "display-clip");
					
			displayClipBox.append("rect")
				.attr("class", "glass")
				.attr("width", 267)
				.attr("height", 500)
				.attr("fill", "none")
				.attr("rx", "10px");
			
			var display = svg.append("g")
				.attr("id", "visual_text_display");
			var display1 = display.append("rect")
				.attr("id", "visual_text_display_main")
				.attr("width", 267)
				.attr("height",  500)
				.attr("fill", "#CCCCCC")
				.attr("transform", "translate("+width+",0)")
				.attr("rx", "10px");
			var display2 = display.append("rect")
				.attr("id", "visual_text_display_square")
				.attr("width", 30)
				.attr("height", 500)
				.attr("fill", "#CCCCCC")
				.attr("transform", "translate("+width+",0)");
	};