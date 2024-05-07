class Announce(models.Model):
    image = models.ImageField(upload_to="announce/%y/%m/%d")
    title = models.CharField(max_length=100)
    launching_date = models.DateField()
    content = models.TextField()
    add_date = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
