// Copyright RealTracker, 10-NOV-2006, path-version
function cv(s){var os,oe,cc,r,i;cc=document.cookie;r='';i=cc.indexOf(s);if(i>-1){
os=cc.indexOf('=',i)+1;oe=cc.indexOf(';',i);if(oe<0)oe=cc.length;r=cc.substring(os,oe)};return r}
function wc(n,v,t){document.cookie=n+'='+v+'; path=/; expires='+t.toGMTString()+';'}
function fdy(n){return (n>200?n:1900+n)}
function td(n){s=''+n;if(s.length==1)s='0'+s;return s}
function f(s){if(navigator.userAgent.indexOf('MSIE 3')<0){i=new Image(1,1);i.src=s}else f2(s)}

var spd=(new Date()).valueOf();window.onload2='';

function realtracker(){t=new Date();spd=t.valueOf()-spd
t.setTime (t.getTime()+900000);wc('RT_speed',spd,t);wc('RT_page0',(id+0),t);wc('RT_pagen',pp,t);
if(window.onload2)if(window.onload2!='')window.onload2();}

o=0;
p=navigator.plugins;
l='Shockwave Flash';
if(p)if(p[l+" 2.0"] || p[l])o=1;
for(a=7;a>1;a--){
 l=(a<3)?'':'.'+a
 if(eval('try{new ActiveXObject("ShockwaveFlash.ShockwaveFlash'+l+'")}catch(e){}'))o=1;
};
res+='&f='+o

var ag=navigator.userAgent;
res+='&l='+ag.length;
if(ag.indexOf('MSIE 3')<0){t=new Date()
res+='&tt='+td(t.getMonth()+1)+'%2F'+td(t.getDate())+'%2F'+fdy(t.getYear())+'+'+td(t.getHours())+'%3A'+td(t.getMinutes())+'%3A'+td(t.getSeconds())
t.setTime (t.getTime()+900000)
c3='RT_id';rt=cv(c3);if(rt=='')rt=parseInt(2000000*Math.random());wc(c3,rt,t)
c='RT_page';c2=c+'n';c+=0;r1=cv('RT_speed');r2=cv(c2);if(r2=='')r2='-';r=cv(c);if(r=='')r=0;wc(c,0,t);wc(c2,'-',t)
res+='&b='+rt+'&p='+r+'&p3='+r2+'&spd='+r1+'&ck='+(cv(c3)!=''?1:0)+'&j='+(navigator.javaEnabled()?1:0)
rd=Math.round(Math.random()*1000000);res+='&d='+rd;if(navigator.appVersion.charAt(0)>3){
res+='&h='+screen.height+'&w='+screen.width+'&c='+(screen.pixelDepth?screen.pixelDepth:screen.colorDepth)}
var rf=document.referrer;if(ag.indexOf('MSIE 5')>0||ag.indexOf('MSIE 6')>0){
var pr='';var cl=window.location.href;

pr=eval("try{parent.document.referrer}catch(e){}")
if(pr!=''){var at=cl.indexOf('/',8);if(at>=0)cl=cl.substring(0,at+1)
if(rf.indexOf(cl)==0||rf=='')rf=pr}}
res+='&ref='+escape(rf)

if(ag.indexOf('MSIE 4')<0||ag.indexOf('Mac_P')<0){
if(typeof window.onload!='undefined' && window.onload!='') window.onload2=window.onload;
window.onload=realtracker
}}

