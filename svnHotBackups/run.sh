#!/bin/bash

if [ -f /root/bin/PYTHONPATH ]; then
	. /root/bin/PYTHONPATH
fi

pid=$(ps aux | grep svnHotBackups.py | grep -v grep | awk '{print $2}' | tail -n 1)

if [ ${#pid} == "0" ]; then
	time=$(date +%H%M%S)
	folder="_"`eval date +%m-%d-%Y`"_"$time"_"
	/root/bin/python /root/svnHotBackups/svnHotBackups.py --verbose --archive-type=gz --num-backups=2 --repo-path="/var/local/svn/repo1" --backup-dir="/var/local/svn/#svn_backups/repo1/${folder}" --carbonite-hours=24 --carbonite-files=4 --carbonite-optimize=1 --carbonite-schedule="?type1=Primary&days1=M-F&hours1=0-20&type2=Alt&days2=Sa-Su&hours2=*" >/root/svnHotBackups/logs/svnHotBackups${folder}.log 2>&1 &

	pid=$(ps aux | grep cpulimit | grep -v grep | awk '{print $2}' | tail -n 1)
	echo ${pid}
	if [ ${#pid} == "0" ]; then
		echo
	else
		kill -9 ${pid}
	fi
	pid=$(ps aux | grep cpulimit | grep -v grep | awk '{print $2}' | tail -n 1)
	echo ${pid}
	if [ ${#pid} == "0" ]; then
		echo
	else
		kill -9 ${pid}
	fi
	pid=$(ps aux | grep svnHotBackups.py | grep -v grep | awk '{print $2}' | tail -n 1)
	echo ${pid}
	if [ ${#pid} == "0" ]; then
		echo
	else
		cpulimit -p ${pid} -l 10
	fi
	p=$(which aws)
	echo ${pid}
	if [ ${#p} == "0" ]; then
		echo
	else
		cpulimit -P ${p} -l 10
	fi

	src="/var/local/svn/#svn_backups/repo1/${folder}"
	 
	IFS=$'\n'
	 
	for dir in `ls "$src/"`
	do
	  if [ -f "$src/$dir" ]; then
	    #rm -f -R $src/$dir
	    echo
	  fi
	done
	
	rmdir $src
else
	echo "Running svnHotBackups.py - Cannot run more than one instance at a time !!!"
fi

