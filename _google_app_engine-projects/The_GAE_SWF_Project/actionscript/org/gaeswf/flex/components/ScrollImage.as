/*

ScrollImage component by Aral Balkan.
Copyright (c) 2008 Aral Balkan.

Based on the ScrollImage component by Arpit Mathur.
http://www.arpitonline.com/blog/?p=87
Copyright (c) 2007 Arpit Mathur.

Changelist from Arpit's version:

* Correctly scrolls both zoomed in (<1) and zoomed out (>1) content.
* Correctly frames scrolled content so that no whitespace shows.
* Supports the loading of images via the load() method.
* Applies smoothening to the bitmap when zoomed in/out (not when at 100%). 
* Implements "natural" click and drag scrolling (reversed). 
* Image does not get stuck to the sides when user keeps scrolling after 
  an edge has been reached. 
* Component displays the hand cursor when over the image.

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/

package org.gaeswf.flex.components
{
	import com.joelconnett.geom.FlexMatrixTransformer;
	
	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Matrix;
	import flash.geom.Rectangle;
	import flash.utils.ByteArray;
	
	import mx.controls.Image;
	import mx.core.ScrollControlBase;
	import mx.core.ScrollPolicy;
	import mx.events.FlexEvent;
	import mx.events.ScrollEvent;
	import mx.events.ScrollEventDirection;
	import mx.graphics.ImageSnapshot;
	
	[Event(name="change", "type=flash.events.Event")]
	public class ScrollImage extends ScrollControlBase
	{
		
		protected var img:Image = null;
		protected var _source:String;
		protected var _scale:Number = 1;
		
		protected var currentAngle:Number = 0;
		
		/**
		 * Constructor
		 * 
		 * The ScrollControlBase's horizontalScrollPolicy 
		 * for some reason is set to OFF. Setting it to AUTO to
		 * allow scrolling as needed. If off is needed, that can 
		 * still be used and the values set will override this 
		 * default.
		 */ 
	    public function ScrollImage()
	    {
	    	this.horizontalScrollPolicy = ScrollPolicy.AUTO;
	    }
	    
	    /**
	    * Applies a rotation to the image
	    */
	    
	    public function rotateBy(angle:Number):void
	    {
	    	// Update the internal rotation counter.
	    	currentAngle += angle;
	    	if (currentAngle == 360) currentAngle = 0;
	    	
	    	applyRotation(angle);
	    }


		private function applyRotation(angle:Number):void
		{
			// Apply the rotation transform.
			var m:Matrix = transform.matrix;
			FlexMatrixTransformer.rotateAroundInternalPoint(m, width / 2, height / 2, angle);
			transform.matrix = m;
		}	    
	    
	    public function get image():Image
	    {
	    	return img;
	    }
	    
		/**
		 * Sets the source of the Image to load it in
		 */ 	
		public function set source(s:String):void
		{
			_source = s;
			invalidateProperties();
		}
		
		public function load(imageFileURL:String):void
		{
			// Reset the scale. 
			createImage();
			
			// Reset the scroll position to the top left.
			horizontalScrollPosition = verticalScrollPosition = 0;
			
			// Load the image.
			source = imageFileURL;
		}
		
		/**
		 * Returns the minimum zoom factors at which the smaller
		 * dimension of the image will fit the viewable area completely. 
		 * Author: Aral Balkan.
		 */
		public function get minScale():Number
		{
			// If img.width<img.height or ==
			if (img.width<=img.height)
			{
				return unscaledWidth/img.width;
			}
			else
			{
				return unscaledHeight/img.height;
			}
		} 
		
		// Can the current image scroll?
		public function get canScroll():Boolean
		{
			return (img.width > width || img.height > height);
		}

		public function get canScale():Boolean
		{
			return minScale != 1;
		}
		
		/**
		 * Return a snapshot of the currently cropped image as a bitmap.
		 */
		public function get byteArray():ByteArray
		{
			// Rotate the shell in the opposite direction to reset it.
			applyRotation(-currentAngle);
			
			// Apply the current rotation to the image before taking a snapshot.
	    	var m:Matrix = img.transform.matrix;
			FlexMatrixTransformer.rotateAroundExternalPoint(m, width/2, height/2, currentAngle);
			img.transform.matrix = m;

			// Take the snapshot.
			var snapshot:ImageSnapshot = ImageSnapshot.captureImage(this);

			// Remove the rotation from the image.
			FlexMatrixTransformer.rotateAroundExternalPoint(m, width/2, height/2, -currentAngle);
			img.transform.matrix = m;

			// Return the rotation to us. 
			applyRotation(currentAngle); 
			
			return snapshot.data;	
		}
		
		/**
		 * If the image source has been set and its different from
		 * the image set earlier, sets the source. Since the image autoLoad
		 * is true, the image is loaded in immediately. 
		 */ 
		override protected function commitProperties():void
		{
			super.commitProperties();
			if(!_source || _source == img.source) return;
			img.source = _source;
			img.addEventListener(FlexEvent.UPDATE_COMPLETE, onUpdateComplete);
		}
		
		public function get source():String
		{
			return _source;
		}
		
		/**
		 * Adds an image component as the child, and sets the maskShape 
		 * Shape (inherited from ScrollControlBase) as the mask for the 
		 * image.Also sets up the scroll listener  as well as the mouseDown
		 * listeners that let you move the image around by clicking and 
		 * dragging the mouse over the image.
		 */ 
		override protected function createChildren():void
		{
			super.createChildren();
			createImage();
			addEventListener(ScrollEvent.SCROLL, onScroll);
		}


		private function createImage():void
		{
			// Rotate the shell in the opposite direction to reset it and
			// reset the current angle.
			applyRotation(-currentAngle);
			currentAngle = 0;
			
			if (img != null)
			{
				// Already exists, remove listeners and delete
				img.removeEventListener(MouseEvent.MOUSE_DOWN, onMouseDown);
				img.removeEventListener(MouseEvent.MOUSE_UP, onMouseUp);
				img.mask = null;
				removeChild(img);
				img = null
			}
			
			img = new Image();
			img.includeInLayout=false;
			img.x = 0;
			img.y = 0; 
			addChild(img);
			img.mask = this.maskShape;	
			img.addEventListener(MouseEvent.MOUSE_DOWN, onMouseDown);
			img.addEventListener(MouseEvent.MOUSE_UP, onMouseUp)
			
		}		
		
		private function onMouseDown(event:MouseEvent):void
		{
			oldMouseX = this.mouseX;
			oldMouseY = this.mouseY;
			this.addEventListener(MouseEvent.MOUSE_MOVE, onMouseMove);
			stage.addEventListener(MouseEvent.MOUSE_UP, onMouseUp);
		}
		
		private var oldMouseX:Number=NaN;
		private var oldMouseY:Number=NaN;
		private var deltaX:Number;
		private var deltaY:Number;
		
		
		/**
		 * On mouseMove, dispatch scrollEvents
		 */ 
		private function onMouseMove(event:MouseEvent):void
		{
			deltaX = oldMouseX-mouseX;
			deltaY = oldMouseY-mouseY;
			this.horizontalScrollPosition += deltaX;
			this.verticalScrollPosition += deltaY;
			
			if( (deltaX < 0 &&  img.x < 0 )){ 
				dispatchEvent(new ScrollEvent(ScrollEvent.SCROLL,false,false,null,this.horizontalScrollPosition,"horizontal",deltaX))
			}
			else if(deltaX > 0 && img.x+img.width>this.width){
				dispatchEvent(new ScrollEvent(ScrollEvent.SCROLL,false,false,null,this.horizontalScrollPosition,"horizontal",deltaY))
			}
			
			if(deltaY > 0 && img.y+img.height>this.height){
				dispatchEvent(new ScrollEvent(ScrollEvent.SCROLL,false,false,null,this.verticalScrollPosition,"vertical",deltaY))
			}
			else if(deltaY < 0 && img.y < 0){
				dispatchEvent(new ScrollEvent(ScrollEvent.SCROLL,false,false,null,this.verticalScrollPosition,"vertical",deltaY))
			}
			oldMouseX = mouseX;
			oldMouseY = mouseY;
		}
		
		private function onMouseUp(event:MouseEvent):void
		{
			this.removeEventListener(MouseEvent.MOUSE_MOVE, onMouseMove);
		}
		
		/**
		 * While Flex's inbuilt scroll functions work fine, the delta's despatched 
		 * during mouseMove could scroll the image past the bounds of the
		 * scrollpane. So fix those if needed
		 */ 
		
		private function onScroll(event:ScrollEvent):void
		{
			if(event.direction==ScrollEventDirection.VERTICAL)
			{
				this.img.y=-event.position;
				if(this.img.y+this.img.height<this.height)
				{
					img.y+=this.height-(img.y+img.height)
				}
				if(img.y>0)img.y=0;

				// Make sure that the vertical scroll position
				// is not increasing behind the scenes (visual symptom:
				// image appears stuck to an edge.)
				if (verticalScrollPosition != -img.y) 
				{
					verticalScrollPosition = -img.y;
				}
				
				//trace ("y: " + img.y);
				//trace ("vsp: " + verticalScrollPosition);


			}
			else
			{
				this.img.x=-event.position;
				
				if(img.x+img.width<this.width)
				{
					img.x += this.width-(img.x+img.width)
				}

				if(img.x>0)
				{
					img.x=0;
				}
				
				// Make sure that the horizontal scroll position
				// is not increasing behind the scenes (visual symptom:
				// image appears stuck to an edge.)
				if (horizontalScrollPosition != -img.x) 
				{
					horizontalScrollPosition = -img.x;
				}
			}
		}
		
		private function onUpdateComplete(event:Event):void{
			if(!img.content || img.content.width==0 || img.content.height==0)return;
			img.removeEventListener(FlexEvent.UPDATE_COMPLETE, onUpdateComplete);
			img.width=img.content.width;
			img.height=img.content.height;
			this.setScrollBarProperties(img.width,unscaledWidth,img.height,unscaledHeight);

			img.scaleX = img.scaleY = 1;
			
			useHandCursor = buttonMode = !(img.width == width && img.height == height);

			// Dispatch a change event to signal that the image has changed. 
			// (It's now safe to query the minScale, for example.) 
			dispatchEvent(new Event(Event.CHANGE));
		}
		

		override protected function mouseWheelHandler(event:MouseEvent):void
		{
			// TODO: NOT WORKING! :)
			if (event.delta>1)
			{
				scale = _scale + .1 > 1 ? _scale + .1 : 1;
			}
			else
			{
				scale = _scale - .1 < minScale ? _scale - .1 : minScale; 
			}

			/*
			super.mouseWheelHandler(event);

			if(event.delta>1){
				if(img.y+img.height >= this.height) return
			}
			else{
				if(img.y <= 0) return;
			}
			*/
		}

		
		/**
		 * Scale the image as needed while maintaining
		 * the image inside the view-port.
		 */ 
		public function set scale(value:Number):void
		{
			_scale = value;
			
			this.img.width=img.content.width*value
			this.img.height= img.content.height*value;

			this.setScrollBarProperties(img.content.width*value,unscaledWidth,img.content.height*value,unscaledHeight);	
			
			if(img.x+img.width<this.width){
				img.x+=this.width-(img.x+img.width);
			}
			if(img.y+img.height<this.height){
				img.y+=this.height-(img.y+img.height);
			}
			
			// Smoothen the bitmap if we're not at 100%
			if (value != 1)
			{
				(img.content as Bitmap).smoothing = true;
			}
		}
	}
}