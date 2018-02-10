def drawTree(canvas,data):
	backGroundColor = 
	font = 

	str = data.tree
	centerX = data.treeCenterX
	top = data.treeTop
	bottom = data.treeBottom
	
	x1 = centerX
	y1 = top + (top - bottom)
	x2 = centerX
	y2 = top + (top - bottom) * (4/5.0)
	x3 = centerX
	y3 = top + (top - bottom) * (3/5.0)
	x4 = centerX
	y4 = top + (top - bottom) * (2/5.0)
	x5 = centerX
	y5 = top + (top - bottom) * (1/5.0)

	canvas.create_text(x1,y1,data.treeLine5)
	canvas.create_text(x2,y2,data.treeLine4)
	canvas.create_text(x3,y3,data.treeLine3)
	canvas.create_text(x4,y4,data.treeLine2)
	canvas.create_text(x5,y5,data.treeLine1)

	#need to set background color and font for text
	#need to set data.treeCenterX
	#need to set data.treeBottom to position the tree
	#need to update data.textLine1 to data.textLine5 at each time step

