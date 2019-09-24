from django.db import models

class BlogProfileManager(models.Manager):
    
    def create_profile(self, first_name, last_name, sex, country, date_birth, **kwargs):
        profile = self.model(
            first_name=first_name, 
            last_name=last_name, 
            sex=sex,
            country=country,
            date_birth=date_birth,
            **kwargs
        )
        profile.save()
        return profile