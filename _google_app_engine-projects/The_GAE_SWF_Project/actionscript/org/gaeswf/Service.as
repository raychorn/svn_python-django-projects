﻿/*	The GAE SWF Project: 	Knowledge and tools to help you build Flash and Flex apps on Google App Engine.		Copyright (c) 2008 Aral Balkan. All Rights Reserved.	Released under the open source MIT License. See LICENSE.txt for full license terms.	Service class (static)	======================	Call remote services and get notified of responses and failures. 		Usage:		You should not have to use the service class directly as all views	have an execute() method that you can use.		Service.call(this, "service.method", arg1, arg2, ...)		Note: Since AS3 does not have arguments.caller, you unfortunately	      have to pass a reference to yourself manually.*/package org.gaeswf{	import flash.events.NetStatusEvent;	import flash.events.SecurityErrorEvent;	import flash.net.NetConnection;		import lt.uza.utils.Global;		public class Service	{		public static var connection:NetConnection = null;		private static var inited:Boolean = false;		private static var listeners:Object;				// The URL to use for the remoting gateway when testing locally in the		// Flash IDE or the Standalone Flash Player. Change this according to your needs.		private static var localGatewayURL:String = "http://localhost:8080/gateway"		//		// Public methods		//						static public function call(serviceName:String, listener:Object, ...args):void		{			// trace ("Service.call: " + serviceName);						// Initialize, if not already initialized.			init();						// Add listener.			listen(serviceName, listener);						// Make the service call. The response or fault will be 			// proxied back to the Service.responseHandler or 			// Service.faultHandler so that listeners can be notified.			var serviceCall:ServiceCall = new ServiceCall(serviceName, args);					}				public static function listen(serviceName:String, listener:Object):void		{			// Initialize, if not already initialized.			init();						// Add listener.			if (listeners[serviceName] == null)			{				listeners[serviceName] = new Array();			}						// Check that we don't add multiple listeners			var l:Array = listeners[serviceName];			var numListeners:uint = l.length;			var found:Boolean = false;			for (var i:uint = 0; i < numListeners; i++)			{				if (l[i] == listener) 				{					found = true;					break;				}			}			if (found) return;						// Listener does not exist, add it.			l.push(listener);						// Debug			/*			trace("");			trace("Listeners");			trace("=========");			for (var j in listeners)			{				trace(j);				for (var k = 0; k < listeners[j].length; k++)				{					trace ("   " + k + " = " + listeners[j][k]);					}			}			*/		}				//		// Private methods.		//				// Initialize the NetConnection.		private static function init():void		{						if (!inited)			{				listeners = new Object();							connection = new NetConnection();								// Rule: The gateway should always be off of the root of your app's URL. 				// e.g. http://localhost:8080/gateway or http://myapp.appspot.com/gateway.				// If you need it elsewhere, you need to modify this code. 								// Here we check if the app is running locally (i.e., when testing in the 				// Flash IDE or via the Standalone Flash Player.) and, if so, connect				// to the URL in the localGatewayURL.								var app:Global = Global.getInstance();				var url:String = (app.isLocal) ? localGatewayURL : app.baseURL + "/gateway";													connection.addEventListener(NetStatusEvent.NET_STATUS, netStatusHandler);				connection.addEventListener(SecurityErrorEvent.SECURITY_ERROR, securityErrorHandler);								connection.connect(url);										inited = true;			}			}				// Returns a handler name from a given service name and handler type. 		private static function getHandlerName(serviceName:String, handlerType:String):String		{			return serviceName.replace(/\./, "_") + handlerType;		}		// Notify listeners that a response or fault has occured on the 		// service that they are listening for. 		private static function notifyListeners(serviceName:String, handlerType:String, eventObj:Object):void		{			var handlerName:String = getHandlerName(serviceName, handlerType);									var serviceListeners:Array = listeners[serviceName];			var numServiceListeners:uint = serviceListeners.length;						for (var i:uint = 0; i < numServiceListeners; i++)			{				var handlerObj:Object = serviceListeners[i];								if (handlerObj.hasOwnProperty(handlerName))				{					handlerObj[handlerName].apply(handlerObj, [eventObj]);									}				else				{					trace ("Warning: No " + handlerName + " found on " + handlerObj);				}			}		}				//		// Event handlers (public; called by ServiceCall instances.)		//				public static function responseHandler(serviceName:String, result:Object):void		{			// Notify listeners			notifyListeners(serviceName, "Response", result);		}				public static function faultHandler(serviceName:String, fault:Object):void		{			trace ("Service fault: ");			for (var i:String in fault)			{				trace (i + " = " + fault[i])			}						// Notify listeners			notifyListeners(serviceName, "Fault", fault);		}				public static function netStatusHandler(event:NetStatusEvent):void		{			trace ("[netStatusHandler] " + event.info.level + ": " + event.info.code);		}		        private static function securityErrorHandler(event:SecurityErrorEvent):void 		{            trace("[securityErrorHandler] " + event);        }			}}