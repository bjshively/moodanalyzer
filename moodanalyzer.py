#!/usr/bin/python
import sys
import urllib2
import re

def determine_youtube_mood(youtube_video_url):
	
	print '#' * 40
	print 'YouTube Comment Mood Analyzer'
	print '#' * 40

	YOUTUBE_BASE_URL = 'https://plus.googleapis.com/u/0/_/widget/render/comments?first_party_property=YOUTUBE&href='
	video_comments_url = YOUTUBE_BASE_URL + youtube_video_url

	#Words used to determine if a comment is happy or sad
	happy_list = ['love','loved','like','liked','awesome','amazing','good','great','excellent']
	sad_list = ['hate','hated','dislike','disliked','awful','terrible','bad','painful','worst', 'wtf']

	#Running tally of people that were happy/sad about the video
	total_happy = 0
	total_sad = 0

	print "Getting comment data..."

	#Get the comment page data
	data = urllib2.urlopen(video_comments_url)

	#Extract the comments from the data
	comments = re.findall(r'<div class="Ct">([^<].*?)</div>', data.read())
	sample_size = len(comments)

	print "Analyzing..."

	#Analyze the comments
	for comment in comments:
		comment = comment.lower()
		happy_count = 0
		sad_count = 0

		#Look for each happy and sad word in the comment, and increment the happy/sad counters
		for word in happy_list:
			hits=0
			hits = re.findall(word, comment)
			happy_count += len(hits)

		for word in sad_list:
			hits=0
			hits = re.findall(word, comment)
			sad_count += len(hits)

		#Increment the total happy/sad commenter count, based on number of happy/sad terms
		if happy_count > sad_count:
			total_happy += 1
		else:
			total_sad += 1

	#Print whether more people were happy or sad, and the sample size
	print "There were %s happy comments and %s sad comments." % (total_happy, total_sad,)
	if (total_happy > total_sad):
		print("The general feelings towards this video were happy.")
	else:
		print("The general feelings towards this video were sad.")
	print "Sample size of %s comments." % (sample_size)

def main():
  input_url = sys.argv[1]

  #Error if no url provided
  if not input_url:
    print 'You need to pass in a YouTube video URL to analyze comments'
    sys.exit(1)

  determine_youtube_mood(input_url)

if __name__ == '__main__':
  main()