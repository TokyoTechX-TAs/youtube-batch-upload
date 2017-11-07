

# youtube-batch-upload
This tool will do a batch video, subtitle, and thumbnail upload to any YouTube channel including adding information such as description, and title automatically. In short, it read all materials' information from macro-excel and upload them accordingly. The tool will return a set of video URLs which will be used as an input for creating video content of edx.org online course instance

Please see the pptx of pdf file for further instructions


# This tool consists of 3 parts

1) a Python script which was developed based on YouTube data API provided by Google. So far, it has 3 functions, uploading videos, subtitles, and Thumbnails.
2) an macro-excel file where information about video files (ex. mp4, wmv, etc.), subtitle fils(ex. srt, vtt,etc.), and thumbnail(ex. png, jpg) are contained according to the format prepared.
3) a credential file of your YouTube account. To upload videos with this tool, however, it needs the credential file for authorization. Click [here](https://developers.google.com/youtube/registering_an_application
) for more detail of how to obtain the credential

# dependencies
- xlrd, xlwt, http.client, httplib2
- [Google API Client Libraries](https://developers.google.com/api-client-library/python/start/installation)

# test environment
Python 3 run on Windows 10 





