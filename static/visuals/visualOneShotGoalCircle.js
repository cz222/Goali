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
				.attr("width", svgWidth)
				.attr("height", svgHeight)
				.attr("fill", "none")
				.attr("rx", "30");
					
			svg.attr("clip-path", "url(#clip-box)");
			
			var backdrop = svg.append("rect")
				.attr("width", svgWidth)
				.attr("height", svgHeight)
				.attr("fill", "white");

			//Draw outer circle
			var arc = d3.svg.arc().outerRadius(radius);
			var arc2 = d3.svg.arc().innerRadius(0).outerRadius(radius).startAngle(0)
			
			var goalArc = svg.append("path")
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
				.duration(1500)
				.call(tweenCircle, 2*Math.PI);
			
			function tweenCircle(transition, newAngle) {
				transition.attrTween("d", function(d) {
					var interpolate = d3.interpolate(d.endAngle, newAngle);
					return function(t) {
						d.endAngle = interpolate(t);
						return arc2(d);
					};
				});
			};
			
			//Draw inner circle
			var arcb = d3.svg.arc().outerRadius(radius*.9);
			var arcb2 = d3.svg.arc().innerRadius(0).outerRadius(radius*.9).startAngle(0);
			
			var goalArcb = svg.append("path")
				.datum({endAngle: 0})
				.style("fill", function() { 
					if (goal.goal_completed) {
						return cColor;
					} else {
						return "#ff9896";
					};})
				.attr("d", arcb)
				.attr("stroke", "white")
				.attr("stroke-width", "6px")
				.attr("transform", "translate(" + width/2 + "," + height/2+")");
			
			function tweenCircleB(transition, newAngle) {
				transition.attrTween("d", function(d) {
					var interpolate = d3.interpolate(d.endAngle, newAngle);
					return function(t) {
						d.endAngle = interpolate(t);
						return arcb2(d);
					};
				});
			};
			
			goalArcb.transition()
				.duration(1500)
				.call(tweenCircleB, 2*Math.PI);
			
			var isComplete = goal.goal_completed;
			
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
					$("#editoneshot-form-btn").click();
				});

			var deleteButton = svg.append("rect")
				.attr("class", "v-button")
				.attr("width", 50)
				.attr("height", 87.5)
				.attr("fill", "#ff9896")
				.attr("stroke", "black")
				.attr("transform", "translate("+(width+260)+",262.5)")
				.on("click", function() {
					$("#deleteoneshot-form-btn").click();
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
						goalArc.remove();
						goalArcb.remove();
						
						var completeArc = svg.append("path")
							.datum({endAngle: 0})
							.style("fill", cColor)
							.attr("d", arc)
							.attr("transform", "translate(" + width/2 + "," + height/2+")");
		
						completeArc.transition()
							.duration(1500)
							.attr("fill", cColor)
							.call(tweenCircle, 2*Math.PI);
						
						var completeArcb = svg.append("path")
							.datum({endAngle: 0})
							.style("fill", cColor)
							.attr("d", arcb)
							.attr("stroke", "white")
							.attr("stroke-width", "6px")
							.attr("transform", "translate(" + width/2 + "," + height/2+")");
							
						completeArcb.transition()
							.duration(1500)
							.attr("fill", cColor)
							.call(tweenCircleB, 2*Math.PI);
						
						isComplete = false;
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