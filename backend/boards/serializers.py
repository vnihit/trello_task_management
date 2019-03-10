from rest_framework import serializers
from .models import Boards, Lists, Cards


class BoardsSerializer(serializers.ModelSerializer):
    labels = serializers.ListField()

    class Meta:
        model = Boards
        fields = "__all__"
    

class ListSerializer(serializers.ModelSerializer):
    card_order = serializers.ListField()
    class Meta:
        model = Lists
        fields = "__all__"


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = "__all__"