from django.db import models

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_send = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class BaseReservation(models.Model):
    POLICIES = (

    )
    your_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    additional_information = models.TextField(blank=True, null=True)
    date_send = models.DateTimeField(auto_now_add=True)

    we_are_allowed_to_take_pictures_of_you_and_your_guest = models.BooleanField(default=True)
    we_are_allowed_to_take_pictures_of_your_apartment = models.BooleanField(default=True)
    we_are_allowed_to_use_your_event_content_for_our_business_promotions = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.your_name
    

class FineReservation(BaseReservation):
    GUEST_NUMBER = (
        ('10', '10 or less'),
        ('20', '20 or less'),
        ('30', '30 or less'),
        ('40', '40 or less'),
        ('50', '50 or more'),
    )

    FINE_DINING = (
        ('M1', 'Menu 1'),
        ('M2', 'Menu 2'),
        ('M3', 'Menu 3'),
        ('M4', 'Menu 4'),
        ('M5', 'Menu 5'),
        ('M6', 'Menu 6'),
        ('M7', 'Menu 7'),
    )

    number_of_guest = models.CharField(max_length=2, choices=GUEST_NUMBER, default=10)
    menu_type = models.CharField(max_length=2, choices=FINE_DINING, default='M1')
