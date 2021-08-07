from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=300)
    date_time = models.DateTimeField()
    description = models.TextField()
    image = models.ImageField(upload_to='static/images/events/', null=True)
    event_link = models.URLField(null=True)

    @property
    def image_url(self):
        try:
            url = self.image.url
        except Exception:
            url = '../static/images/shop/no-image-available.png'
        return url




