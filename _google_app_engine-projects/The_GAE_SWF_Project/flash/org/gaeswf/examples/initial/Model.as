/*
	The GAE SWF Project: 
	Knowledge and tools to help you build Flash and Flex apps on Google App Engine.	
	Copyright (c) 2008 Aral Balkan. All Rights Reserved.
	Released under the open source MIT License. See LICENSE.txt for full license terms.

	Model class (static)
	====================
	The Model holds the data for the application. It listens for service responses and
	populates its data models in the handlers.  
*/
package org.gaeswf.examples.initial
{
	import org.gaeswf.Service;
	
	// TODO: For larger projects, it might be a good idea to split the model properties into separate classes
	// for things like user, friends, etc. We'll cross that bridge when the Model begins to smell. 
	public class Model
	{
		// Model objects are untyped in this example.
		
		public static var loginURL:String = null;
		public static var logoutURL:String = null;
		
		public static var profile:Object = null;
		public static var user:Object = null;
		public static var auth:Boolean = false;
		
		public static function init():void
		{			
			// Listen for service events
			listen("user.login");
			listen("user.updateProfile");
		}
		
		// Service handlers
		
		// Login data.
		public static function user_loginResponse(result:Object):void
		{
			auth = result.auth;
			loginURL = result.login;
			logoutURL = result.logout;
						
			if (result.user != null)
			{
				user = result.user;
				if (result.profile != null)
				{
					profile = result.profile;		
				}
			}
		}
		
		// Update profile data.
		public static function user_updateProfileResponse(profile:Object):void
		{
			Model.profile = profile;
		}
		
		// Private methods
		
		// Service listener helper
		private static function listen(serviceName):void
		{
			// Add the model as a listener for service responses.
			Service.listen(serviceName, Model);
		}
		
	}
}