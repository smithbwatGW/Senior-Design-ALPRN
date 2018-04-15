#!/bin/bash
CONTENT=`ls *.{JPG,jpg,gif,png}`
OUTPUT="Output-$(date +"%m-%d-%Y--%T").txt"
echo $OUTPUT 1>$OUTPUT
for b in $CONTENT ;
do
	echo $b
	ALPROUT=`alpr -n 3 $b`
	printf "$b $ALPROUT" 1>>$OUTPUT
	printf "\n" 1>>$OUTPUT
done
