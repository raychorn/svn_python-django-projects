#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import urllib
import wsgiref.handlers

from google.appengine.api import images
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import models

_content = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
		<meta name="description" content="Pet Sitting Services serving Seal Beach and Long Beach, CA">
		<meta name="keywords" content="cat, kennel, pets, pet sitting, feline, animals, animal care, pet care, cat care, cat sitting, meow, kittens, animal rescue, animal shetlers, cat breeds, all cat breeds, seal beach, long beach, you tube, google, fandango, fandango.com, felinephandango, felinephandango.com, phandango, feline phandango, feline fandango">
		<meta name="generator" content="Built by Vyper Logix Corp.">
		
		<title>Home</title>
		<script type="text/javascript">
			<!--
						function reDo() {
						        top.location.reload();
						}
						if (navigator.appName == 'Netscape' && parseInt(navigator.appVersion) < 5) {
						        top.onresize = reDo;
						}
						dom=document.getElementById
					//-->
		</script>
		<script type="text/javascript">
			<!--
							  
						
  var strRelativePagePath = "index.html".toLowerCase();
  
						
  var strRelativePathToRoot = "";
  



						//-->
		</script>
		<link rel="stylesheet" href="http://www.homestead.com/~media/elements/Text/font_styles_ns4.css" type="text/css">
		<style type="text/css">
			/*
				$Author: Gmcnaughton $
				$Date: 4/09/02 5:50p $, $Revision: 4 $
			*/
			.dummy { font-size: 10px; }
			.size11px { font-size: 11px; }
			.size8 { font-size: 10px; line-height: normal; }
			.size9 { font-size: 12px; line-height: normal; }
			.size10 { font-size: 13px; line-height: normal; }
			.size11 { font-size: 14px; line-height: normal; }
			.size12 { font-size: 16px; line-height: normal; }
			.size14 { font-size: 18px; line-height: normal; }
			.size16 { font-size: 20px; line-height: normal; }
			.size18 { font-size: 24px; line-height: normal; }
			.size20 { font-size: 26px; line-height: normal; }
			.size22 { font-size: 28px; line-height: normal; }
			.size24 { font-size: 32px; line-height: normal; }
			.size26 { font-size: 34px; line-height: normal; }
			.size28 { font-size: 36px; line-height: normal; }
			.size36 { font-size: 48px; line-height: normal; }
			.size48 { font-size: 64px; line-height: normal; }
			.size72 { font-size: 96px; line-height: normal; }
			
			.Arial8 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 10px; line-height: 13px; }
			.Arial9 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 12px; line-height: 15px; }
			.Arial10 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 13px; line-height: 16px; }
			.Arial11 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 14px; line-height: 16px; }
			.Arial12 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 16px; line-height: 18px; }
			.Arial14 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 18px; line-height: 21px; }
			.Arial16 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 20px; line-height: 23px; }
			.Arial18 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 24px; line-height: 27px; }
			.Arial20 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 26px; line-height: 31px; }
			.Arial22 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 28px; line-height: 32px; }
			.Arial24 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 32px; line-height: 36px; }
			.Arial26 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 34px; line-height: 39px; }
			.Arial28 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 36px; line-height: 41px; }
			.Arial36 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 48px; line-height: 55px; }
			.Arial48 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 64px; line-height: 72px; }
			.Arial72 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 96px; line-height: 107px; }
			.Arial8 b, b .Arial8 { line-height: 12px; }
			.Arial12 b, b .Arial12 { line-height: 19px; }
			.Arial16 b, b .Arial16 { line-height: 24px; }
			.Arial18 b, b .Arial18 { line-height: 29px; }
			.Arial20 b, b .Arial20 { line-height: 30px; }
			.Arial22 b, b .Arial22 { line-height: 33px; }
			.Arial24 b, b .Arial24 { line-height: 37px; }
			.Arial26 b, b .Arial26 { line-height: 40px; }
			.Arial28 b, b .Arial28 { line-height: 43px; }
			.Arial36 b, b .Arial36 { line-height: 56px; }
			.Arial48 b, b .Arial48 { line-height: 75px; }
			.Arial72 b, b .Arial72 { line-height: 110px; }
			
			.ArialNarrow8 { font-family: "Arial Narrow"; font-size: 10px; line-height: 14px; }
			.ArialNarrow9 { font-family: "Arial Narrow"; font-size: 12px; line-height: 16px; }
			.ArialNarrow10 { font-family: "Arial Narrow"; font-size: 13px; line-height: 16px; }
			.ArialNarrow11 { font-family: "Arial Narrow"; font-size: 14px; line-height: 17px; }
			.ArialNarrow12 { font-family: "Arial Narrow"; font-size: 16px; line-height: 20px; }
			.ArialNarrow14 { font-family: "Arial Narrow"; font-size: 18px; line-height: 22px; }
			.ArialNarrow16 { font-family: "Arial Narrow"; font-size: 20px; line-height: 24px; }
			.ArialNarrow18 { font-family: "Arial Narrow"; font-size: 24px; line-height: 29px; }
			.ArialNarrow20 { font-family: "Arial Narrow"; font-size: 26px; line-height: 31px; }
			.ArialNarrow22 { font-family: "Arial Narrow"; font-size: 28px; line-height: 33px; }
			.ArialNarrow24 { font-family: "Arial Narrow"; font-size: 32px; line-height: 37px; }
			.ArialNarrow26 { font-family: "Arial Narrow"; font-size: 34px; line-height: 40px; }
			.ArialNarrow28 { font-family: "Arial Narrow"; font-size: 36px; line-height: 42px; }
			.ArialNarrow36 { font-family: "Arial Narrow"; font-size: 48px; line-height: 57px; }
			.ArialNarrow48 { font-family: "Arial Narrow"; font-size: 64px; line-height: 75px; }
			.ArialNarrow72 { font-family: "Arial Narrow"; font-size: 96px; line-height: 110px; }
			
			.BookmanOldStyle8 { font-family: "Bookman Old Style"; font-size: 10px; line-height: 14px; }
			.BookmanOldStyle9 { font-family: "Bookman Old Style"; font-size: 12px; line-height: 16px; }
			.BookmanOldStyle10 { font-family: "Bookman Old Style"; font-size: 13px; line-height: 18px; }
			.BookmanOldStyle11 { font-family: "Bookman Old Style"; font-size: 14px; line-height: 19px; }
			.BookmanOldStyle12 { font-family: "Bookman Old Style"; font-size: 16px; line-height: 20px; }
			.BookmanOldStyle14 { font-family: "Bookman Old Style"; font-size: 18px; line-height: 20px; }
			.BookmanOldStyle16 { font-family: "Bookman Old Style"; font-size: 20px; line-height: 23px; }
			.BookmanOldStyle18 { font-family: "Bookman Old Style"; font-size: 24px; line-height: 27px; }
			.BookmanOldStyle20 { font-family: "Bookman Old Style"; font-size: 26px; line-height: 31px; }
			.BookmanOldStyle22 { font-family: "Bookman Old Style"; font-size: 28px; line-height: 33px; }
			.BookmanOldStyle24 { font-family: "Bookman Old Style"; font-size: 32px; line-height: 39px; }
			.BookmanOldStyle26 { font-family: "Bookman Old Style"; font-size: 34px; line-height: 41px; }
			.BookmanOldStyle28 { font-family: "Bookman Old Style"; font-size: 36px; line-height: 43px; }
			.BookmanOldStyle36 { font-family: "Bookman Old Style"; font-size: 48px; line-height: 58px; }
			.BookmanOldStyle48 { font-family: "Bookman Old Style"; font-size: 64px; line-height: 72px; }
			.BookmanOldStyle72 { font-family: "Bookman Old Style"; font-size: 96px; line-height: 113px; }
			.BookmanOldStyle8 b, b .BookmanOldStyle8 { line-height: 12px; }
			.BookmanOldStyle9 b, b .BookmanOldStyle9 { line-height: 14px; }
			.BookmanOldStyle10 b, b .BookmanOldStyle10 { line-height: 16px; }
			.BookmanOldStyle11 b, b .BookmanOldStyle11 { line-height: 17px; }
			.BookmanOldStyle12 b, b .BookmanOldStyle12 { line-height: 19px; }
			.BookmanOldStyle14 b, b .BookmanOldStyle14 { line-height: 21px; }
			.BookmanOldStyle16 b, b .BookmanOldStyle16 { line-height: 24px; }
			.BookmanOldStyle18 b, b .BookmanOldStyle18 { line-height: 28px; }
			.BookmanOldStyle20 b, b .BookmanOldStyle20 { line-height: 30px; }
			.BookmanOldStyle22 b, b .BookmanOldStyle22 { line-height: 32px; }
			.BookmanOldStyle24 b, b .BookmanOldStyle24 { line-height: 38px; }
			.BookmanOldStyle26 b, b .BookmanOldStyle26 { line-height: 40px; }
			.BookmanOldStyle28 b, b .BookmanOldStyle28 { line-height: 42px; }
			.BookmanOldStyle36 b, b .BookmanOldStyle36 { line-height: 56px; }
			.BookmanOldStyle48 b, b .BookmanOldStyle48 { line-height: 75px; }
			.BookmanOldStyle72 b, b .BookmanOldStyle72 { line-height: 112px; }
			
			.Courier8 { font-family: Courier New, adobe-courier, Courier; font-size: 10px; line-height: 12px; }
			.Courier9 { font-family: Courier New, adobe-courier, Courier; font-size: 12px; line-height: 15px; }
			.Courier10 { font-family: Courier New, adobe-courier, Courier; font-size: 13px; line-height: 16px; }
			.Courier11 { font-family: Courier New, adobe-courier, Courier; font-size: 14px; line-height: 17px; }
			.Courier12 { font-family: Courier New, adobe-courier, Courier; font-size: 16px; line-height: 18px; }
			.Courier14 { font-family: Courier New, adobe-courier, Courier; font-size: 18px; line-height: 20px; }
			.Courier16 { font-family: Courier New, adobe-courier, Courier; font-size: 20px; line-height: 22px; }
			.Courier18 { font-family: Courier New, adobe-courier, Courier; font-size: 24px; line-height: 27px; }
			.Courier20 { font-family: Courier New, adobe-courier, Courier; font-size: 26px; line-height: 29px; }
			.Courier22 { font-family: Courier New, adobe-courier, Courier; font-size: 28px; line-height: 31px; }
			.Courier24 { font-family: Courier New, adobe-courier, Courier; font-size: 32px; line-height: 36px; }
			.Courier26 { font-family: Courier New, adobe-courier, Courier; font-size: 34px; line-height: 37px; }
			.Courier28 { font-family: Courier New, adobe-courier, Courier; font-size: 36px; line-height: 39px; }
			.Courier36 { font-family: Courier New, adobe-courier, Courier; font-size: 48px; line-height: 50px; }
			.Courier48 { font-family: Courier New, adobe-courier, Courier; font-size: 64px; line-height: 69px; }
			.Courier72 { font-family: Courier New, adobe-courier, Courier; font-size: 96px; line-height: 103px; }
			.Courier8 b, b .Courier8 { line-height: 13px; }
			.Courier9 b, b .Courier9 { line-height: 16px; }
			.Courier11 b, b .Courier11 { line-height: 16px; }
			.Courier14 b, b .Courier14 { line-height: 21px; }
			.Courier16 b, b .Courier16 { line-height: 23px; }
			.Courier20 b, b .Courier20 { line-height: 30px; }
			.Courier28 b, b .Courier28 { line-height: 41px; }
			.Courier36 b, b .Courier36 { line-height: 54px; }
			.Courier48 b, b .Courier48 { line-height: 73px; }
			.Courier72 b, b .Courier72 { line-height: 110px; }
			
			.Garamond8 { font-family: Garamond; font-size: 10px; line-height: 12px; }
			
			.Haettenschweiler8 { font-family: Haettenschweiler; font-size: 10px; line-height: 11px; }
			.Haettenschweiler9 { font-family: Haettenschweiler; font-size: 12px; line-height: 12px; }
			.Haettenschweiler10 { font-family: Haettenschweiler; font-size: 13px; line-height: 14px; }
			.Haettenschweiler11 { font-family: Haettenschweiler; font-size: 14px; line-height: 16px; }
			.Haettenschweiler12 { font-family: Haettenschweiler; font-size: 16px; line-height: 17px; }
			.Haettenschweiler14 { font-family: Haettenschweiler; font-size: 18px; line-height: 19px; }
			.Haettenschweiler16 { font-family: Haettenschweiler; font-size: 20px; line-height: 22px; }
			.Haettenschweiler18 { font-family: Haettenschweiler; font-size: 24px; line-height: 26px; }
			.Haettenschweiler20 { font-family: Haettenschweiler; font-size: 26px; line-height: 27px; }
			.Haettenschweiler22 { font-family: Haettenschweiler; font-size: 28px; line-height: 29px; }
			.Haettenschweiler24 { font-family: Haettenschweiler; font-size: 32px; line-height: 34px; }
			.Haettenschweiler26 { font-family: Haettenschweiler; font-size: 34px; line-height: 35px; }
			.Haettenschweiler28 { font-family: Haettenschweiler; font-size: 36px; line-height: 37px; }
			.Haettenschweiler36 { font-family: Haettenschweiler; font-size: 48px; line-height: 50px; }
			.Haettenschweiler48 { font-family: Haettenschweiler; font-size: 64px; line-height: 67px; }
			.Haettenschweiler72 { font-family: Haettenschweiler; font-size: 96px; line-height: 101px; }
			
			.Helvetica8 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 10px; line-height: 13px; }
			.Helvetica9 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 12px; line-height: 15px; }
			.Helvetica10 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 13px; line-height: 16px; }
			.Helvetica11 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 14px; line-height: 16px; }
			.Helvetica12 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 16px; line-height: 18px; }
			.Helvetica14 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 18px; line-height: 21px; }
			.Helvetica16 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 20px; line-height: 23px; }
			.Helvetica18 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 24px; line-height: 27px; }
			.Helvetica20 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 26px; line-height: 31px; }
			.Helvetica22 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 28px; line-height: 32px; }
			.Helvetica24 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 32px; line-height: 36px; }
			.Helvetica26 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 34px; line-height: 39px; }
			.Helvetica28 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 36px; line-height: 41px; }
			.Helvetica36 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 48px; line-height: 55px; }
			.Helvetica48 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 64px; line-height: 72px; }
			.Helvetica72 { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 96px; line-height: 107px; }
			.Helvetica8 b, b .Helvetica8 { line-height: 12px; }
			.Helvetica12 b, b .Helvetica12 { line-height: 19px; }
			.Helvetica16 b, b .Helvetica16 { line-height: 24px; }
			.Helvetica18 b, b .Helvetica18 { line-height: 29px; }
			.Helvetica20 b, b .Helvetica20 { line-height: 30px; }
			.Helvetica22 b, b .Helvetica22 { line-height: 33px; }
			.Helvetica24 b, b .Helvetica24 { line-height: 37px; }
			.Helvetica26 b, b .Helvetica26 { line-height: 40px; }
			.Helvetica28 b, b .Helvetica28 { line-height: 43px; }
			.Helvetica36 b, b .Helvetica36 { line-height: 56px; }
			.Helvetica48 b, b .Helvetica48 { line-height: 75px; }
			.Helvetica72 b, b .Helvetica72 { line-height: 110px; }
			
			.FranklinGothicMedium8 { font-family: "Franklin Gothic Medium"; font-size: 10px; line-height: 14px; }
			.FranklinGothicMedium9 { font-family: "Franklin Gothic Medium"; font-size: 12px; line-height: 16px; }
			.FranklinGothicMedium10 { font-family: "Franklin Gothic Medium"; font-size: 13px; line-height: 17px; }
			.FranklinGothicMedium11 { font-family: "Franklin Gothic Medium"; font-size: 14px; line-height: 18px; }
			.FranklinGothicMedium12 { font-family: "Franklin Gothic Medium"; font-size: 16px; line-height: 21px; }
			.FranklinGothicMedium14 { font-family: "Franklin Gothic Medium"; font-size: 18px; line-height: 23px; }
			.FranklinGothicMedium16 { font-family: "Franklin Gothic Medium"; font-size: 20px; line-height: 25px; }
			.FranklinGothicMedium18 { font-family: "Franklin Gothic Medium"; font-size: 24px; line-height: 30px; }
			.FranklinGothicMedium20 { font-family: "Franklin Gothic Medium"; font-size: 26px; line-height: 33px; }
			.FranklinGothicMedium22 { font-family: "Franklin Gothic Medium"; font-size: 28px; line-height: 36px; }
			.FranklinGothicMedium24 { font-family: "Franklin Gothic Medium"; font-size: 32px; line-height: 37px; }
			.FranklinGothicMedium26 { font-family: "Franklin Gothic Medium"; font-size: 34px; line-height: 39px; }
			.FranklinGothicMedium28 { font-family: "Franklin Gothic Medium"; font-size: 36px; line-height: 42px; }
			.FranklinGothicMedium36 { font-family: "Franklin Gothic Medium"; font-size: 48px; line-height: 61px; }
			.FranklinGothicMedium48 { font-family: "Franklin Gothic Medium"; font-size: 64px; line-height: 81px; }
			.FranklinGothicMedium72 { font-family: "Franklin Gothic Medium"; font-size: 96px; line-height: 120px; }
			
			.Impact8 { font-family: Impact; font-size: 10px; line-height: 14px; }
			.Impact9 { font-family: Impact; font-size: 12px; line-height: 16px; }
			.Impact10 { font-family: Impact; font-size: 13px; line-height: 17px; }
			.Impact11 { font-family: Impact; font-size: 14px; line-height: 18px; }
			.Impact12 { font-family: Impact; font-size: 16px; line-height: 20px; }
			.Impact14 { font-family: Impact; font-size: 18px; line-height: 22px; }
			.Impact16 { font-family: Impact; font-size: 20px; line-height: 25px; }
			.Impact18 { font-family: Impact; font-size: 24px; line-height: 29px; }
			.Impact20 { font-family: Impact; font-size: 26px; line-height: 33px; }
			.Impact22 { font-family: Impact; font-size: 28px; line-height: 35px; }
			.Impact24 { font-family: Impact; font-size: 32px; line-height: 39px; }
			.Impact26 { font-family: Impact; font-size: 34px; line-height: 42px; }
			.Impact28 { font-family: Impact; font-size: 36px; line-height: 44px; }
			.Impact36 { font-family: Impact; font-size: 48px; line-height: 60px; }
			.Impact48 { font-family: Impact; font-size: 64px; line-height: 80px; }
			.Impact72 { font-family: Impact; font-size: 96px; line-height: 117px; }
			
			.LucidaConsole8 { font-family: "Lucida Console"; font-size: 10px; line-height: 10px; }
			.LucidaConsole9 { font-family: "Lucida Console"; font-size: 12px; line-height: 12px; }
			.LucidaConsole10 { font-family: "Lucida Console"; font-size: 13px; line-height: 13px; }
			.LucidaConsole11 { font-family: "Lucida Console"; font-size: 14px; line-height: 14px; }
			.LucidaConsole12 { font-family: "Lucida Console"; font-size: 16px; line-height: 16px; }
			.LucidaConsole14 { font-family: "Lucida Console"; font-size: 18px; line-height: 18px; }
			.LucidaConsole16 { font-family: "Lucida Console"; font-size: 20px; line-height: 20px; }
			.LucidaConsole18 { font-family: "Lucida Console"; font-size: 24px; line-height: 24px; }
			.LucidaConsole20 { font-family: "Lucida Console"; font-size: 26px; line-height: 26px; }
			.LucidaConsole22 { font-family: "Lucida Console"; font-size: 28px; line-height: 28px; }
			.LucidaConsole24 { font-family: "Lucida Console"; font-size: 32px; line-height: 32px; }
			.LucidaConsole26 { font-family: "Lucida Console"; font-size: 34px; line-height: 34px; }
			.LucidaConsole28 { font-family: "Lucida Console"; font-size: 36px; line-height: 36px; }
			.LucidaConsole36 { font-family: "Lucida Console"; font-size: 48px; line-height: 48px; }
			.LucidaConsole48 { font-family: "Lucida Console"; font-size: 64px; line-height: 64px; }
			.LucidaConsole72 { font-family: "Lucida Console"; font-size: 96px; line-height: 96px; }
			
			.LucidaSansUnicode8 { font-family: "Lucida Sans Unicode"; font-size: 10px; line-height: 14px; }
			.LucidaSansUnicode9 { font-family: "Lucida Sans Unicode"; font-size: 12px; line-height: 16px; }
			.LucidaSansUnicode10 { font-family: "Lucida Sans Unicode"; font-size: 13px; line-height: 16px; }
			.LucidaSansUnicode11 { font-family: "Lucida Sans Unicode"; font-size: 14px; line-height: 17px; }
			.LucidaSansUnicode12 { font-family: "Lucida Sans Unicode"; font-size: 16px; line-height: 20px; }
			.LucidaSansUnicode14 { font-family: "Lucida Sans Unicode"; font-size: 18px; line-height: 22px; }
			.LucidaSansUnicode16 { font-family: "Lucida Sans Unicode"; font-size: 20px; line-height: 23px; }
			.LucidaSansUnicode18 { font-family: "Lucida Sans Unicode"; font-size: 24px; line-height: 28px; }
			.LucidaSansUnicode20 { font-family: "Lucida Sans Unicode"; font-size: 26px; line-height: 32px; }
			.LucidaSansUnicode22 { font-family: "Lucida Sans Unicode"; font-size: 28px; line-height: 34px; }
			.LucidaSansUnicode24 { font-family: "Lucida Sans Unicode"; font-size: 32px; line-height: 39px; }
			.LucidaSansUnicode26 { font-family: "Lucida Sans Unicode"; font-size: 34px; line-height: 42px; }
			.LucidaSansUnicode28 { font-family: "Lucida Sans Unicode"; font-size: 36px; line-height: 44px; }
			.LucidaSansUnicode36 { font-family: "Lucida Sans Unicode"; font-size: 48px; line-height: 59px; }
			.LucidaSansUnicode48 { font-family: "Lucida Sans Unicode"; font-size: 64px; line-height: 78px; }
			.LucidaSansUnicode72 { font-family: "Lucida Sans Unicode"; font-size: 96px; line-height: 116px; }
			
			.MicrosoftSansSerif8 { font-family: "Microsoft Sans Serif"; font-size: 10px; line-height: 13px; }
			.MicrosoftSansSerif9 { font-family: "Microsoft Sans Serif"; font-size: 12px; line-height: 15px; }
			.MicrosoftSansSerif10 { font-family: "Microsoft Sans Serif"; font-size: 13px; line-height: 16px; }
			.MicrosoftSansSerif11 { font-family: "Microsoft Sans Serif"; font-size: 14px; line-height: 17px; }
			.MicrosoftSansSerif12 { font-family: "Microsoft Sans Serif"; font-size: 16px; line-height: 20px; }
			.MicrosoftSansSerif14 { font-family: "Microsoft Sans Serif"; font-size: 18px; line-height: 22px; }
			.MicrosoftSansSerif16 { font-family: "Microsoft Sans Serif"; font-size: 20px; line-height: 25px; }
			.MicrosoftSansSerif18 { font-family: "Microsoft Sans Serif"; font-size: 24px; line-height: 29px; }
			.MicrosoftSansSerif20 { font-family: "Microsoft Sans Serif"; font-size: 26px; line-height: 30px; }
			.MicrosoftSansSerif22 { font-family: "Microsoft Sans Serif"; font-size: 28px; line-height: 32px; }
			.MicrosoftSansSerif24 { font-family: "Microsoft Sans Serif"; font-size: 32px; line-height: 37px; }
			.MicrosoftSansSerif26 { font-family: "Microsoft Sans Serif"; font-size: 34px; line-height: 39px; }
			.MicrosoftSansSerif28 { font-family: "Microsoft Sans Serif"; font-size: 36px; line-height: 40px; }
			.MicrosoftSansSerif36 { font-family: "Microsoft Sans Serif"; font-size: 48px; line-height: 55px; }
			.MicrosoftSansSerif48 { font-family: "Microsoft Sans Serif"; font-size: 64px; line-height: 73px; }
			.MicrosoftSansSerif72 { font-family: "Microsoft Sans Serif"; font-size: 96px; line-height: 108px; }
			
			/* Firefox does not have Modern font face. */
			.Modern8 { font-family: Modern; font-size: 10px; line-height: 11px; }
			.Modern9 { font-family: Modern; font-size: 12px; line-height: 14px; }
			.Modern10 { font-family: Modern; font-size: 13px; line-height: 15px; }
			.Modern11 { font-family: Modern; font-size: 14px; line-height: 16px; }
			.Modern12 { font-family: Modern; font-size: 16px; line-height: 18px; }
			.Modern14 { font-family: Modern; font-size: 18px; line-height: 21px; }
			.Modern16 { font-family: Modern; font-size: 20px; line-height: 23px; }
			.Modern18 { font-family: Modern; font-size: 24px; line-height: 27px; }
			.Modern20 { font-family: Modern; font-size: 26px; line-height: 30px; }
			.Modern22 { font-family: Modern; font-size: 28px; line-height: 32px; }
			.Modern24 { font-family: Modern; font-size: 32px; line-height: 37px; }
			.Modern26 { font-family: Modern; font-size: 34px; line-height: 39px; }
			.Modern28 { font-family: Modern; font-size: 36px; line-height: 41px; }
			.Modern36 { font-family: Modern; font-size: 48px; line-height: 55px; }
			.Modern48 { font-family: Modern; font-size: 64px; line-height: 73px; }
			.Modern72 { font-family: Modern; font-size: 96px; line-height: 110px; }
			
			.MSSansSerif8 { font-family: "MS Sans Serif"; font-size: 10px; line-height: 13px; }
			.MSSansSerif9 { font-family: "MS Sans Serif"; font-size: 12px; line-height: 13px; }
			.MSSansSerif10 { font-family: "MS Sans Serif"; font-size: 13px; line-height: 16px; }
			.MSSansSerif11 { font-family: "MS Sans Serif"; font-size: 14px; line-height: 16px; }
			.MSSansSerif12 { font-family: "MS Sans Serif"; font-size: 16px; line-height: 20px; }
			.MSSansSerif14 { font-family: "MS Sans Serif"; font-size: 18px; line-height: 24px; }
			.MSSansSerif16 { font-family: "MS Sans Serif"; font-size: 20px; line-height: 24px; }
			.MSSansSerif18 { font-family: "MS Sans Serif"; font-size: 24px; line-height: 29px; }
			.MSSansSerif20 { font-family: "MS Sans Serif"; font-size: 26px; line-height: 32px; }
			.MSSansSerif22 { font-family: "MS Sans Serif"; font-size: 28px; line-height: 32px; }
			.MSSansSerif24 { font-family: "MS Sans Serif"; font-size: 32px; line-height: 37px; }
			.MSSansSerif26 { font-family: "MS Sans Serif"; font-size: 34px; line-height: 37px; }
			.MSSansSerif28 { font-family: "MS Sans Serif"; font-size: 36px; line-height: 48px; }
			.MSSansSerif36 { font-family: "MS Sans Serif"; font-size: 48px; line-height: 58px; }
			.MSSansSerif48 { font-family: "MS Sans Serif"; font-size: 64px; line-height: 74px; }
			.MSSansSerif72 { font-family: "MS Sans Serif"; font-size: 96px; line-height: 111px; }
			
			.MSSerif8 { font-family: "MS Serif"; font-size: 10px; line-height: 11px; }
			.MSSerif9 { font-family: "MS Serif"; font-size: 12px; line-height: 13px; }
			.MSSerif10 { font-family: "MS Serif"; font-size: 13px; line-height: 16px; }
			.MSSerif11 { font-family: "MS Serif"; font-size: 14px; line-height: 16px; }
			.MSSerif12 { font-family: "MS Serif"; font-size: 16px; line-height: 19px; }
			.MSSerif14 { font-family: "MS Serif"; font-size: 18px; line-height: 21px; }
			.MSSerif16 { font-family: "MS Serif"; font-size: 20px; line-height: 21px; }
			.MSSerif18 { font-family: "MS Serif"; font-size: 24px; line-height: 27px; }
			.MSSerif20 { font-family: "MS Serif"; font-size: 26px; line-height: 32px; }
			.MSSerif22 { font-family: "MS Serif"; font-size: 28px; line-height: 33px; }
			.MSSerif24 { font-family: "MS Serif"; font-size: 32px; line-height: 35px; }
			.MSSerif26 { font-family: "MS Serif"; font-size: 34px; line-height: 35px; }
			.MSSerif28 { font-family: "MS Serif"; font-size: 36px; line-height: 42px; }
			.MSSerif36 { font-family: "MS Serif"; font-size: 48px; line-height: 54px; }
			.MSSerif48 { font-family: "MS Serif"; font-size: 64px; line-height: 70px; }
			.MSSerif72 { font-family: "MS Serif"; font-size: 96px; line-height: 105px; }
			
			.PalatinoLinotype8 { font-family: "Palatino Linotype"; font-size: 10px; line-height: 14px; }
			.PalatinoLinotype9 { font-family: "Palatino Linotype"; font-size: 12px; line-height: 17px; }
			.PalatinoLinotype10 { font-family: "Palatino Linotype"; font-size: 13px; line-height: 18px; }
			.PalatinoLinotype11 { font-family: "Palatino Linotype"; font-size: 14px; line-height: 19px; }
			.PalatinoLinotype12 { font-family: "Palatino Linotype"; font-size: 16px; line-height: 22px; }
			.PalatinoLinotype14 { font-family: "Palatino Linotype"; font-size: 18px; line-height: 24px; }
			.PalatinoLinotype16 { font-family: "Palatino Linotype"; font-size: 20px; line-height: 27px; }
			.PalatinoLinotype18 { font-family: "Palatino Linotype"; font-size: 24px; line-height: 32px; }
			.PalatinoLinotype20 { font-family: "Palatino Linotype"; font-size: 26px; line-height: 35px; }
			.PalatinoLinotype22 { font-family: "Palatino Linotype"; font-size: 28px; line-height: 37px; }
			.PalatinoLinotype24 { font-family: "Palatino Linotype"; font-size: 32px; line-height: 44px; }
			.PalatinoLinotype26 { font-family: "Palatino Linotype"; font-size: 34px; line-height: 46px; }
			.PalatinoLinotype28 { font-family: "Palatino Linotype"; font-size: 36px; line-height: 49px; }
			.PalatinoLinotype36 { font-family: "Palatino Linotype"; font-size: 48px; line-height: 64px; }
			.PalatinoLinotype48 { font-family: "Palatino Linotype"; font-size: 64px; line-height: 86px; }
			.PalatinoLinotype72 { font-family: "Palatino Linotype"; font-size: 96px; line-height: 129px; }
			
			.PalatinoLinotype8 b { font-family: "Palatino Linotype"; font-size: 10px; line-height: 15px; }
			.PalatinoLinotype22 b { font-family: "Palatino Linotype"; font-size: 28px; line-height: 38px; }
			.PalatinoLinotype36 b { font-family: "Palatino Linotype"; font-size: 48px; line-height: 65px; }
			.PalatinoLinotype48 b { font-family: "Palatino Linotype"; font-size: 64px; line-height: 87px; }
			
			.Roman8 { font-family: Roman; font-size: 10px; line-height: 11px; }
			.Roman9 { font-family: Roman; font-size: 12px; line-height: 14px; }
			.Roman10 { font-family: Roman; font-size: 13px; line-height: 15px; }
			.Roman11 { font-family: Roman; font-size: 14px; line-height: 16px; }
			.Roman12 { font-family: Roman; font-size: 16px; line-height: 18px; }
			.Roman14 { font-family: Roman; font-size: 18px; line-height: 21px; }
			.Roman16 { font-family: Roman; font-size: 20px; line-height: 23px; }
			.Roman18 { font-family: Roman; font-size: 24px; line-height: 27px; }
			.Roman20 { font-family: Roman; font-size: 26px; line-height: 30px; }
			.Roman22 { font-family: Roman; font-size: 28px; line-height: 32px; }
			.Roman24 { font-family: Roman; font-size: 32px; line-height: 37px; }
			.Roman26 { font-family: Roman; font-size: 34px; line-height: 39px; }
			.Roman28 { font-family: Roman; font-size: 36px; line-height: 41px; }
			.Roman36 { font-family: Roman; font-size: 48px; line-height: 55px; }
			.Roman48 { font-family: Roman; font-size: 64px; line-height: 73px; }
			.Roman72 { font-family: Roman; font-size: 96px; line-height: 110px; }
			
			.SmallFonts48 { font-family: "Small Font"; font-size: 64px; line-height: 72px; }
			.SmallFonts72 { font-family: "Small Font"; font-size: 96px; line-height: 107px; }
			.SmallFonts48 b, b .SmallFonts48 { font-family: "Small Fonts"; font-size: 64px; line-height: 75px; }
			.SmallFonts72 b, b .SmallFonts72 { font-family: "Small Fonts"; font-size: 96px; line-height: 111px; }
			
			/* Firefox does not have Script font face. Used 'French Script MT' instead.
			   Since the font width for Script is very narrow, the line height is incorrect.
			*/
			.Script8 { font-family: Script, 'French Script MT'; font-size: 10px; line-height: 11px; }
			.Script9 { font-family: Script, 'French Script MT'; font-size: 12px; line-height: 13px; }
			.Script10 { font-family: Script, 'French Script MT'; font-size: 13px; line-height: 15px; }
			.Script11 { font-family: Script, 'French Script MT'; font-size: 14px; line-height: 16px; }
			.Script12 { font-family: Script, 'French Script MT'; font-size: 16px; line-height: 18px; }
			.Script14 { font-family: Script, 'French Script MT'; font-size: 18px; line-height: 20px; }
			.Script16 { font-family: Script, 'French Script MT'; font-size: 20px; line-height: 22px; }
			.Script18 { font-family: Script, 'French Script MT'; font-size: 24px; line-height: 27px; }
			.Script20 { font-family: Script, 'French Script MT'; font-size: 26px; line-height: 29px; }
			.Script22 { font-family: Script, 'French Script MT'; font-size: 28px; line-height: 31px; }
			.Script24 { font-family: Script, 'French Script MT'; font-size: 32px; line-height: 36px; }
			.Script26 { font-family: Script, 'French Script MT'; font-size: 34px; line-height: 38px; }
			.Script28 { font-family: Script, 'French Script MT'; font-size: 36px; line-height: 40px; }
			.Script36 { font-family: Script, 'French Script MT'; font-size: 48px; line-height: 54px; }
			.Script48 { font-family: Script, 'French Script MT'; font-size: 64px; line-height: 72px; }
			.Script72 { font-family: Script, 'French Script MT'; font-size: 96px; line-height: 108px; }
			
			/* When font-family: Symbol is specified, FireFox cannot display the correct 
			   font. Need to rely on face=&quot;Symbol&quot;. Also note that Symbol 
			   sizes 12, 14, 18, 24 cannot be fixed with line-height.
			*/
			.Symbol8 { font-size: 10px; line-height: 12px; }
			.Symbol9 { font-size: 12px; line-height: 15px; }
			.Symbol10 { font-size: 13px; line-height: 16px; }
			.Symbol11 { font-size: 14px; line-height: 17px; }
			.Symbol12 { font-size: 16px; line-height: 19px; }
			.Symbol14 { font-size: 18px; line-height: 21px; }
			.Symbol16 { font-size: 20px; line-height: 24px; }
			.Symbol18 { font-size: 24px; line-height: 27px; }
			.Symbol20 { font-size: 26px; line-height: 32px; }
			.Symbol22 { font-size: 28px; line-height: 35px; }
			.Symbol24 { font-size: 32px; line-height: 35px; }
			.Symbol26 { font-size: 34px; line-height: 41px; }
			.Symbol28 { font-size: 36px; line-height: 44px; }
			.Symbol36 { font-size: 48px; line-height: 59px; }
			.Symbol48 { font-size: 64px; line-height: 78px; }
			.Symbol72 { font-size: 96px; line-height: 118px; }
			.Symbol12 b, b .Symbol12 { font-size: 16px; line-height: 20px; }
			.Symbol14 b, b .Symbol14 { font-size: 18px; line-height: 22px; }
			.Symbol18 b, b .Symbol18 { font-size: 24px; line-height: 30px; }
			.Symbol24 b, b .Symbol24 { font-size: 32px; line-height: 39px; }
			
			.TimesRoman8 { font-family: Times New Roman, adobe-times, Times; font-size: 10px; line-height: 12px; }
			.TimesRoman9 { font-family: Times New Roman, adobe-times, Times; font-size: 12px; line-height: 15px; }
			.TimesRoman10 { font-family: Times New Roman, adobe-times, Times; font-size: 13px; line-height: 15px; }
			.TimesRoman11 { font-family: Times New Roman, adobe-times, Times; font-size: 14px; line-height: 16px; }
			.TimesRoman12 { font-family: Times New Roman, adobe-times, Times; font-size: 16px; line-height: 19px; }
			.TimesRoman14 { font-family: Times New Roman, adobe-times, Times; font-size: 18px; line-height: 20px; }
			.TimesRoman16 { font-family: Times New Roman, adobe-times, Times; font-size: 20px; line-height: 22px; }
			.TimesRoman18 { font-family: Times New Roman, adobe-times, Times; font-size: 24px; line-height: 27px; }
			.TimesRoman20 { font-family: Times New Roman, adobe-times, Times; font-size: 26px; line-height: 29px; }
			.TimesRoman22 { font-family: Times New Roman, adobe-times, Times; font-size: 28px; line-height: 33px; }
			.TimesRoman24 { font-family: Times New Roman, adobe-times, Times; font-size: 32px; line-height: 36px; }
			.TimesRoman26 { font-family: Times New Roman, adobe-times, Times; font-size: 34px; line-height: 39px; }
			.TimesRoman28 { font-family: Times New Roman, adobe-times, Times; font-size: 36px; line-height: 41px; }
			.TimesRoman36 { font-family: Times New Roman, adobe-times, Times; font-size: 48px; line-height: 55px; }
			.TimesRoman48 { font-family: Times New Roman, adobe-times, Times; font-size: 64px; line-height: 73px; }
			.TimesRoman72 { font-family: Times New Roman, adobe-times, Times; font-size: 96px; line-height: 109px; }
			.TimesRoman11 b, b .TimesRoman11 { line-height: 17px; }
			.TimesRoman16 b, b .TimesRoman16 { line-height: 23px; }
			.TimesRoman18 b, b .TimesRoman18 { line-height: 26px; }
			.TimesRoman20 b, b .TimesRoman20 { line-height: 30px; }
			.TimesRoman22 b, b .TimesRoman22 { line-height: 32px; }
			.TimesRoman26 b, b .TimesRoman26 { line-height: 38px; }
			
			.TrebuchetMS8 { font-family: "Trebuchet MS"; font-size: 10px; line-height: 15px; }
			.TrebuchetMS9 { font-family: "Trebuchet MS"; font-size: 12px; line-height: 18px; }
			.TrebuchetMS10 { font-family: "Trebuchet MS"; font-size: 13px; line-height: 18px; }
			.TrebuchetMS11 { font-family: "Trebuchet MS"; font-size: 14px; line-height: 18px; }
			.TrebuchetMS12 { font-family: "Trebuchet MS"; font-size: 16px; line-height: 22px; }
			.TrebuchetMS14 { font-family: "Trebuchet MS"; font-size: 18px; line-height: 23px; }
			.TrebuchetMS16 { font-family: "Trebuchet MS"; font-size: 20px; line-height: 26px; }
			.TrebuchetMS18 { font-family: "Trebuchet MS"; font-size: 24px; line-height: 29px; }
			.TrebuchetMS20 { font-family: "Trebuchet MS"; font-size: 26px; line-height: 33px; }
			.TrebuchetMS22 { font-family: "Trebuchet MS"; font-size: 28px; line-height: 36px; }
			.TrebuchetMS24 { font-family: "Trebuchet MS"; font-size: 32px; line-height: 40px; }
			.TrebuchetMS26 { font-family: "Trebuchet MS"; font-size: 34px; line-height: 43px; }
			.TrebuchetMS28 { font-family: "Trebuchet MS"; font-size: 36px; line-height: 44px; }
			.TrebuchetMS36 { font-family: "Trebuchet MS"; font-size: 48px; line-height: 61px; }
			.TrebuchetMS48 { font-family: "Trebuchet MS"; font-size: 64px; line-height: 81px; }
			.TrebuchetMS72 { font-family: "Trebuchet MS"; font-size: 96px; line-height: 119px; }
			
			/* When font-family: Webdings is specified, FireFox cannot display the correct 
			   font. Need to rely on face=&quot;Webdings&quot;
			*/
			.Webdings8 { font-size: 10px; line-height: 16px; }
			.Webdings9 { font-size: 12px; line-height: 19px; }
			.Webdings10 { font-size: 13px; line-height: 18px; }
			.Webdings11 { font-size: 14px; line-height: 20px; }
			.Webdings12 { font-size: 16px; line-height: 19px; }
			.Webdings14 { font-size: 18px; line-height: 21px; }
			.Webdings16 { font-size: 20px; line-height: 24px; }
			.Webdings18 { font-size: 24px; line-height: 26px; }
			.Webdings20 { font-size: 26px; line-height: 29px; }
			.Webdings22 { font-size: 28px; line-height: 31px; }
			.Webdings24 { font-size: 32px; line-height: 33px; }
			.Webdings26 {  font-size: 34px; line-height: 34px; }
			.Webdings28 { font-size: 36px; line-height: 38px; }
			.Webdings36 { font-size: 48px; line-height: 49px; }
			.Webdings48 { font-size: 64px; line-height: 65px; }
			.Webdings72 { font-size: 96px; line-height: 97px; }
			
			.Wingdings8 { font-size: 10px; line-height: 12px; }
			.Wingdings9 { font-size: 12px; line-height: 14px; }
			.Wingdings10 { font-size: 13px; line-height: 15px; }
			.Wingdings11 { font-size: 14px; line-height: 15px; }
			.Wingdings12 { font-size: 16px; line-height: 17px; }
			.Wingdings14 { font-size: 18px; line-height: 20px; }
			.Wingdings16 { font-size: 20px; line-height: 22px; }
			.Wingdings18 { font-size: 24px; line-height: 26px; }
			.Wingdings20 { font-size: 26px; line-height: 28px; }
			.Wingdings22 { font-size: 28px; line-height: 31px; }
			.Wingdings24 { font-size: 32px; line-height: 36px; }
			.Wingdings26 { font-size: 34px; line-height: 37px; }
			.Wingdings28 { font-size: 36px; line-height: 40px; }
			.Wingdings36 { font-size: 48px; line-height: 53px; }
			.Wingdings48 { font-size: 64px; line-height: 71px; }
			.Wingdings72 { font-size: 96px; line-height: 106px; }
			
			/* padding: 2px 0px 1px 39px are the values specified by SB. The vertical padding is placed on the li because SBL allows new li nodes to be created inside the same ul node, and we want to keep the spacing uniform. */
			ul.lpx { margin: 0px; padding-left: 39px; }
			ul.lpx li { padding-top: 2px; padding-bottom: 1px; }
			img.lpxtab { height: 1em; width: 30px; border: 0px; }
			.photositealbum { font-size: 9px; }
			
			/* Support for text published by the OE. */
			div.lpxtext { font-family: Arial, Helvetica, adobe-helvetica, Arial Narrow; font-size: 13px; line-height: 16px}
			div.lpxtext p  { margin-top: 0px; margin-bottom: 0px; }
			div.lpxtext ul  { margin: 0px; padding-left: 39px; }
			div.lpxtext ul  li { padding-top: 2px; padding-bottom: 1px; }

			div.lpxcenterpageouter { text-align: center; position: absolute; top: 0px; left: 0px; width: 100% }
			div.lpxcenterpageinner { position: relative; margin: 0 auto; text-align: left; width: 810px; }
		</style>
		
		<STYLE type="text/css">
			<!--
							.navBackgroundQuickSiteMain { background-image:url('/~media/elements/LayoutClipart/../LayoutClipart/Buttons/Basic_Button_Gray.gif'); background-position: center; background-repeat:no-repeat }
							.navBackgroundSelectedQuickSiteMain { background-image:url('/~media/elements/LayoutClipart/../LayoutClipart/Buttons/Basic_Button_White.gif'); background-position: center; background-repeat:no-repeat }
						-->
		</STYLE>

		<script language="JavaScript" type="text/javascript" src="http://www.homestead.com/~media/elements/shared/DynamicDrive/SlideShow.js">
		</script>
	</head>
	<body bgcolor="#FFFFFF" link="#BA4B24" vlink="#702201" alink="#702201" onLoad="slideShowInit('slideLayer_element38', 'slide2Layer_element38', 'mouseLayer_element38', imageselement38);" background="http://media.vyperlogix.com/felinephandango/static/bg.gif" id="element1" onUnload="" scroll="auto">
		<noscript>
			<img height="40" width="373" border="0" alt="" src="http://www.homestead.com/~media/elements/shared/javascript_disabled.gif">
		</noscript>
		<div class="lpxcenterpageouter"><div class="lpxcenterpageinner"><div id="element2" style="position: absolute; top: 10px; left: 0px; width: 810px; height: 602px; z-index: 0;"><img height="602" width="810" alt="" src="http://media.vyperlogix.com/felinephandango/static/body_bg.jpg"></div><div id="element5" style="position: absolute; top: 116px; left: 5px; width: 131px; height: 130px; z-index: 1;"><img height="130" width="131" alt="" src="http://media.vyperlogix.com/felinephandango/static/June_2009_607x600.jpg"></div><div id="element15" style="position: absolute; top: 547px; left: 383px; width: 39px; height: 39px; z-index: 2;"><img height="39" width="39" alt="" src="http://media.vyperlogix.com/felinephandango/static/icon.gif"></div><div id="element21" style="position: absolute; top: 249px; left: 1px; width: 799px; height: 1px; z-index: 3;"><table cellspacing="0" border="0" cellpadding="0"><tr><td height="1" bgcolor="#BA4B24" width="799"><img height="1" width="799" alt="" src="http://www.homestead.com/~site/Scripts_Shapes/shapes.dll?CMD=GetRectangleGif&r=186&g=75&b=36"></td></tr></table></div><div id="element22" style="position: absolute; top: 292px; left: 7px; width: 114px; height: 62px; z-index: 4;"><div align="left"><SCRIPT TYPE="text/javascript" SRC="http://media.vyperlogix.com/felinephandango/static/QuickSiteMain.js"></SCRIPT><noscript><font face="'Bookman Old Style', 'Times New Roman', Times, serif" style="font-weight:bold;" class="size10 BookmanOldStyle10"><a target="_self" href="/index.html">Home</a><br/><a target="_self" href="/Contact.html">Contact</a></font></noscript></div></div><div id="element24" style="position: absolute; top: 10px; left: 5px; width: 780px; height: 63px; z-index: 6;"><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size22 Helvetica22"><b>FelinePhandango.Com - Professional Cat Sitting Service</b><br></font></div><div align="left"><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10"><b>A Licensed, Insured, and Bonded Service</b><br></font></div></div><div id="element25" style="position: absolute; top: 482px; left: 265px; width: 100px; height: 100px; z-index: 7;"><img height="100" width="100" alt="" src="http://media.vyperlogix.com/felinephandango/static/Meow1.jpg"></div><div id="element26" style="position: absolute; top: 407px; left: 696px; width: 100px; height: 100px; z-index: 8;"><img height="100" width="100" alt="" src="http://media.vyperlogix.com/felinephandango/static/meow2.jpg"></div><div id="element27" style="position: absolute; top: 462px; left: 4px; width: 92px; height: 115px; z-index: 10;"><a target="_blank" href="http://www.petsitters.org/"><img height="115" width="92" border="0" alt="" src="http://media.vyperlogix.com/felinephandango/static/nappslogo.jpg"></a></div><div id="element28" style="position: absolute; top: 467px; left: 99px; width: 125px; height: 105px; z-index: 11;"><a target="_blank" href="http://www.petsit.com/"><img height="105" width="125" border="0" alt="" src="http://media.vyperlogix.com/felinephandango/static/psilogo.jpg"></a></div><div id="element31" style="position: absolute; top: 414px; left: 9px; width: 218px; height: 20px; z-index: 12;">
		  <div align="center" style="padding-top: 24px;"><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10"><b>Accredited Member of:</b></font></div></div><div id="element33" style="position: absolute; top: 264px; left: 259px; width: 428px; height: 193px; z-index: 13;"><div><font face="'Comic Sans MS', Arial, Helvetica, sans-serif" color="#000000" class="size16 ComicSansMS16"><i>Welcome!</i><br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10"><br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10">Feline Phandango proudly presents a service that provides unconditional love and care for your cats. Your cats will enjoy staying home knowing someone who cares for them is going to come over and play each day. Attention to detail has helped my business. It is your pet, I follow your instructions.<br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10"><br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10">I will provide fresh water, clean bowl, replenish food supply, clean feeding area and floor. I will also comb and brush your pet, scoop and change litter, change bedding, spend time entertaining and exercising cat. I will also provide mail, newspaper, and indoor plant watering. <br></font></div></div><div id="element34" style="position: absolute; top: 256px; left: 410px; width: 375px; height: 21px; z-index: 14;"><div align="left"><font face="'Comic Sans MS', Arial, Helvetica, sans-serif" color="#000000" class="size10 ComicSansMS10"><b>Serving Seal Beach and Long Beach, CA</b><br></font></div></div><div id="element35" style="position: absolute; top: 482px; left: 436px; width: 257px; height: 97px; z-index: 15;"><div style="height: 97px; padding: 0; border-width: 2; border-color: #CC9966; background-color: transparent;"><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10"><b> Benefits of In-Home Sitting</b><br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10"><br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10">- Less trauma for the pet<br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10">- Happier in thier own bed at home<br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10">- Easier for the owner<br></font></div><div><font face="Helvetica, Arial, sans-serif" color="#000000" class="size10 Helvetica10">- No worries interactions with other pets<br></font></div></div></div><div id="element38" style="position: absolute; top: 117px; left: 138px; width: 658px; height: 129px; z-index: 16;"><script language="javascript" type="text/javascript">
<!--//
					
					var imageselement38='<nobr><img style="vertical-align:middle;" border=0 width=172 height=129 src="http://media.vyperlogix.com/felinephandango/static/buff.jpg"><img style="vertical-align:middle;" border=0 width=172 height=129 src="http://media.vyperlogix.com/felinephandango/static/buffbuck.jpg"><img style="vertical-align:middle;" border=0 width=172 height=129 src="http://media.vyperlogix.com/felinephandango/static/Molikini.jpg"><img style="vertical-align:middle;" border=0 width=191 height=129 src="http://media.vyperlogix.com/felinephandango/static/Nov__09_800x538.jpg"><img style="vertical-align:middle;" border=0 width=96 height=129 src="http://media.vyperlogix.com/felinephandango/static/kona.jpg"><img style="vertical-align:middle;" border=0 width=184 height=129 src="http://media.vyperlogix.com/felinephandango/static/Santa_Monica.jpg"></nobr>';
					//-->

</script><div style="overflow: hidden; position: relative; width:658;height:129"><div speed="2" onMouseOver="setAttribute('speed', '0')" style="position: absolute; width:658;height:129;background-color:#cccccc" onMouseOut="setAttribute(&quot;speed&quot;, &quot;2&quot;)" id="mouseLayer_element38"><div id="slideLayer_element38" style="position: absolute; left: 0px; top:0"></div><div id="slide2Layer_element38" style="position: absolute; left: 0px; top:0"></div></div></div></div></div></div>
	</body>
</html>


'''

class MainHandler(webapp.RequestHandler):

  def get(self):
    self.response.out.write(_content)

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
