from rest_framework import serializers
from restaurants.models import Restaurant
from .models import Menu, MenuItem, ExcelFile
from django.core.files.storage import default_storage
from .mixins import read_excel_file
from django.core.exceptions import ObjectDoesNotExist


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    excel_file = serializers.FileField(write_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ('restaurant', 'created_at', 'updated_at',)

    def create(self, validated_data):
        excel_file = validated_data.pop('excel_file')
        file = ExcelFile(file=excel_file)
        validated_data['excel_file'] = file
        file.save()

        try:
            restaurant = Restaurant.objects.get(owner__user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("The restaurant associated with the current user does not exist.")

        validated_data['restaurant'] = restaurant
        menu = Menu(**validated_data)
        menu.save()
        self.save_menu_items(menu, excel_file)
        return menu

    def save_menu_items(self, menu, excel_file):
        # Read data from the uploaded Excel file
        file_path = default_storage.save('temp_excel_file.xlsx', excel_file)
        excel_data = read_excel_file(file_path)

        # Save data to the MenuItem model
        for item_data in excel_data:
            MenuItem.objects.create(
                name=item_data['name'],
                description=item_data['description'],
                price=item_data['price'],
                image=item_data['image'],
                menu=menu,
                is_active=item_data['is_active'],
            )

        # Delete the uploaded file from the storage
        default_storage.delete(file_path)
