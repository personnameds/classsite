from django.db import models
from django.contrib.auth.models import User
from classlists.models import School_Staff

class Schoolpage(models.Model):
    message=models.TextField()
    date=models.DateField(blank=True, null=True)
    entered_by=models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name='School Message'
        verbose_name_plural='School Messages'
        ordering=['-date']

    def entered_by_display(self):
    	if School_Staff.objects.filter(user=self.entered_by).exists():
    		return self.entered_by.school_staff.teacher_name
    	else:
    		return self.entered_by.first_name
    entered_by_display.short_description='Entered By'
