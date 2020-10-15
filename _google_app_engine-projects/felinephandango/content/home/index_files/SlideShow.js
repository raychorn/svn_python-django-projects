//////////////////////////////////////////////////////
//Conveyor belt slideshow script- 
//© Dynamic Drive (www.dynamicdrive.com)
//For full source code, 100's more DHTML scripts, and Terms Of Use, visit dynamicdrive.com
///////////////////////////////////////////////////////

/* calls slideShowInit without the spanID parameter. this method only exists for backwards versioning compatibility */
function fillup(slide1, slide2, spanID, mouseLayer, slideHTML)
{
	slideShowInit(slide1, slide2, mouseLayer, slideHTML);
}

/* slide and slide2 are two divs that get their html set to slideHTML.
    setInterval is used to scroll the divs from right to left, and having two divs
    with the same html allows us to handle the case when one div has finished scrolling.
*/
function slideShowInit(slide1, slide2, mouseLayer, slideHTML)
{
	var cross_slide1 = document.getElementById(slide1);
	var cross_slide2 = document.getElementById(slide2);
	cross_slide1.innerHTML = cross_slide2.innerHTML = slideHTML;
	// position slide2 to appear after slide1, with a 30px gap
	cross_slide2.style.left = cross_slide1.offsetWidth + 30 + "px";
		
	lefttime = setInterval("slideleft('" + slide1 + "', '" + slide2 + "', '" + mouseLayer + "')", 30);
}

function slideleft(slide1, slide2, mouseLayer)
{
	var cross_slide1 = document.getElementById(slide1);
	var cross_slide2 = document.getElementById(slide2);
	var actualwidth = cross_slide1.offsetWidth;
	var speed = parseInt(document.getElementById(mouseLayer).getAttribute('speed'));
	
	// if a slide has not yet scrolled all the way, then move it by speed pixels to the left.
	// if a slide has scrolled all the way, then reposition it 30 pixels to the right of the other side
	if (parseInt(cross_slide1.style.left) > (actualwidth * (-1) + 8))
		cross_slide1.style.left = parseInt(cross_slide1.style.left) - speed + "px";
	else
		cross_slide1.style.left = parseInt(cross_slide2.style.left) + actualwidth + 30 + "px";
	
	if (parseInt(cross_slide2.style.left) > (actualwidth * (-1) + 8))
		cross_slide2.style.left = parseInt(cross_slide2.style.left) - speed + "px";
	else
		cross_slide2.style.left = parseInt(cross_slide1.style.left) + actualwidth + 30 + "px";
}