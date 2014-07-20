	var visualDonutChart = function(divID, goal, msSet, cColor){	
			//find depths
			var count = 0;
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
			};
			
			for (var i = 0; i < msSet.length; i++) {
				findSizeNArray(msSet[i]);
			};
			
			//draw pie
			var color = d3.scale.ordinal()
				.domain([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
				.range(["#1f77b4","#aec7e8","#ffbb78","#d62728","#ff9896","#9467bd","#c5b0d5","#c49c94","#e377c2","#f7b6d2","#bcbd22","#dbdb8d","#17becf","#9edae5"]);
			
			var pie = d3.layout.pie();
			var arc = d3.svg.arc().outerRadius(radius);
			
			//draw svg
			var width = 700,
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
			var selected = goal.goal_id;
			var selectedObj;
			var delayCounter = 0;
			var completedGoal; //goal that is to be completed
			var completedColor; //original color of selected completed ms
			var selectedColor; //color of selected ms
			var cmplt = false; //whether or not completeTrans has been run
			
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
				if (obj.milestone_completed) {
				} else if (obj.milestone_is_sub) {
					var subs = obj.submilestones;
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
					var subs = obj.submilestones;
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
					if (!(isGoal)) {
						for (var i = 0; i < msSet.length; i++) {
							normalTransHelp(msSet[i], completedColor, opacBool);
						};
					} else {
						normalTransHelp(obj, completedColor, opacBool);
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
				}
				
				d3.select("#goal_arc")
						.transition()
						.style("opacity", "1.0");
			};
			
			backdrop.on("click", function() { restoreOpacity(idArray); delayCounter = 0; normalTrans(completedGoal, false);});

			//Draw donut arcs
			var drawArcs = function(arr, clr) {
				idArray.push(arr.milestone_id);
				addNewButton('milestone', arr.milestone_id, arr.milestone_is_sub, 'submilestone-form', 'submilestone-form', 'Add New Sub-Milestone'+arr.milestone_id, arr.milestone_title, arr.milestone_description, arr.milestone_private, arr.milestone_completed, arr.milestone_date_completed)
				addNewButton('editmilestone', arr.milestone_id, arr.milestone_is_sub, 'editmilestone-form', 'editmilestone-form', 'Edit Milestone'+arr.milestone_id, arr.milestone_title, arr.milestone_description, arr.milestone_private, arr.milestone_completed, arr.milestone_date_completed)
				addNewButton('deletemilestone', arr.milestone_id, arr.milestone_is_sub, 'deletemilestone-form', 'deletemilestone-form', 'Delete Milestone'+arr.milestone_id, arr.milestone_title, arr.milestone_description, arr.milestone_private, arr.milestone_completed, arr.milestone_date_completed)
				
				if (arr.milestone_completed) {
					var radAdd = sizeArray[currentDepth];
					var arc = d3.svg.arc()
						.innerRadius(0)
						.outerRadius(radius)
						.startAngle(currentAngle)
						.endAngle(radAdd + currentAngle);
						
					svg.append("path")
						.attr("id", "msArc_"+arr.milestone_id)
						.attr("d", arc)
						.attr("fill", cColor)
						.attr("stroke", "white")
						.attr("stroke-width", "5px")
						.attr("transform", "translate(" + width/2 + "," + height/2+")")
						.on("click", function() {
							selected = arr.milestone_id;
							selectedColor = cColor;
							selectedObj = arr;
							infoText.text(arr.milestone_title);
							isGoal=false;	
							fadeMilestones(idArray, selected);
							delayCounter = 0; 
							normalTrans(completedGoal, true);
						
						});
						
					currentAngle = radAdd+currentAngle
				
					var subs = arr.submilestones;
					var subLength = subs.length;
					if (subLength > 0) {
						currentDepth++;
						for (var i = 0; i < subLength; i++) {
							drawArcs(subs[i],cColor, true);
						};
						currentDepth--;
					}
				}
				
				var radAdd = sizeArray[currentDepth];
				var arc = d3.svg.arc()
					.innerRadius(iradius)
					.outerRadius(radius)
					.startAngle(currentAngle)
					.endAngle(radAdd + currentAngle);
				
				if (currentDepth == 1) {
					var newColor = color((arr.milestone_id*23)%13)
					svg.append("path")
						.attr("d", arc)
						.attr("id", "msArc_"+arr.milestone_id)
						.attr("fill", newColor)
						.attr("stroke", "white")
						.attr("stroke-width", "5px")
						.attr("transform", "translate(" + width/2 + "," + height/2+")")
						.on("click", function() {
							selected = arr.milestone_id;
							selectedColor = newColor;
							selectedObj = arr;
							infoText.text(arr.milestone_title);
							addMSButton.text("Add Sub-Milestone");
							isGoal=false;
							fadeMilestones(idArray, selected);
							delayCounter = 0; 
							normalTrans(completedGoal, true);  

						});
						
						currentAngle = radAdd+currentAngle
				
					var subs = arr.submilestones;
					var subLength = subs.length;
					if (subLength > 0) {
						currentDepth++;
						for (var i = 0; i < subLength; i++) {
							drawArcs(subs[i],newColor);
						};
						currentDepth--;
					}
				} else {
					svg.append("path")
						.attr("d", arc)
						.attr("id", "msArc_"+arr.milestone_id)
						.attr("fill", clr)
						.attr("stroke", "white")
						.attr("stroke-width", "5px")
						.attr("transform", "translate(" + width/2 + "," + height/2+")")
						.on("click", function() {
							selected = arr.milestone_id;
							selectedColor = clr;
							selectedObj = arr;
							infoText.text(arr.milestone_title);
							isGoal=false;
							fadeMilestones(idArray, selected);
							delayCounter = 0; 
							normalTrans(completedGoal, true);  
							isGoal=false;
						});
						
					currentAngle = radAdd+currentAngle
				
					var subs = arr.submilestones;
					var subLength = subs.length;
					if (subLength > 0) {
						currentDepth++;
						for (var i = 0; i < subLength; i++) {
							drawArcs(subs[i],clr);
						};
						currentDepth--;
					}
				}
			};
			
			var gArc = d3.svg.arc()
				.innerRadius(radius*0.5)
				.outerRadius(radius)
				.startAngle(0-(sizeArray[0]/2))
				.endAngle(0+(sizeArray[0]/2));
				
			svg.append("path")
				.attr("d", gArc)
				.attr("id", "goal_arc")
				.attr("fill", cColor)
				.attr("stroke", "white")
				.attr("stroke-width", "5px")
				.attr("transform", "translate(" + width/2 + "," + height/2+")")
				.on("click", function() {
					infoText.text(goal.goal_title);
					isGoal=true;
					selected = 0;
					fadeMilestones(idArray, "goal_arc");
					delayCounter = 0; 
					normalTrans(completedGoal, true);
				})
			
			currentAngle += 0+(sizeArray[0]/2);
			currentDepth++;
			
			for (var i = 0; i < msSet.length; i++) {
				drawArcs(msSet[i]);
			};
			
			//draw display
			var display = svg.append("rect")
				.attr("width", 260)
				.attr("height",  350)
				.attr("fill", "white")
				.attr("stroke", "black")
				.attr("transform", "translate(700,0)");
			
			//draw buttons
			var editButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 130)
				.attr("height", 50)
				.attr("fill", "white")
				.attr("stroke", "black")
				.attr("transform", "translate(700,350)")
				.on("click", function() {
					if (isGoal) {
						$("#editmilestonegoal-form-btn").click()
					} else {
						$("#editmilestone-"+selected+"-btn").click()
					}
				});

			var deleteButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 130)
				.attr("height", 50)
				.attr("fill", "white")
				.attr("stroke", "black")
				.attr("transform", "translate(830,350)")
				.on("click", function() {
					if (isGoal) {
						$("#deletemilestonegoal-form-btn").click()
					} else {
						$("#deletemilestone-"+selected+"-btn").click()
					};
				});
			
			var addMSButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 260)
				.attr("height", 50)
				.attr("fill", "white")
				.attr("stroke", "black")
				.attr("transform", "translate(700,400)")
				.on("click", function() {
					if (isGoal) {
						$("#milestone-form-btn").click()
					} else {
						$("#milestone-"+selected+"-btn").click()
					};
			});
			
			var completeButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 260)
				.attr("height", 50)
				.attr("transform", "translate(700,450)")
				.attr("stroke", "black")
				.attr("fill", "lightgreen")
				.on("click", function() {
					completeTrans(selectedObj);
					completedGoal = selectedObj;
					completedColor = selectedColor;
					$("#id_completedmilestone_id").val(selected);
					$("#completed-form-btn").click();
				});
			
			var border = svg.append("rect")
				.attr("class", "glass")
				.attr("width", svgWidth)
				.attr("height", svgHeight)
				.attr("fill", "none")
				.attr("stroke", "grey")
				.attr("stroke-width", "5px")
				.attr("rx", "30");
			
			var infoText = svg.append("text")
				.attr("dx", width+150)
				.attr("dy", height/4)
				.attr("text-anchor", "middle")
				.attr("font-size",15)
				.text(goal.title);
	};