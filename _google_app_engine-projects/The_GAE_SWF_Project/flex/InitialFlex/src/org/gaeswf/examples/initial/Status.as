﻿package org.gaeswf.examples.initial{	import com.mimswright.easing.Cubic;	import com.mimswright.sync.Sequence;	import com.mimswright.sync.SynchronizedSetProperty;	import com.mimswright.sync.SynchronizerEvent;	import com.mimswright.sync.Tween;	import com.mimswright.sync.Wait;		import mx.containers.Canvas;	import mx.controls.Label;		public class Status extends Canvas	{		// Defined in MXML:		public var messageLabel:Label; 						private var fadeSequence:Sequence;		private static var inst:Status;					public function Status()		{			// Hide initially.			this.alpha = 0;						// Make this is the instance that the static method calls.			Status.inst = this;						initializeFadeSequence(true);		}			public static function show(message:String):void		{			inst._show(message);		}				public function _show(message:String):void		{							trace("Status: " + message);						// Is the sequence already running? 			// (Are we in the middle of showing a status message?)			if (fadeSequence.childrenAreRunning) 			{				// Unless the message is already fading out, kill 				// the sequence and start the fade out.				if (fadeSequence.currentAction.name != "fadeOut")				{					// Reinitialize the sequence.					initializeFadeSequence();										// Fade out the current message (using the current alpha as a starting point					// so that it doesn't jump.)					var fadeOutOldMessage:Tween = new Tween(this, "alpha", 0, alpha, "1s", "0s", Cubic.easeInOut);					fadeOutOldMessage.name = "fadeOut";										fadeSequence.addAction(fadeOutOldMessage);				}			}			// Fade the message in action.			var fadeIn:Tween = new Tween(this, "alpha", 1, 0, "1s", "0s", Cubic.easeInOut);			fadeIn.name = "Fade in: " + message;						// Fade message out action.			var fadeOut:Tween = new Tween(this, "alpha", 0, 1, "1s", "0s", Cubic.easeInOut);			fadeOut.name = "fadeOut";						// Wait action			var wait:Wait = new Wait("4sec");			wait.name = "WAIT on fade sequence " + fadeSequence.name;						// Update label action.			var updateLabel:SynchronizedSetProperty = new SynchronizedSetProperty(messageLabel, "text", message);			updateLabel.name = "Update label: " + message;						// A sequence is already running, add this message to the end of it. 			fadeSequence.addAction(updateLabel)			fadeSequence.addAction(fadeIn);			fadeSequence.addAction(wait);			fadeSequence.addAction(fadeOut);				if (!fadeSequence.childrenAreRunning)			{				fadeSequence.start();				}		}				private function fadeSequenceCompleteHandler(event:SynchronizerEvent):void		{			initializeFadeSequence();		}				private function initializeFadeSequence(firstTime:Boolean = false):void		{						if (fadeSequence != null || firstTime) 			{				if (fadeSequence != null)				{					fadeSequence.removeEventListener(SynchronizerEvent.COMPLETE, fadeSequenceCompleteHandler);					fadeSequence.kill();					fadeSequence = null;					}								fadeSequence = new Sequence();				//fadeSequence.autoDelete = true;				fadeSequence.addEventListener(SynchronizerEvent.COMPLETE, fadeSequenceCompleteHandler)					}			}	}}