#!/bin/bash

pub_file="base_info_pub.json"
debug_file="base_info_debug.json"
base_file="base_info.json"

if [ ! -e "$pub_file" ]
then
	echo "Already change to publishing mode"
else 
	mv "$base_file" "$debug_file"
	mv "$pub_file" "$base_file"
	echo "success to change to publishing mode"
	ls
fi

