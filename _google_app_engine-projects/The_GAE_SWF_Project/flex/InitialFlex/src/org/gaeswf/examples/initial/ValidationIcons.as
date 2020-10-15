package org.gaeswf.examples.initial
{
	import mx.containers.Canvas;
	import mx.controls.Image;
	import mx.core.MovieClipAsset;
	import mx.core.SpriteAsset;

	public class ValidationIcons extends Canvas
	{
		[Embed(source="library.swf", symbol="ErrorIcon")]
		public var ErrorIcon:Class;
		
		[Embed(source="library.swf", symbol="CheckIcon")]
		public var CheckIcon:Class;
		
		[Embed(source="library.swf", symbol="Progress")]
		public var Progress:Class;

		public static const NONE:int = -1;
		public static const ERROR:int = 0;
		public static const CHECK:int = 1;
		public static const PROGRESS:int = 2; 
		

		private var errorIcon:Image;
		private var checkIcon:Image;
		private var progressIndicator:Image;
		
		private var icons:Array;
		
		public function ValidationIcons()
		{
			super();
			
			errorIcon = addSymbol(SpriteAsset, ErrorIcon);
			checkIcon = addSymbol(SpriteAsset, CheckIcon);
			progressIndicator = addSymbol(MovieClipAsset, Progress);
			
			icons = [errorIcon, checkIcon, progressIndicator];
			
			show(ValidationIcons.NONE);			
		}

		// Call with either BitmapAsset, SpriteAsset, or MovieClipAsset
		private function addSymbol(AssetType:Class, FromClass:Class):Image
		{
			// Thanks to Tink (http://www.tink.ws/blog/flash-on-the-beach-was-blazin/) :) 
			var image:Image = new Image();
			var instance:* = AssetType(new FromClass());
			image.source = instance;
			addChild(image);
			return image;
		}

		public function show(iconIndex:int):void
		{
			for (var i:uint = 0; i < icons.length; i++)
			{
				icons[i].visible = false;
			}
			
			if (iconIndex != ValidationIcons.NONE)
			{
				icons[iconIndex].visible = true;
			}
		}
	}
}