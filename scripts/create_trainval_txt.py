#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys

name_to_classID={'Cake':1,
		'Coffee':2,
		'GreenTea':3,
		'LemonTea':4,
		'Milk':5,
		'Soymilk':6}

def create_records():
	dataSet_root=os.path.realpath('.')
	dirs=os.listdir(dataSet_root)
	if 'images' not in dirs:
		print ('no images dir')
		sys.exit()
	images_dir=os.path.join(dataSet_root, 'images')
	files=os.listdir(images_dir)

	fp=open('trainval.txt', 'w')
	for file_name in files:
		name, _= os.path.splitext(file_name)
		classID=name_to_classID[name.split('_')[0]]
		fp.write(name+' '+str(classID)+'\n')
	
	fp.close()

create_records()
