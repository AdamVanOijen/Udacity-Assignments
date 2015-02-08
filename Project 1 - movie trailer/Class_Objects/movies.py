#creating a class - defines the contents of the objects in the instance of the 'Movie' class.
class Movie ():
	#on instantiation, the members: 'title', 'poster_image_url',
	#'trailer_youtube_url' and 'description' will be assigned the values of: 'name', 'URL' and 'Link' and 'summary'
	def __init__(self, name, URL, Link, summary): 
		self.title = name
		self.poster_image_url = URL
		self.trailer_youtube_url = Link
		self.description = summary
