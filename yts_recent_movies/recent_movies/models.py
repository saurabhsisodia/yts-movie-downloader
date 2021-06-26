from django.db import models

# Create your models here.


class Movie(models.Model):
	name=models.CharField(max_length=500,null=True,blank=True)
	imdbRating=models.PositiveIntegerField(null=True,blank=True)
	image=models.ImageField(null=True,blank=True)
	summary=models.TextField(null=True,blank=True)

	class Meta:
		ordering=['-imdbRating']
		indexes=[
			models.Index(fields=['name']),
		]


	def __str__(self):
		return self.name or ''
		
class MovieCastAward(models.Model):
	movie=models.ForeignKey(Movie,on_delete=models.CASCADE,null=True,related_name="castaward")
	cast=models.CharField(max_length=1000)
	award=models.CharField(max_length=1000)

	def __str__(self):
		return self.cast+" "+self.award


