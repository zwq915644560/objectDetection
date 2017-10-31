
# coding: utf-8

import cv2
import os
import sys
from optparse import OptionParser 

# 解析标志参数
def flagParse():
	parser = OptionParser(usage="%prog [options]")

	parser.add_option('-i', '--input_dir', action='store', type='string', dest='input_dir',	help='the raw images dir, which has some subdirs named by its images\' class.')
	parser.add_option('-o','--output_dir', action='store', type='string', dest='output_dir', default='_images_', help='the dir stores renamed images.')

	(options,args)=parser.parse_args() 
	if options.input_dir==None:
		print ("you have to specify your images dir. you should try to see the script's usage.")
		sys.exit()
	return options.input_dir, options.output_dir


(input_dir, output_dir)=flagParse()
# 获得输入目录和输出目录的绝对路径
input_path=os.path.realpath(input_dir)
output_path=os.path.realpath(output_dir)
os.makedirs(output_path)

subdir_names=os.listdir(input_path)
for dir_name in subdir_names:
    class_name=dir_name
    subdir=os.path.join(input_path,dir_name)
    files=os.listdir(subdir)
    
    c=1
    for file_name in files:
        file=os.path.join(subdir, file_name)
	
        new_name=class_name+'_'+str(c)+'.jpg'
        new_name=os.path.join(output_path, new_name)
        os.rename(file, new_name)
        c+=1
print ('done..')







