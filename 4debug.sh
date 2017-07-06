#!/bin/bash

pub_file="base_info_pub.json"
debug_file="base_info_debug.json"
base_file="base_info.json"

if [ ! -e "$debug_file" ]
then
	echo "Already change to debug mode"
else 
	mv "$base_file" "$pub_file"
	mv "$debug_file" "$base_file"
	echo "succcess to change to debug mode"
	ls
fi

