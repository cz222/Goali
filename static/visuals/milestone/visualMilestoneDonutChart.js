	var visualMilestone = function(divID, goal, msSet, alljournals){	
			//set goalColor
			var goalColor = "steelblue";
			var cColor = "lightgreen";
			
			var getGoalColor = function() {
				if (goal.goal_completed) {
					return cColor;
				} else {
					return goalColor;
				};
			};
			
			//find depths
			var count = 1;
			var depthArray = [1,0];
			var currentDepth = 2;
			
			var findSizeNArray = function(arr) {
				if (depthArray.length >= currentDepth) {
					var ele = currentDepth - 1; 
					depthArray[ele] += 1;
				}
				else {
					depthArray.push(1);
				};
				var subs = arr.submilestones;
				var subLength = subs.length;
				if (subLength > 0) {
					currentDepth++;
					for (var i = 0; i < subLength; i++) {
						findSizeNArray(subs[i]);
					};
					currentDepth--;
				}
				else {
				}
				count++;
			};
			
			for (var i = 0; i < msSet.length; i++) {
				findSizeNArray(msSet[i]);
			};
			
			//set opening transition speed
			var transSpeed = 1500/count;
			
			//draw pie
			var color = d3.scale.ordinal()
				.domain([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
				.range(["#1f77b4","#aec7e8","#ffbb78","#d62728","#ff9896","#9467bd","#c5b0d5","#c49c94","#e377c2","#f7b6d2","#bcbd22","#dbdb8d","#17becf","#9edae5"]);
			
			var pie = d3.layout.pie();
			var arc = d3.svg.arc().outerRadius(radius);
			
			//draw svg
			var width = 650,
				height = 500,
				radius = Math.min(width, height)/2 - 10;
			var iradius = radius*0.6;	
			
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
				
			//calculate size of donut arcs
			var sizeArray = [];
			var depths = [];
			var sum = 0;
			
			for (var i = 0; i < depthArray.length; i++) {
				sizeArray[i] = Math.pow(0.70, i); 
				sizeArray[i] = sizeArray[i]*depthArray[i];
				sum += sizeArray[i];
				depths[i] = i+1;
			};
			
			var rad = (2*Math.PI)/sum;
			for (var i = 0; i < depthArray.length; i++) {
				sizeArray[i] = sizeArray[i]*rad/depthArray[i];
			};

			var radScale = d3.scale.ordinal()
				.domain(depths)
				.range(sizeArray);
			
			//donut arc variables
			currentDepth = 0;
			currentAngle = 0;
			var idArray = [goal.goal_id];
			var isGoal = true;
			var selected = -15;
			var selectedObj;
			var delayCounter = 0;
			var completedGoal; //goal that is to be completed
			var completedColor; //original color of selected completed ms
			var selectedColor; //color of selected ms
			var cmplt = false; //whether or not completeTrans has been run
			var start = true;
			
			//Transitions
			var completeTransHelp = function(obj) {
				if (obj.milestone_completed) {
				} else {
					var subs = obj.submilestones;
					d3.select("#msArc_"+obj.milestone_id)
						.transition()
						.style("fill", cColor)
						.duration(400)
						.delay(delayCounter*300);
					delayCounter++;
					for (var i = 0; i < subs.length; i++) {
						completeTransHelp(subs[i]);
					};
				}
			};
	
			var completeTrans = function(obj) {
				if (isGoal) {
					for (var i = 0; i < msSet.length; i++) {
						completeTransHelp(msSet[i]);
					}
					d3.select("#goal_arc")
						.transition()
						.style("fill", cColor)
						.duration(400)
						.delay(delayCounter*300);
				} else {
					completeTransHelp(obj);
				};
				cmplt = true;
			};
			
			var normalTransHelp = function(obj, clr, opacBool) {
				var subs = obj.submilestones;
				if (obj.milestone_completed) {
				} else if (obj.milestone_is_sub) {
					if (opacBool && !(obj.milestone_id === selected)) {
						d3.select("#msArc_"+obj.milestone_id)
							.transition()
							.style("opacity", "0.5")
							.style("fill", clr)
							.duration(250);
					} else {
						d3.select("#msArc_"+obj.milestone_id)
							.transition()
							.style("fill", clr)
							.duration(250)
							.style("opacity", "1.0");
					}
					for (var i = 0; i < subs.length; i++) {
						normalTransHelp(subs[i], clr, opacBool);
					};
				} else {
					var newColor = color((obj.milestone_id*23)%13)
					if (opacBool && !(obj.milestone_id === selected)) {
						d3.select("#msArc_"+obj.milestone_id)
							.transition()
							.style("opacity", "0.5")
							.style("fill", newColor)
							.duration(250)
							.transition();
					} else {
						d3.select("#msArc_"+obj.milestone_id)
							.transition()
							.style("fill", newColor)
							.duration(250)
							.style("opacity", "1.0");
					}
					for (var i = 0; i < subs.length; i++) {
						normalTransHelp(subs[i], newColor, opacBool);
					};
				};
			};
			
			var normalTrans = function(obj, opacBool) {
				if (cmplt) {
					if (opacBool && !(selected === (-15))) {
						d3.select("#goal_arc")
							.transition()
							.style("opacity", "0.5")
							.style("fill", getGoalColor)
							.duration(250);
					} else {
						d3.select("#goal_arc")
							.transition()
							.style("fill", getGoalColor)
							.duration(250)
							.style("opacity", "1.0");
					};
						for (var i = 0; i < msSet.length; i++) {
							normalTransHelp(msSet[i], completedColor, opacBool);
						};
					$("#completed-form").hide()
				};
				cmplt = false;
			};
			
			var fadeMilestones = function(arr, sel) {
				if (isGoal) {
					d3.select("#goal_arc")
						.transition()
						.duration(350)
						.style("opacity", "1.0");
				} else {
					d3.select("#goal_arc")
						.transition()
						.duration(350)
						.style("opacity", "0.5");
				};
				for (var i = 0; i < arr.length; i++) {
					if (arr[i] === sel) {
						d3.select("#msArc_"+sel)
							.transition()
							.duration(350)
							.style("opacity", "1.0");
					} else {
						d3.select("#msArc_"+arr[i])
							.transition()
							.duration(350)
							.style("opacity", "0.5");
					}
				};
			};
			
			var restoreOpacity = function(arr) {
				for (var i = 0; i < arr.length; i++) {
					d3.select("#msArc_"+arr[i])
						.transition()
						.style("opacity", "1.0");
				};
				d3.select("#goal_arc")
					.transition()
					.style("opacity", "1.0");
			};
			
			backdrop.on("click", function() { restoreOpacity(idArray);});
			
			var delayArcs = 1;
			
			var drawArcs = function(arr, clr) {
				idArray.push(arr.milestone_id);
				addNewButton('milestone', arr.milestone_id, arr.milestone_is_sub, 'submilestone-form', 'submilestone-form', 'Add New Sub-Milestone'+arr.milestone_id, arr.milestone_title, arr.milestone_description, arr.milestone_private, arr.milestone_completed, arr.milestone_date_completed)
				addNewButton('editmilestone', arr.milestone_id, arr.milestone_is_sub, 'editmilestone-form', 'editmilestone-form', 'Edit Milestone'+arr.milestone_id, arr.milestone_title, arr.milestone_description, arr.milestone_private, arr.milestone_completed, arr.milestone_date_completed)
				addNewButton('deletemilestone', arr.milestone_id, arr.milestone_is_sub, 'deletemilestone-form', 'deletemilestone-form', 'Delete Milestone'+arr.milestone_id, arr.milestone_title, arr.milestone_description, arr.milestone_private, arr.milestone_completed, arr.milestone_date_completed)
				
				var radAdd = sizeArray[currentDepth];
				var arcData = {endAngle: (radAdd + currentAngle)};
				var arc = d3.svg.arc().innerRadius(iradius).outerRadius(radius).startAngle(currentAngle);
				
				var tweenDonut = function(transition, newAngle) {
					transition.attrTween("d", function(d) {
						var interpolate = d3.interpolate(d.endAngle, newAngle);
						return function(t) {
							d.endAngle = interpolate(t);
							return arc(d);
						};
					});
				};
				var msClr = clr;
				if (arr.milestone_completed) {
					msClr = cColor;
				} else if (currentDepth == 1) {
					msClr = color((arr.milestone_id*23)%13);
				} else {
					msClr = clr;
				};
				var msArc = visualContainer.append("path")
				  .datum({endAngle: currentAngle})
					.attr("id", "msArc_"+arr.milestone_id)
					.attr("d", arc)
					.attr("fill", msClr)
					.attr("stroke", "white")
					.attr("stroke-width", "5px")
					.attr("transform", "translate(" + width/2 + "," + height/2+")")
					.on("click", function() {
						start = false;
						selected = arr.milestone_id;
						selectedColor = msClr;
						selectedObj = arr;
						isGoal=false;
						fadeMilestones(idArray, selected);
						delayCounter = 0; 
						normalTrans(completedGoal, true);
						fillDisplayDetails(arr.milestone_title, arr.milestone_description, arr.milestone_private, arr.milestone_completed, 
							arr.milestone_date_created, arr.milestone_date_completed, arr.milestone_last_updated);
						fillDisplayNote(arr.milestone_title, arr.milestone_notes, arr.milestone_id, false);
						fillDisplayJournal(arr.milestone_title, arr.milestone_journal, arr.milestone_id, false);
						$("#completed-form").animate({top:"390"});
						$("#42").hide();
					});
				msArc.transition()
					.duration(transSpeed)
					.delay(transSpeed*delayArcs)
					.call(tweenDonut, (radAdd+currentAngle));
				delayArcs++;
				currentAngle = radAdd+currentAngle
				var subs = arr.submilestones;
				var subLength = subs.length;
				if (subLength > 0) {
					currentDepth++;
					for (var i = 0; i < subLength; i++) {
						drawArcs(subs[i],msClr);
					};
					currentDepth--;
				};
			};
			
			//Draw goal arc
			var gArcData = {endAngle: (sizeArray[0]/2)};
			var gArc = d3.svg.arc().innerRadius(radius*0.5).outerRadius(radius).startAngle(0-(sizeArray[0]/2));

			var gTweenDonut = function(transition, newAngle) {
				transition.attrTween("d", function(d) {
					var interpolate = d3.interpolate(d.endAngle, newAngle);
					return function(t) {
						d.endAngle = interpolate(t);
						return gArc(d);
					};
				});
			};
			
			var goalArc = visualContainer.append("path")
			  .datum({endAngle: (0-(sizeArray[0]/2))})
				.attr("id", "goal_arc")
				.attr("d", gArc)
				.attr("fill", getGoalColor())
				.attr("stroke", "white")
				.attr("stroke-width", "5px")
				.attr("transform", "translate(" + width/2 + "," + height/2+")")
				.on("click", function() {
					start = false;
					isGoal=true;
					selected = -15;
					fadeMilestones(idArray, "goal_arc");
					delayCounter = 0; 
					normalTrans(completedGoal, true);
					fillDisplayDetails(gl.goal_title, gl.goal_description, gl.goal_private, gl.goal_completed, gl.goal_date_created, 
						gl.goal_date_completed, gl.goal_last_updated);
					fillDisplayNote(gl.goal_title, gl.goal_notes, -15, true);
					fillDisplayJournal(gl.goal_title, alljournals, -15, true);
					$("#completed-form").animate({top:"390"});
					$("#42").hide();
				});
			
			goalArc.transition()
				.duration(transSpeed)
				.call(gTweenDonut, (sizeArray[0]/2));
			currentAngle += 0+(sizeArray[0]/2);
			currentDepth++;
			
			//Draw donut arcs
			for (var i = 0; i < msSet.length; i++) {
				drawArcs(msSet[i]);
			};

			$("#id_completedmilestone_id").val(goal.goal_id);
			$("#id_completedmilestone_isGoal").val(true);
			
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
			
			//Other buttons
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
			
			var addContainer = svg.append("g");
			var addButton = addContainer.append("rect")
				.attr("id", "cmplt-tab")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*7)+")");		
			var addIcon = addContainer.append("rect")
				.attr("id", "add-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#addSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*6+iconPadding+8)+")");
			var displayRectAdd = addContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
				if (isGoal) {
					$("#milestone-form-btn").click()
				} else {
					$("#milestone-"+selected+"-btn").click()
				};
			});
			
			var editContainer = svg.append("g");
			var editButton = editContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*8)+")");			
			var editIcon = editContainer.append("rect")
				.attr("id", "edit-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#editSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*7+iconPadding+8)+")");
			var displayRectEdit = editContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*7+displayBarHeight-1)+")");
			editContainer.on("mouseover", function() {
				displayRectEdit
					.attr("display", "block");
			});
			editContainer.on("mouseout", function() {
				displayRectEdit
					.attr("display", "none");
			});
			editContainer.on("click", function() {
				if (isGoal) {
					$("#editmilestonegoal-form-btn").click()
				} else {
					$("#editmilestone-"+selected+"-btn").click()
				}
			});
			
			var deleteContainer = svg.append("g");
			var deleteButton = deleteContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*9)+")");
			var deleteIcon = deleteContainer.append("rect")
				.attr("id", "delete-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#deleteSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*8+iconPadding+8)+")");
			var displayRectDelete = deleteContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
				if (isGoal) {
					$("#deletemilestonegoal-form-btn").click()
				} else {
					$("#deletemilestone-"+selected+"-btn").click()
				};
			});
			
			var downloadContainer = svg.append("g");
			var downloadButton = downloadContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*10)+")")
			var downloadIcon = downloadContainer.append("rect")
				.attr("id", "download-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#downloadSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*9+iconPadding+8)+")");
			var displayRectDownload = downloadContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
			var completeButton = completeContainer.append("rect")
				.attr("id", "cmplt-tab")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*11)+")")
				.attr("fill", "none")
			var completeIcon = completeContainer.append("rect")
				.attr("id", "complete-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#completeSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*10+iconPadding+8)+")");
			var displayRectComplete = completeContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
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
				completeTrans(selectedObj);
				completedGoal = selectedObj;
				completedColor = selectedColor;
				if (isGoal) {
					$("#id_completedmilestone_id").val(goal.goal_id);
					$("#id_completedmilestone_isGoal").val(true);
				} else {
					$("#id_completedmilestone_id").val(selected);
					$("#id_completedmilestone_isGoal").val(isGoal);
				};
				$("#completed-form-btn").click();
			});
			
			//draw display
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