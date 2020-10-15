package org.gaeswf.examples.initial
{
	import lt.uza.utils.Global;
	
	import mx.containers.Canvas;
	import mx.controls.List;
	
	
	import org.gaeswf.examples.initial.Application;

	public class MouseWheel extends Canvas
	{
		[Bindable]
		protected var quoteInPieces:Array = ["I", "made", "this", "letter", "longer", "than", "usual", "because", "I", "lack", "the", "time", "to", "make", "it", "short.", "(Blaise Pascal)"];

		// In MXML
		public var listBox:List;

		public function MouseWheel()
		{
			super();
		}
		
		override public function set visible(state:Boolean):void
		{
			super.visible = state;

			var app:Application = (Global.getInstance().application) as Application;

			// Setup mouse wheel support on OS X for list box.
			if (state)
			{
				// Register the list box to receive mouse wheel events.
				app.mouseWheelSupport.registerObject(listBox);			
			}
			else
			{
				// Unregister the list box.
				if (listBox != null)
				{
					app.mouseWheelSupport.unRegisterObject(listBox);
				}
			}
		}
		
	}
}