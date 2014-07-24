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
				.attr("width", svgWidth)
				.attr("height", svgHeight)
				.attr("fill", "none")
				.attr("rx", "30");
					
			svg.attr("clip-path", "url(#clip-box)");
			
			var backdrop = svg.append("rect")
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
					.style("fill", "#ff9896")
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
				var meterArc = svg.append("path")
					.datum({endAngle: 0})
					.style("fill", "#ddd")
					.attr("d", mArc)
					.attr("transform", "translate(" + width/2 + "," + height/2+")");
		
				meterArc.transition()
					.duration(500)
					.delay(750)
					.call(tweenMeter, (percentUsed*full));
				
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
							.call(tweenMeter, (percentUsed*full));
					}
				}, 2000);
			};
			//Draw inner circle
			var arc = d3.svg.arc().innerRadius(0).outerRadius(radius*.8).startAngle(0);
			
			var mainArc = svg.append("path")
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
				.call(tweenCircle, 2*Math.PI);
				
			//draw buttons
			var convertButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 87.5)
				.attr("fill", "#9edae5")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",0)")
				.on("click", function() {
				});
			
			var detailsButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 87.5)
				.attr("fill", "#c5b0d5")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",87.5)")
				.on("click", function() {
				});
			
			var editButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 87.5)
				.attr("fill", "#dbdb8d")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",175)")
				.on("click", function() {
					$("#edittimeoneshot-form-btn").click();
				});

			var deleteButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 87.5)
				.attr("fill", "#ff9896")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",262.5)")
				.on("click", function() {
					$("#deletetimeoneshot-form-btn").click();
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
							.call(tweenCircle, full);
						
						background.transition()
							.delay(1000)
							.duration(500)
							.style("fill", cColor);
					} else {
					}
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
			
			var infoText = svg.append("text")
				.attr("dx", width+150)
				.attr("dy", height/4)
				.attr("text-anchor", "middle")
				.attr("font-size",15)
				.text(goal.title);
	};