from rest_framework import serializers
from main.models import Shop,Slot


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            'shop_name',
            'gst_id',
            'start_time',
            'stop_time',
            'shop_capacity',
            'owner_name',
            'owner_phone_number',
            'shop_pincode',
            'shop_city',
            'shop_area',
            'shop_street',
            'shop_state'
        )

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        Model=Slot
        fields=(
            # 'shop.owner_name',
            'slot_start_time',
            'slot_stop_time',
            'num_entries_left'
        )

