package org.gaeswf.flex.components
{
	import flash.errors.IllegalOperationError;
	import flash.events.DataEvent;
	import flash.events.Event;
	import flash.events.HTTPStatusEvent;
	import flash.events.IOErrorEvent;
	import flash.events.MouseEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.FileFilter;
	import flash.net.FileReference;
	import flash.net.URLRequest;
	import flash.net.URLRequestMethod;
	import flash.net.URLVariables;
	import flash.utils.ByteArray;
	
	import lt.uza.utils.Global;
	
	import mx.containers.HBox;
	import mx.containers.Panel;
	import mx.controls.Button;
	import mx.controls.sliderClasses.Slider;
	import mx.events.FlexEvent;
	
	import org.gaeswf.Service;
	import org.gaeswf.examples.initial.Application;
	import org.gaeswf.examples.initial.Model;
	import org.gaeswf.examples.initial.Status;
	import org.gaeswf.examples.initial.ValidationIcons;

	public class PhotoCropperClass extends Panel
	{
		private var fileRef:FileReference;

		public var photo:ScrollImage;
		public var imageZoomSlider:Slider;
		public var photoUploadProgress:ValidationIcons;
		public var uploadPhotoButton:Button;
		public var photoCropButton:Button;
		public var rotateButton:Button;
		public var flipButton:Button;
		
		public var imageTools:HBox;

		public function PhotoCropperClass()
		{
			super();
	
			addEventListener(FlexEvent.UPDATE_COMPLETE, init);
		}
		
		private function init(event:Event):void
		{
			// Load the profile photo
			// TODO: Do this better (preloading, etc.)
			photo.source = Global.getInstance().baseURL + "/photo/download";
			photoUploadProgress.show(ValidationIcons.PROGRESS);

			fileRef = new FileReference();

			// Listeners for file operations.
	        fileRef.addEventListener(Event.SELECT, fileSelectHandler);
	        fileRef.addEventListener(Event.CANCEL, fileCancelHandler);
	        fileRef.addEventListener(ProgressEvent.PROGRESS, fileProgressHandler);
	        fileRef.addEventListener(Event.COMPLETE, fileCompleteHandler);
	        fileRef.addEventListener(HTTPStatusEvent.HTTP_STATUS, fileHttpStatusHandler);
	        fileRef.addEventListener(IOErrorEvent.IO_ERROR, fileIoErrorHandler);
	        fileRef.addEventListener(Event.OPEN, fileOpenHandler);
	        fileRef.addEventListener(SecurityErrorEvent.SECURITY_ERROR, fileSecurityErrorHandler);
	        fileRef.addEventListener(DataEvent.UPLOAD_COMPLETE_DATA,fileUploadCompleteDataHandler);

			// TODO: Add this after image is created.
			photo.addEventListener(Event.CHANGE, profileImageChangeHandler);
			imageZoomSlider.addEventListener(Event.CHANGE, imageZoomChangeHandler);

			uploadPhotoButton.addEventListener(MouseEvent.CLICK, uploadPhotoButtonHandler);
			photoCropButton.addEventListener(MouseEvent.CLICK, photoCropButtonHandler);
			
			// Layout
			imageZoomSlider.y = photo.y + photo.height + 5;
			imageZoomSlider.width=photo.width;
			
			imageTools.y = imageZoomSlider.y + imageZoomSlider.height + 5;
			
			photoUploadProgress.x = photo.x + photo.width/2 - photoUploadProgress.width/2;
			photoUploadProgress.y = photo.y + photo.height/2 - photoUploadProgress.height/2;
			
			rotateButton.addEventListener(MouseEvent.CLICK, rotateButtonHandler);
			
		}
		
		
		override public function set visible(state:Boolean):void
		{
			// Register the mouse wheel for OS X support.
			var app:Application = (Global.getInstance().application) as Application;

			if (state)
			{
				// Register the profile image to listen for mouse wheel events
				app.mouseWheelSupport.registerObject(photo);
			}
			else
			{
				// Unregister the list box.
				if (photo != null)
				{
					app.mouseWheelSupport.unRegisterObject(photo);
				}				
			}

		}
		
		//
		// UI event handlers.
		//
		
		
		private function rotateButtonHandler(event:MouseEvent):void
		{
			photo.rotateBy(90);
		}
				
		private function imageZoomChangeHandler(event:Event):void
		{
			// Zoom the image.
			photo.scale = imageZoomSlider.value;
		}
		
		private function profileImageChangeHandler(event:Event):void
		{
			// The profile image has changed, update the minimum zoom factor on the 
			// slider and reset it. 
			imageZoomSlider.minimum = photo.minScale;
			imageZoomSlider.value = 1;

			// If the image is the right size, don't display the slider.			
			rotateButton.enabled = photoCropButton.enabled = photo.canScroll;
			
			// Fade out the slider if it's disabled (the disabled skin doesn't look disabled enough
			// and I don't want to skin it right now.) 
			imageZoomSlider.enabled = photo.canScale;
			imageZoomSlider.alpha = photo.canScale ? 1 : 0.25;
			
			photoUploadProgress.show(ValidationIcons.NONE);
			
		}
		
		private function photoCropButtonHandler(event:MouseEvent):void
		{
			var croppedPhoto:ByteArray = photo.byteArray;

			photoUploadProgress.show(ValidationIcons.PROGRESS);
			
			execute("photo.uploadByteArray", croppedPhoto);
		}
		
		private function photoUpdateCompleteHandler(event:FlexEvent):void
		{
			photoUploadProgress.show(ValidationIcons.NONE);
		}

		//
		// Service event handlers
		//

		public function photo_uploadByteArrayResponse(result:Object):void
		{
			Status.show("Now that's a spiffy new photo!");
			photoUploadProgress.show(ValidationIcons.PROGRESS);
			
            // Load the cropped photo back from the server.
            // TODO: Implement BulkLoader.
            photo.load(Global.getInstance().baseURL + "/photo/download");
		}
		
		public function photo_getAuthTokenResponse(result:Object):void
		{
			// status.show("Photo auth token: " + Model.photoUploadAuthToken);
			
			trace("Uploading file " + fileRef.name + "...");
			photoUploadProgress.show(ValidationIcons.PROGRESS);
			
			var photoUploadURL:String = Global.getInstance().baseURL+"/photo/upload";
			
			var vars:URLVariables = new URLVariables();
			vars.authToken = Model.photoUploadAuthToken;

			var urlRequest:URLRequest = new URLRequest(photoUploadURL);
			urlRequest.data = vars;
			urlRequest.method = URLRequestMethod.POST;
			
			fileRef.upload(urlRequest, "upload");
		}

		//
		// File upload/download handlers.
		//
		
		private function uploadPhotoButtonHandler(event:MouseEvent):void
		{
			try
			{
				fileRef.browse([new FileFilter("Images", "*.png;*.gif;*.jpg")]);
			}
			catch (illegalOperationError:IllegalOperationError)
			{
				Status.show("There was an error while selecting files.");
			
				trace ("Error while selecting files.");
			}
		}
		
		private function fileSelectHandler(event:Event):void
		{			
			//trace("Uploading photo...");

			if (fileRef.size > 900000) 
			{
				Status.show("The file you selected is too large (over 900KB).");	
			}
			else
			{
				Status.show("Uploading photo...");
				trace("Getting auth token for upload...");
				//trace ("File is the right size.");
				uploadPhotoButton.enabled = false;
				
				// TODO: We sometimes get the wrong type (null) from FileReference -- why?
				var fileRefType:String =  (fileRef.type == null) ? "Unknown" : fileRef.type;
				
				// Get an auth token for the selected file.
				execute("photo.getAuthToken", fileRef.name, fileRef.size, fileRefType);			
			}			
		}
		
		// TODO: Implement execute in the base classes.
		// Execute: Makes a service call
		// TODO: Factor out to a Mixin (we can't use the BaseView base class 
		// as we need to use this method from both the Application class which extends
		// BaseApplication -> mx.core.Application and the Profile class which 
		// extends BaseView -> mx.core.Canvas.
		private function execute(serviceName:String, ...args):void
		{
			// Add the current 
			args.unshift(this);
			args.unshift(serviceName);
			Service.call.apply(Service.call, args);
			
			/*trace("Service called with args: ");
			for (var i:uint = 0; i < args.length; i++)
			{
				trace(i + " = " + args[i]);
			}*/
			
		}
		
		private function fileCancelHandler(event:Event):void
		{
			//status.show("File upload was cancelled.");
			//trace("File upload was cancelled.");
		}
		
		private function fileProgressHandler(event:ProgressEvent):void
		{
			//photoPanel.title = "Photo - " + Math.round(event.bytesLoaded*100/event.bytesTotal);
			trace("File progress: " + Math.round(event.bytesLoaded*100/event.bytesTotal) + "%");
		}

        private function fileCompleteHandler(event:Event):void 
        {
            trace("completeHandler: " + event);
            // Note: It's not really complete until uploadCompleteData gets called.
        }

        private function fileUploadCompleteDataHandler(event:DataEvent):void 
        {
        	//status.show("Photo uploaded successfully!");
        	Status.show("Frame your photo and click OK when ready!");
            trace("uploadCompleteData: " + event);
            
            // TODO: Rename ValidationIcons to Icons (generic). 
			//photoUploadProgress.show(ValidationIcons.NONE);
            uploadPhotoButton.enabled = true;
            
            if (event.data == "True")
            {
            	// Load the photo
            	photo.load(Global.getInstance().baseURL + "/photo/download");
            }
        }

        private function fileHttpStatusHandler(event:HTTPStatusEvent):void 
        {
           trace("httpStatusHandler: " + event);
           //uploadPhotoButton.enabled = true;
        }
        
        private function fileIoErrorHandler(event:IOErrorEvent):void 
        {
            trace("ioErrorHandler: " + event);
            Status.show("Encountered an IO Error.");
			photoUploadProgress.show(ValidationIcons.NONE);
            uploadPhotoButton.enabled = true;
        }

        private function fileOpenHandler(event:Event):void 
        {
            //trace("openHandler: " + event);
        }

        private function fileSecurityErrorHandler(event:SecurityErrorEvent):void 
        {
            trace("securityErrorHandler: " + event);
            Status.show("Encountered a security error.");
            
            uploadPhotoButton.enabled = true;
			photoUploadProgress.show(ValidationIcons.NONE);
        }

	}
}