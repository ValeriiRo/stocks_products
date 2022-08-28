from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):

        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for el in positions:
            new_position = StockProduct(product=el['product'], quantity=el['quantity'], price=el['price'], stock=stock)
            new_position.save()

        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for el in positions:
            StockProduct.objects.update_or_create(
                product=el['product'], stock=stock,
                defaults={'product': el['product'], 'quantity': el['quantity'], 'price': el['price'], 'stock': stock}
            )

        return stock


