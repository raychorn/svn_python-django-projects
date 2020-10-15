package org.gaeswf.examples.initial
{
	import flash.events.Event;
	
	import lt.uza.utils.Global;
	
	import mx.collections.ArrayCollection;
	import mx.containers.VBox;
	import mx.core.Application;
	import mx.events.FlexEvent;
	
	import org.gaeswf.flex.BaseCanvas;

	public class Home extends BaseCanvas
	{

		// TODO: Implement progress indicator for the recent users list.
		public var recentUsersList:VBox;
		
		public var loadProgress:ValidationIcons;
		
		[Bindable]
		protected var recentUsersWithPhotos:ArrayCollection;

		public function Home()
		{
			super();

			// Only access the app 
			mx.core.Application.application.addEventListener(FlexEvent.APPLICATION_COMPLETE, init);
			
			visible = false;
		}

		private function init(event:Event):void
		{
			recentUsersWithPhotos = new ArrayCollection();
			
			refreshProfiles();			
		}		
		
		private function refreshProfiles():void
		{
			loadProgress.show(ValidationIcons.PROGRESS);
			execute("user.getRecentUsersWithPhotos");
		}
		
		override public function set visible(state:Boolean):void
		{
			super.visible = state;
			
			var app:org.gaeswf.examples.initial.Application = (Global.getInstance().application) as org.gaeswf.examples.initial.Application;
			
			if (app != null)
			{
				// Setup mouse wheel support on OS X for list box.
				if (state)
				{
					// Register the list box to receive mouse wheel events.
					app.mouseWheelSupport.registerObject(recentUsersList);		
				}
				else
				{
					// Unregister the list box.
					if (recentUsersList != null)
					{
						app.mouseWheelSupport.unRegisterObject(recentUsersList);
					}
				}
			}
		}

		// Helper method: Returns an HTML link from a URL.
		// Defaults to an underlined link and to using the URL itself as the link text.
		// TODO: Pull out to a base class, this will be useful in all views.
		protected function htmlLink(url:String, linkText:String = null, underline:Boolean = true):String
		{
			var uStart:String = "<u>";
			var uEnd:String = "</u>";
			var linkStart:String = '<a href="';
			var linkStartClose:String = '">';
			var linkEnd:String = '</a>';
			
			if (url == null) return ""; 			// Pretty print nulls
			if (linkText == null) linkText = url;	// Default to link if no link text is given
			if (!underline) 
			{
				uStart = uEnd = ""; 
			}
			var link:String = uStart + linkStart +url + linkStartClose + linkText + linkEnd + uEnd;
			
			return link;
		}
		
		// 
		// Event handlers
		//

		public function user_getRecentUsersWithPhotosResponse(result:ArrayCollection):void
		{
			recentUsersWithPhotos = result;
			visible = true;
			loadProgress.show(ValidationIcons.NONE);
		}
		
	}
}