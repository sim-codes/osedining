from django.db import models

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_send = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class BaseRequest(models.Model):
    your_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    date_send = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Hire(BaseRequest):

    EVENT_TYPE = (
        ('HOME', 'Home'),
        ('WEDDING', 'Wedding'),
        ('BIRTHDAY', 'Birthday'),
        ('ANNIVERSARY', 'Anniversary'),
        ('OTHERS', 'Others'),
    )

    event_type = models.CharField(max_length=15, choices=EVENT_TYPE, default='HOME')
    additional_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Hire request by {self.your_name}'

class CustomDining(BaseRequest):
    menu_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Custom menu request by {self.your_name}'

class BaseDining(models.Model):
    POLICIES = (

    )
    your_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    additional_information = models.TextField(blank=True, null=True)
    date_send = models.DateTimeField(auto_now_add=True)

    we_are_allowed_to_take_pictures_of_you_and_your_guest = models.BooleanField(default=True)
    we_are_allowed_to_take_pictures_of_your_apartment = models.BooleanField(default=True)
    we_are_allowed_to_use_your_event_content_for_our_business_promotions = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.your_name
    

class FineDining(BaseDining):
    GUEST_NUMBER = (
        ('10', '10 or less'),
        ('20', '20 or less'),
        ('30', '30 or less'),
        ('40', '40 or less'),
        ('50', '50 or more'),
    )

    MENUS = (
        ('M1', 'Menu 1'),
        ('M2', 'Menu 2'),
        ('M3', 'Menu 3'),
        ('M4', 'Menu 4'),
        ('M5', 'Menu 5'),
        ('M6', 'Menu 6'),
        ('M7', 'Menu 7'),
    )

    # number_of_guest = models.CharField(max_length=2, choices=GUEST_NUMBER, default=10)
    number_of_guest = models.IntegerField(default=10)
    menu_type = models.CharField(max_length=2, choices=MENUS, default='M1')


class CasualDining(BaseDining):
    BREAD = (
        ('F', 'Focaccia'),
        ('C', 'Ciabatta'),
        ('S', 'Sourdough'),
        ('H', 'Herbal bun'),
        ('G', 'Garlic bread'),
        ('CH', 'Challah'),
    )

    GUEST_NUMBER = (
        ('8', '8 or less'),
        ('15', '15 or less'),
        ('20', '20 or less'),
        ('30', '30 or less'),
        ('40', '40 or more'),
    )

    MENUS = (
        ('M1', 'Menu 1'),
        ('M2', 'Menu 2')
    )

    SIDES = (
        ('BMP', 'Buttering mashed potatoes'),
        ('CGP', 'Cheesy garlic roasted butter potatoes'),
        ('PF', 'Potatoes fondant'),
        ('CBP', 'Creamy baby potatoes'),
        ('SPR', 'OSE special fried rice'),
        ('SSF', 'Spaghetti stir fry'),
        ('CJ', 'Coriander jasmine'),
        ('SAJ', 'Smoked asun jollof '),

    )

    VEGETABLES = (
        ('RC', 'Roasted carrot'),
        ('BT', 'Broccoli tempura'),
        ('SM', 'Sautéed mushroom'),
        ('PO', 'Pickled onion'),
        ('MP', 'Mixed bell pepper'),
        ('SS', 'Sautéed spinach'),
        ('AB', 'Assorted bread'),
    )

    number_of_guest = models.CharField(max_length=2, choices=GUEST_NUMBER, default='8')
    menu_type = models.CharField(max_length=2, choices=MENUS, default='M1')
    bread = models.CharField(max_length=2, choices=BREAD, default='F')
    side_one = models.CharField(max_length=3, choices=SIDES, default='BMP')
    side_two = models.CharField(max_length=3, choices=SIDES, default='CGP')

    vegetable_one = models.CharField(max_length=2, choices=VEGETABLES, default='RC')
    vegetable_two = models.CharField(max_length=2, choices=VEGETABLES, default='BT')
