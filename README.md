# nct-scrapy

Clone project to a FOLDER by command:
	git clone https://github.com/tvduy97/nct-scrapy.git

Open Anaconda Prompt, move to FOLDER/nct-scrapy/nhaccuatui
Run this command to crawl data to file .csv (the file name can be changed)
	scrapy crawl lyric -o filename.csv

We have a file named file.csv is an example of data crawled, open it by notepad or sublime text to view (do not use excel)
Our problem is export our crawled data to some file that can be import to Solr 
(My solr run not corectly so I am trying to run it)
Or we can use pipeline to export Solr same like export to MySql (do not use MySQL)