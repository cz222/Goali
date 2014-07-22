	var visualMilestone = function(divID, goal, msSet, cColor){	
			//set goalColor
			var goalColor = "steelblue"
			
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
				.attr("width", svgWidth)
				.attr("height", svgHeight)
				.attr("fill", "none")
				.attr("rx", "30");
					
			svg.attr("clip-path", "url(#clip-box)");
			
			var backdrop = svg.append("rect")
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
			var completeTransHelp = function(obj, compl) {
				if (obj.milestone_completed) {
				} else {
					var subs = obj.submilestones;
					d3.select("#msArc_"+obj.milestone_id)
						.transition()
						.attr("fill", cColor)
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
						.attr("fill", cColor)
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
							.attr("fill", clr)
							.duration(250);
					} else {
						d3.select("#msArc_"+obj.milestone_id)
							.transition()
							.attr("fill", clr)
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
							.attr("fill", newColor)
							.duration(250)
							.transition();
					} else {
						d3.select("#msArc_"+obj.milestone_id)
							.transition()
							.attr("fill", newColor)
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
							.attr("fill", getGoalColor)
							.duration(250);
					} else {
						d3.select("#goal_arc")
							.transition()
							.attr("fill", getGoalColor)
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
				var arc = d3.svg.arc().outerRadius(radius)
				var arc2 = d3.svg.arc().innerRadius(iradius).outerRadius(radius).startAngle(currentAngle);
				
				var tweenDonut = function(transition, newAngle) {
					transition.attrTween("d", function(d) {
						var interpolate = d3.interpolate(d.endAngle, newAngle);
						return function(t) {
							d.endAngle = interpolate(t);
							return arc2(d);
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
				var msArc = svg.append("path")
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
						fillDisplay(arr.milestone_title, arr.milestone_description, arr.milestone_completed, arr.milestone_date_completed, arr.milestone_last_updated);
						$("#completed-form").animate({top:"430"});
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
			var gArc = d3.svg.arc().outerRadius(radius)
			var gArc2 = d3.svg.arc().innerRadius(radius*0.5).outerRadius(radius).startAngle(0-(sizeArray[0]/2));

			var gTweenDonut = function(transition, newAngle) {
				transition.attrTween("d", function(d) {
					var interpolate = d3.interpolate(d.endAngle, newAngle);
					return function(t) {
						d.endAngle = interpolate(t);
						return gArc2(d);
					};
				});
			};
			
			var goalArc = svg.append("path")
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
					fillDisplay(goal.goal_title, goal.goal_description, goal.goal_completed, goal.goal_date_completed, goal.goal_last_updated);
					$("#completed-form").animate({top:"430"});
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
			var convertButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 70)
				.attr("fill", "#9edae5")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",0)")
				.on("click", function() {
				});
			
			var detailsButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 70)
				.attr("fill", "#c5b0d5")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",70)")
				.on("click", function() {
				});
			
			var addMSButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 70)
				.attr("fill", "#aec7e8")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",140)")
				.on("click", function() {
					if (isGoal) {
						$("#milestone-form-btn").click()
					} else {
						$("#milestone-"+selected+"-btn").click()
					};
			});
			
			var editButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 70)
				.attr("fill", "#dbdb8d")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",210)")
				.on("click", function() {
					if (isGoal) {
						$("#editmilestonegoal-form-btn").click()
					} else {
						$("#editmilestone-"+selected+"-btn").click()
					}
				});

			var deleteButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 70)
				.attr("fill", "#ff9896")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",280)")
				.on("click", function() {
					if (isGoal) {
						$("#deletemilestonegoal-form-btn").click()
					} else {
						$("#deletemilestone-"+selected+"-btn").click()
					};
				});
			
			var completeButton = svg.append("rect")
				.attr("id", "cmplt-tab")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 150)
				.attr("transform", "translate("+(width+260)+",350)")
				.attr("stroke", "black")
				.attr("fill", "lightgreen")
				.on("click", function() {
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
			var display = svg.append("rect")
				.attr("width", 260)
				.attr("height",  500)
				.attr("fill", "white")
				.attr("stroke", "black")
				.attr("transform", "translate("+width+",0)");
			
			var border = svg.append("rect")
				.attr("class", "glass")
				.attr("width", svgWidth)
				.attr("height", svgHeight)
				.attr("fill", "none")
				.attr("stroke", "grey")
				.attr("stroke-width", "5px")
				.attr("rx", "30");
	};