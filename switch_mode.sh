#!/bin/bash

pub_file="json/base_info_pub.json"
debug_file="json/base_info_debug.json"
base_file="json/base_info.json"

if [ ! -e "$pub_file" ] && [ -e "$debug_file" ];
then 
	echo "It's in publishing mode."
	echo "Changing to debug mode."
	mv "$base_file" "$pub_file"
	mv "$debug_file" "$base_file"
	echo "succcess to change to debug mode."
	cat $base_file
elif [ -e "$pub_file" ] && [ ! -e "$debug_file" ];
then
	echo "It's in debug mode."
	echo "Changing to publishing mode."
	mv "$base_file" "$debug_file"
	mv "$pub_file" "$base_file"
	echo "Success to change to publishing mode."
	cat $base_file
fi