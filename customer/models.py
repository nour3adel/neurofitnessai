from django.db import models
from pages.models import User  

#region[Red] History

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_name = models.CharField(max_length=255)
    start_date = models.DateTimeField()  
    end_date = models.DateTimeField()    
    correct_reps = models.IntegerField()
    incorrect_reps = models.IntegerField()

    def __str__(self):
        return self.workout_name
    
    
#endregion