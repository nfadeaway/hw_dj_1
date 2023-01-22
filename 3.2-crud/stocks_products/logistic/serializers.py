from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


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

        for position in positions:
            stock_product_dict = dict(position)
            StockProduct.objects.create(stock=stock, product=stock_product_dict['product'],
                                        quantity=stock_product_dict['quantity'], price=stock_product_dict['price'])

        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position in positions:
            stock_product_dict = dict(position)
            values_for_update = {'stock': instance,
                                 'product': stock_product_dict['product'],
                                 'quantity': stock_product_dict['quantity'],
                                 'price': stock_product_dict['price']
                                 }
            StockProduct.objects.filter(stock=instance, product=stock_product_dict['product']).update_or_create(defaults=values_for_update)

        return stock
