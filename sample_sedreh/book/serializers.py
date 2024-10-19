from rest_framework import serializers
from .models import Category, Book


class CategorySerializer(serializers.ModelSerializer):
    child_categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "is_sub", "sub_category", "child_categories"]

    def get_child_categories(self, obj):

        if obj.is_sub:
            result = obj.scategory.all()
            return CategorySerializer(instance=result, many=True).data
        else:
            return None


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"
