
function logoElementLogo1()
{
			
	
	if (navigator.userAgent.indexOf("Mozilla/3") != -1)
	{
		var msg = 'Sorry, since you are using an old version of Netscape, you may not be able to access all the pages in this Web site.';	
		document.write(msg);
	}
	else 
	{
		
		var strHTML = '';

				strHTML += '<a  href="' + strRelativePathToRoot+ 'index.html"';
				strHTML += ' target="" >';
				strHTML += '	<img src="' + strRelativePathToRoot + 'publishImages/logo_Logo1B.jpg"';
				strHTML += ' alt=""';
				strHTML += ' border="0"';
				strHTML += ' width="790"';
				strHTML += ' height="61" >';
				strHTML += '</a>';

		
		document.write(strHTML);
	}
}

		
function netscapeDivCheckLogo1()
{
	
				 			
				
				
	var strAppName = navigator.appName;
	var appVer = parseFloat(navigator.appVersion);
								
	if ( (strAppName == "Netscape") &&
		(appVer >= 4.0 && appVer < 5) ) {  
		document.write("</DIV>");
	}
}
			
			
		
logoElementLogo1();
			
		
netscapeDivCheckLogo1();
	