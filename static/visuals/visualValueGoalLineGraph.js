	var visualValue = function(divID, goal, updates, cColor){
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
			var width = 650,
				height = 500;

			var svgWidth = 960,
				svgHeight = 500;
		
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
				.attr("width", 3000)
				.attr("height", 3000)
				.attr("fill", "white")
				.attr("transform", "translate(-1500,-1500)");
			
			//Prepare Axis Data
			var getMaxMin = function(values, start, max, min) {
				var newmax = max;
				var newmin = min;
				var current = start;
				for (var i = 0; i < values.length; i++) {
					var num = (parseFloat(values[i].update_value)) + current;
					if (num > newmax) {
						newmax = num;
					}
					if (num < newmin) {
						newmax = num;
					}
					current = num;
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
			var margin = {top: 50, right: 40, bottom: 50, left: 60};
			
			//calculate x and y scales
			var xScale = d3.time.scale()
				.domain([startDate, finishDate])
				.range([margin.left, width-margin.right]);
			
			var yScale = d3.scale.linear()
				.domain([maxmin.min*.8, maxmin.max*1.2])
				.range([height-margin.bottom, margin.top]);
			
			//Draw Chart
			var radius = 5;
			var pointArray = [];
			var dataArrayLine = updates.slice();
			var goalUpdate = {update_value: goal.goal_startValue, 
				update_date_created: goal.goal_date_created,
				update_total: goal.goal_startValue};
			dataArrayLine.unshift(goalUpdate);

			var dataArrayArea = dataArrayLine.slice();
			var lastValue = dataArrayLine[dataArrayLine.length-1];
			var areaEnd = {update_date_created: lastValue.update_date_created,
				update_total: (maxmin.min*.8)};
			var area0 = {update_date_created: goal.goal_date_created,
				update_total: (maxmin.min*.8)};
			dataArrayArea.push(areaEnd);
			dataArrayArea.push(area0);

			var drawLine = d3.svg.line()
				.x(function(d) {return xScale(createDate(d.update_date_created))})
				.y(function(d) {return yScale(String(d.update_total))})
				.interpolate("linear");
			
			var drawArea = d3.svg.line()
				.x(function(d) {return xScale(createDate(d.update_date_created))})
				.y(function(d) {return yScale(String(d.update_total))})
				.interpolate("linear");
			
			//draw area
			var area = container.append("path")
				.attr("id", "updatearea")
				.attr("d", drawArea(dataArrayArea))
				.attr("stroke", "none")
				.style("fill", areacolor)
				.attr("transform", "translate(750,0)");
			
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
				.attr("transform", "translate(-1000,"+(height-margin.bottom)+")")
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
				.attr("cy", function(d) { return yScale(String(d.update_total));})
				.attr("r", radius)
				.attr("stroke", linecolor)
				.attr("transform", "translate(750,-550)")
				.on("mouseover", function(d) {  
					d3.select("#update_"+d.update_id)
						.style("fill", linecolor);
					mouseText
						.attr("x", (xScale(createDate(d.update_date_created))+6))
						.attr("y", yScale(String(d.update_total))+5)
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
					fillDisplayUpdate(d.update_value_nozero, d.update_description, d.update_date_created);
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
					fillDisplayGoal(goal.goal_title, goal.goal_description, goal.goal_nozero, maxmin.max, goal.goal_date_created, 
						goal.goal_determinate, goal.goal_completed, goal.goal_date_completed, goal.goal_last_updated);
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
			var buttonWidth = 43;
			var buttonHeight = 42;
			var iconPadding = 6;
			var displayBarWidth = (svgWidth-buttonWidth+iconPadding-2);
			var displayBarHeight = (iconPadding+3);
			
			var convertContainer = svg.append("g");
			var convertButton = convertContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("stroke", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+",0)")
			var convertIcon = convertContainer.append("rect")
				.attr("id", "convert-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#convertSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(iconPadding+8)+")");
			var displayRectConvert = convertContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(displayBarHeight)+")");
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
			
			var detailsContainer = svg.append("g");
			var detailsButton = detailsContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight)+")")
			var detailsIcon = detailsContainer.append("rect")
				.attr("id", "details-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#detailsSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight+iconPadding+8)+")");
			var displayRectDetails = detailsContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight+displayBarHeight)+")");
			detailsContainer.on("mouseover", function() {
				displayRectDetails
					.attr("display", "block");
			});
			detailsContainer.on("mouseout", function() {
				displayRectDetails
					.attr("display", "none");
			});
			detailsContainer.on("click", function() {
			});
			
			var addContainer = svg.append("g");
			var addButton = addContainer.append("rect")
				.attr("id", "cmplt-tab")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*2)+")");
			var addIcon = addContainer.append("rect")
				.attr("id", "add-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#addSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*2+iconPadding+8)+")");
			var displayRectAdd = addContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*2+displayBarHeight)+")");
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
			var editButton = editContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*3)+")");				
			var editIcon = editContainer.append("rect")
				.attr("id", "edit-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#editSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*3+iconPadding+8)+")");
			var displayRectEdit = editContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*3+displayBarHeight)+")");
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
			var deleteButton = deleteContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*4)+")");
			var deleteIcon = deleteContainer.append("rect")
				.attr("id", "delete-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#deleteSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*4+iconPadding+8)+")");
			var displayRectDelete = deleteContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*4+displayBarHeight-1)+")");
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
			var downloadButton = downloadContainer.append("rect")
				.attr("class", "v-button")
				.attr("width", buttonWidth)
				.attr("height", buttonHeight)
				.attr("fill", "none")
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*5)+")");
			var downloadIcon = downloadContainer.append("rect")
				.attr("id", "download-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#downloadSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*5+iconPadding+8)+")");
			var displayRectDownload = downloadContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*5+displayBarHeight)+")");
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
				.attr("transform", "translate("+(svgWidth-buttonWidth)+","+(buttonHeight*6)+")")
				.attr("fill", "none")
			var completeIcon = completeContainer.append("rect")
				.attr("id", "complete-button")
				.attr("width", "50px")
				.attr("height", "50px")
				.attr("fill", "transparent")
				.style("fill", "url(#completeSVG)")
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*6+iconPadding+8)+")");
			var displayRectComplete = completeContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*6+displayBarHeight)+")");
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
			
			//draw display
			var display = svg.append("rect")
				.attr("id", "visual_text_display")
				.attr("width", 267)
				.attr("height",  500)
				.attr("fill", "white")
				.attr("transform", "translate("+width+",0)")
				.attr("rx", "10");
	};