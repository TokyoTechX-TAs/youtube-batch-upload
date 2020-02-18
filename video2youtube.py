#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xlrd
import xlwt
import re
import subprocess
from datetime import datetime



"""
	sheet-> Upload videos
"""
UPLOADSHEET = "upload_list"
FILEINDEX = 0
FILEDIR = 1
FILENAME = 2
TITLE = 3
DESCRIPTION = 4
KEYWORD = 5
PRIVACYSTATUS = 6

"""
	sheet-> Upload caption
"""

CAPTIONSHEET = "caption_list"
CAPTIONINDEX = 0
CAPTIONFILEDIR = 1
CAPTIONFILENAME = 2
CAPTIONLANG = 3
CAPTIONNAME = 4
CAPTIONVIDEOID = 5


"""
	sheet-> Upload thumbnail
"""

THUMBNAILSHEET = "thumbnail_list"
THUMBNAILINDEX = 0
THUMBNAILFILEDIR = 1
THUMBNAILFILENAME = 2
THUMBNAILVIDEOID = 3



EXCELFILE = "course_info.xlsm"
wb = xlrd.open_workbook(EXCELFILE)

CAPTIONEXTENSION = {'.srt'}



def read_xlm(task_flag):
	
	all_data = []
	if task_flag == '1':
		print('---------------------------------Import list of video info from excel file----------------------------\n\n')

		sheetstruc = wb.sheet_by_name(UPLOADSHEET)
		for row in range(1, sheetstruc.nrows):

			idx_ = sheetstruc.cell_value(row,FILEINDEX)
			filedir_ = sheetstruc.cell_value(row,FILEDIR)
			filename_ = sheetstruc.cell_value(row,FILENAME)
			title_ = sheetstruc.cell_value(row,TITLE)
			desc_ = sheetstruc.cell_value(row,DESCRIPTION)
			keyw_ = sheetstruc.cell_value(row,KEYWORD)
			priv_ = sheetstruc.cell_value(row,PRIVACYSTATUS)
			
			all_data.append({'row':row,
				'id': idx_,
				'file_dir': filedir_,
				'filename': filename_,
				'title': title_,
				'description': desc_,
				'keyword': keyw_,
				'privacy_status': priv_})

	elif task_flag == '2':
		print('---------------------------------Import list of transcipt info from excel file----------------------------\n\n')
	
		sheetstruc = wb.sheet_by_name(CAPTIONSHEET)
		for row in range(1, sheetstruc.nrows):

			idx_ = sheetstruc.cell_value(row,CAPTIONINDEX)
			filedir_ = sheetstruc.cell_value(row,CAPTIONFILEDIR)
			filename_ = sheetstruc.cell_value(row,CAPTIONFILENAME)
			lang_ = sheetstruc.cell_value(row,CAPTIONLANG)
			name_ = sheetstruc.cell_value(row,CAPTIONNAME)
			videoid_ = sheetstruc.cell_value(row,CAPTIONVIDEOID)
			videoid_ = re.sub(r'\S+be/', '', videoid_)
			videoid_ = re.sub(' ','',videoid_)
			
			all_data.append({'row':row,
				'id': idx_,
				'file_dir': filedir_,
				'filename': filename_,
				'lang': lang_,
				'name': name_,
				'videoid': videoid_})

	elif task_flag == '3':
		print('---------------------------------Import list of thumbnails info from excel file----------------------------\n\n')
	
		sheetstruc = wb.sheet_by_name(THUMBNAILSHEET)
		for row in range(1, sheetstruc.nrows):

			idx_ = sheetstruc.cell_value(row,THUMBNAILINDEX)
			filedir_ = sheetstruc.cell_value(row,THUMBNAILFILEDIR)
			filename_ = sheetstruc.cell_value(row,THUMBNAILFILENAME)
			videoid_ = sheetstruc.cell_value(row,THUMBNAILVIDEOID)
			videoid_ = re.sub(r'\S+be/', '', videoid_)
			
			all_data.append({'row':row,
				'id': idx_,
				'file_dir': filedir_,
				'filename': filename_,
				'videoid': videoid_})
	else:
		print("wrong task flag")
		exit()

		
	

	return(all_data)


def upload_video(videos):
	cur_path = os. getcwd()
	for video in videos:
		filename_template = os.path.join(video['file_dir'],video['filename'])
		#upload_command_template = 'cd video_source & python upload_video.py --file='+ filename_template  
		#upload_command_template = 'python upload_video.py --file='+ filename_template  
		arg_list = ['--file',filename_template]
		if video['title'] != "":
			arg_list += ['--title',str((video['title'])) ]
			#upload_command_template = upload_command_template + " --title=" + str((video['title'])) 
		if video['description'] != "":
			#upload_command_template = upload_command_template + " --description=" +str(video['description']) 
			arg_list += ['--description',str(video['description']) ]
		if video['keyword'] != "":		
			#upload_command_template = upload_command_template + " --keywords=" +str(video['keyword']) 
			arg_list += ['--keywords',str(video['keyword'])]
		if video['privacy_status'] != "":
			#upload_command_template = upload_command_template + " --privacyStatus=" +str(video['privacy_status'])
			arg_list += ['--privacyStatus',str(video['privacy_status'])]
		#print(type(video["keyword"]))
		print("---------------------------------start uploading " + video['filename'] + "---------------------------------")
		upload_command_template = ['python','upload_video.py'] + arg_list
		print(upload_command_template)
		os.chdir(os.path.join(cur_path,'video_source'))
		subprocess.call(upload_command_template)
		os.chdir(cur_path)
		
		#os.system(upload_command_template)
		print('-------------------------------------------------------------------------------------------------------\n')



def upload_transcript(transcripts):
	cur_path = os. getcwd()
	
	for transcript in transcripts:
		filename_template_old = os.path.join(transcript['file_dir'],transcript['filename'])



		if transcript['filename'] == "":
			print ('no filename specified for transcript at excel id: ' + str(transcript['id']))
			continue
		script_path_old = os.path.join('video_source',filename_template_old)
		script_path = os.path.join('video_source',filename_template_old)
		for e_ext in CAPTIONEXTENSION:

			if e_ext in script_path and os.path.isfile(script_path):
				bin_filename = transcript['filename'].replace(e_ext, '.bin')
				newfile = script_path.replace(e_ext, '.bin')
				os.rename(script_path, newfile)
				filename_template = os.path.join(transcript['file_dir'],bin_filename)


		#upload_command_template = 'cd video_source & python upload_caption.py --videoid='+ str(transcript['videoid']) + ' --file='+filename_template
		arg_list = ['--videoid',str(transcript['videoid']),'--file',filename_template]
		if transcript['name'] != "":
			#upload_command_template = upload_command_template + " --name=" + str((transcript['name'])) 
			arg_list += ['--name',str((transcript['name'])) ]
		if transcript['lang'] != "":
			#upload_command_template = upload_command_template + " --language=" +str(transcript['lang']) 
			arg_list+=['--language', str(transcript['lang'])]
		
		#upload_command_template = upload_command_template + ' --action=upload'
		print("---------------------------------start uploading " + transcript['filename'] + "---------------------------------")
		upload_command_template = ['python','upload_caption.py'] + arg_list
		print(upload_command_template)
		os.chdir(os.path.join(cur_path,'video_source'))
		subprocess.call(upload_command_template)
		os.chdir(cur_path)
		#os.system(upload_command_template)
		print('-------------------------------------------------------------------------------------------------------\n')
		os.rename(newfile,script_path_old)



def upload_thumbnail(thumbnails):
	cur_path = os. getcwd()
	for thumbnail in thumbnails:
		filename_template = os.path.join(thumbnail['file_dir'],thumbnail['filename'])
		upload_command_template = ['python','upload_thumbnails.py','--file',filename_template,'--video-id',str(thumbnail['videoid']) ] 
		#'cd video_source & python upload_thumbnails.py --file '+ filename_template + ' --video-id=' + str(thumbnail['videoid']) 
		os.chdir(os.path.join(cur_path,'video_source'))
		print(str(thumbnail['videoid']))
		print("---------------------------------start uploading thumbnail:  " + thumbnail['filename'] + "---------------------------------")
		print(upload_command_template)
		subprocess.call(upload_command_template)
		#os.system(upload_command_template)
		os.chdir(cur_path)
		print('-------------------------------------------------------------------------------------------------------\n')




def output_video_list(title,youtube_id):

	output_name = 'uploaded_video_link.txt' 
	file = open(output_name,'a')
	file.write( datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' , '+title+' , '+'https://youtu.be/'+youtube_id+'\n')
	file.close()


#python captions.py --videoid='<video_id>' --name='<name>' --file='<file>' --language='<language>' --action='action'

def main():
	flag = 0
	global file
	
	while(flag==0):
		command = input("enter [1-3]\n1.Upload video\n2.Upload Caption\n3.Upload thumbnail\n")
		if command == '1':
			print ('the Upload video task is chosen')
			all_videos = read_xlm(command)
			upload_video(all_videos)
			flag = 1
		elif command == '2':
			print ('the Upload Caption task is chosen')
			all_transcripts = read_xlm(command)
			upload_transcript(all_transcripts)
			flag = 1
		elif command == '3':
			print ('the Upload thumbnail task is chosen')
			all_thumbnails = read_xlm(command)
			upload_thumbnail(all_thumbnails)
			flag = 1
		else:
			print ('wrong command, try again!!!!')




	




if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		logging.warn("\n\nCTRL-C detected, shutting down....")
		sys.exit(ExitCode.OK)



