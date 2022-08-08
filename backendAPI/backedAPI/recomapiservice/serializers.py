from rest_framework import serializers
from .models import Recom
from .models import User_intr

class RecomSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(required=False)
    bookmarkflag = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        instance.views=validated_data.get('views',instance.views)
        instance.bookmarkflag=validated_data.get('bookmarkflag',instance.bookmarkflag)
        instance.rating=validated_data.get('rating',instance.rating)
        instance.snoozed_date=validated_data.get('snoozed_date',instance.snoozed_date)
        instance.snoozeval_days=validated_data.get('snoozeval_days',instance.snoozeval_days)
        instance.snooze_priority=validated_data.get('snooze_priority',instance.snooze_priority)
        instance.quality=validated_data.get('quality',instance.quality)
        instance.save()
        return instance

    class Meta:
        model = Recom
        fields = ['keyid','rec_rank','itemtype','title','descrptn','datemod','authors','urllink','tags','bookmarkflag','views',
                  'score','rating','snoozeval_days','snoozed_date','snooze_priority','deleted_tag','repetitions',
                  'quality','previous_interval','previous_ef','scheduled_date','displaying_date','curr_status','needs_update_flag']
        extra_kwargs = {'keyid': {'required': False},'rec_rank': {'required': False},'itemtype': {'required': False},'title': {'required': False},
                        'datemod': {'required': False},'authors': {'required': False},'urllink': {'required': False},'rating':{'required': False},
                        'snoozeval_days': {'required': False},'snoozed_date': {'required': False},'snooze_priority':{'required': False},
                        'deleted_tag':{'required': False},'repetitions':{'required': False},
                       'quality':{'required': False},'previous_interval':{'required': False},
                        'previous_ef':{'required': False},'scheduled_date':{'required': False},'displaying_date':{'required': False},
                        'curr_status':{'required': False},'needs_update_flag':{'required': False}}


class User_intrSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_intr
        fields = ['keyid','interaction_type','interaction_timestamp']
