	var visualTimeOneShot = function(divID, goal, cColor){
			//draw svg
			var width = 650,
				height = 500;

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
			
			var isComplete = goal.goal_completed;
			
			//Draw Arcs
			var radius = Math.min(width, height)/2 - 10;
			var mRadius = .85*radius; //meter inner radius
			var full = 2*Math.PI;
			if (isComplete) {
				var mArc = d3.svg.arc()
					.innerRadius(mRadius)
					.outerRadius(radius)
					.startAngle(0);
					
				var background = svg.append("path")
				  .datum({endAngle: 0})
					.attr("id", "backgroundArc")
					.style("fill", cColor)
					.attr("d", mArc)
					.attr("transform", "translate(" + width/2 + "," + height/2+")");
					
				background.transition()
					.duration(1000)
					.call(tweenMeter, full);
			} else {
				//Draw Background Meter Circle
				var mArc = d3.svg.arc()
					.innerRadius(mRadius)
					.outerRadius(radius)
					.startAngle(0);
					
				var background = svg.append("path")
					.datum({endAngle: full})
					.style("fill", "#ddd")
					.attr("d", mArc)
					.attr("transform", "translate(" + width/2 + "," + height/2+")");
						
				//Calculate time passed
				var startDate = goal.goal_date_created;
				startDate = new Date(startDate.replace(/-/g, '/'));
				var finishDate = goal.goal_complete_by;
				finishDate = new Date(finishDate.replace(/-/g, '/'));
				var range = Math.abs(finishDate-startDate);
				var now = new Date();
				var diff = Math.abs(now-startDate);
				var percentUsed = diff/range;
				if (percentUsed > 1) {
					percentUsed = 1;
				}
				
				//Draw meter arc
				var meterArc = visualContainer.append("path")
					.datum({endAngle: 0})
					.style("fill", "#ff9896")
					.attr("d", mArc)
					.attr("transform", "translate(" + width/2 + "," + height/2+")");
		
				meterArc.transition()
					.duration(1000)
					.call(tweenMeter,((percentUsed-1)*full));
				
				function tweenMeter(transition, newAngle) {
					transition.attrTween("d", function(d) {
						var interpolate = d3.interpolate(d.endAngle, newAngle);
						return function(t) {
							d.endAngle = interpolate(t);
							return mArc(d);
						};
					});
				};
				
				setInterval(function() {
					if (!(isComplete)) {
						var now = new Date();
						var diff = Math.abs(now-startDate);
						var percentUsed = diff/range;
						if (percentUsed > 1) {
							percentUsed = 1;
						};
						meterArc.transition()
							.duration(750)
							.call(tweenMeter, ((percentUsed-1)*full));
					}
				}, 2000);
			};
			//Draw inner circle
			var arc = d3.svg.arc().innerRadius(0).outerRadius(radius*.8).startAngle(0);
			
			var mainArc = visualContainer.append("path")
				.datum({endAngle: 0})
				.style("fill", function() { 
					if (goal.goal_completed) {
						return cColor;
					} else {
						return "#ff9896";
					};})
				.attr("d", arc)
				.attr("transform", "translate(" + width/2 + "," + height/2+")");
			
			function tweenCircle(transition, newAngle) {
				transition.attrTween("d", function(d) {
					var interpolate = d3.interpolate(d.endAngle, newAngle);
					return function(t) {
						d.endAngle = interpolate(t);
						return arc(d);
					};
				});
			};
			
			mainArc.transition()
				.duration(1000)
				.call(tweenCircle, -full);

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
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*2+iconPadding+8)+")");
			var displayRectEdit = editContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*2+displayBarHeight)+")");
			editContainer.on("mouseover", function() {
				displayRectEdit
					.attr("display", "block");
			});
			editContainer.on("mouseout", function() {
				displayRectEdit
					.attr("display", "none");
			});
			editContainer.on("click", function() {
				$("#edittimeoneshot-form-btn").click();
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
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*3+iconPadding+8)+")");
			var displayRectDelete = deleteContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*3+displayBarHeight-1)+")");
			deleteContainer.on("mouseover", function() {
				displayRectDelete
					.attr("display", "block");
			});
			deleteContainer.on("mouseout", function() {
				displayRectDelete
					.attr("display", "none");
			});
			deleteContainer.on("click", function() {
				$("#deletetimeoneshot-form-btn").click();
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
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*4+iconPadding+8)+")");
			var displayRectDownload = downloadContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*4+displayBarHeight)+")");
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
				.attr("transform", "translate("+(svgWidth-buttonWidth+iconPadding+12)+","+(buttonHeight*5+iconPadding+8)+")");
			var displayRectComplete = completeContainer.append("rect")
				.attr("height", (buttonHeight-iconPadding/2-4))
				.attr("width", "5")
				.attr("display", "none")
				.attr("fill", "white")
				.attr("transform", "translate("+displayBarWidth+","+(buttonHeight*5+displayBarHeight)+")");
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
					isComplete = true;					
					var completeArc = svg.append("path")
						.datum({endAngle: 0})
						.style("fill", cColor)
						.attr("d", arc)
						.attr("transform", "translate(" + width/2 + "," + height/2+")");
		
					completeArc.transition()
						.duration(1000)
						.call(tweenCircle, -full);
					
					meterArc.transition()
						.duration(500)
						.style("fill", cColor);
				} else {
				}
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