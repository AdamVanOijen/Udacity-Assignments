"""This module defines a class with name 'Movie'"""
class Movie ():
	"""Instances of this class contain information on a given movie"""

	def __init__(self, name, URL, Link, summary): 
		"""assigns the values of the class' arguments to their corresponding members on instantiation"""
		self.title = name
		self.poster_image_url = URL
		self.trailer_youtube_url = Link
		self.description = summary
