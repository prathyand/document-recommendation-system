from django.db import models

# Create your models here.
class Recom(models.Model):
    keyid = models.CharField(primary_key=True, max_length=255)
    rec_rank = models.IntegerField(null=False)
    itemtype = models.CharField(db_column='itemType', max_length=255)  # Field name made lowercase.
    title = models.CharField(max_length=255)
    descrptn = models.CharField(max_length=5000, blank=True, null=True)
    datemod = models.DateTimeField(db_column='dateMod')  # Field name made lowercase.
    authors = models.CharField(db_column='authors',max_length=5000)
    urllink = models.CharField(max_length=2000)
    tags = models.CharField(max_length=1000, blank=True, null=True)
    bookmarkflag = models.BooleanField(blank=False, null=False)
    views = models.IntegerField(blank=False, null=False)
    score = models.FloatField(blank=True, null=True)
    rating = models.IntegerField(blank=False, null=False)
    snoozeval_days =  models.IntegerField(blank=False, null=False)
    snoozed_date = models.DateTimeField(db_column='snoozed_date')
    snooze_priority = models.IntegerField(blank=False, null=False)
    deleted_tag = models.BooleanField(blank=False, null=False)
    repetitions = models.IntegerField(blank=False, null=False)
    quality=models.IntegerField(blank=False, null=False)
    previous_interval=models.IntegerField(blank=False, null=False)
    previous_ef=models.DecimalField(max_digits = 8,decimal_places = 4)
    scheduled_date=models.DateField(db_column='scheduled_date')
    displaying_date=models.DateField(db_column='displaying_date')
    curr_status=models.TextField()
    needs_update_flag=models.BooleanField(blank=False, null=False)


    class Meta:
        managed = False
        db_table = 'recom'

class User_intr(models.Model):
    # interactionid = models.IntegerField(blank=False, null=False,db_column='interactionID')
    keyid = models.CharField(max_length=255,db_column='keyid')
    interaction_type = models.TextField(db_column='interaction_type')
    interaction_timestamp = models.DateTimeField(db_column='interaction_timestamp')

    class Meta:
        managed = False
        db_table = 'user_intr'