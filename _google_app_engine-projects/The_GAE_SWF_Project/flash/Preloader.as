﻿/*	Generic SWF application preloader. 	Configured via Flashvars in the HTML.*/package{	import flash.display.MovieClip;	import flash.display.LoaderInfo;	import flash.display.Loader;		import flash.net.URLRequest;		import flash.events.Event;	import flash.events.ProgressEvent;		public class Preloader extends MovieClip	{		// On stage:		// private var progress:MovieClip; 		var originalWidth:Number = 0;		var loader:Loader;				public function Preloader()		{			// Get the URL of the SWF to load from Flashvars.			var swf:String = root.loaderInfo.parameters.swf;			// trace("Preloader loading SWF: " + swf);			// Save the original width of the progress bar so 			// we can use it to show progress (then initialize it zero).			originalWidth = progressBar.progress.width;			progressBar.progress.width = 0;			progressBar.visible = false;			// Create the loader, listen for events			loader = new Loader();			loader.contentLoaderInfo.addEventListener(Event.INIT, loadInitHandler);			loader.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, loadProgressHandler);			//loader.visible = false;			if (swf != null)			{				loader.load(new URLRequest(swf));			}			else			{				trace("Preloader ERROR: Could not find SWF URL to load.");			}		}						private function loadProgressHandler(event:ProgressEvent):void		{			progressBar.visible = true;			// trace(event.bytesLoaded + " of " + event.bytesTotal);			var loadRatio:Number = event.bytesLoaded/event.bytesTotal;			progressBar.progress.width = originalWidth * loadRatio;		}						private function loadInitHandler(event:Event)		{			progressBar.visible = false;			addChild(loader.content);		}	}}