from rest_framework import routers, serializers
from process_file.models import MiscData


class MiscDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiscData
        fields = ('id', 'parent_id', 'props', 'created_at', 'updated_at')