from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    """
    Address model.
    """

    raw_address = models.CharField(max_length=300, default="address")
    address = models.CharField(max_length=300)
    creation_date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def query_address(self):
        """
        Used for google maps api
        """
        return self.address.replace(" ", "+")
