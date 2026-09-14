from rest_framework import serializers
from .models import MyProduct, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProduct
        fields = ['id', 'title', 'price', 'dis_price', 'description', 'category', 'image']

class OrderSerializer(serializers.ModelSerializer):
    # Expect raw cart items array from client: [{"product_id": 1, "quantity": 2}]
    cart_items = serializers.JSONField(write_only=True)  # Accept cart items as JSON input
    
    class Meta:
        model = Order
        fields = ['id', 'name', 'phone_num','email', 'address', 'city', 'state', 'zip_code', 'cart_items'
                  ,'total_price', 'created_at','status','items']
        # Protect internal & generated fields from client manipulation
        read_only_fields = ['id', 'total_price', 'items', 'status', 'created_at']
    
    # FIELD-LEVEL VALIDATION FOR cart_items
    def validate_cart_items(self, value):
        """
        'value' contains whatever data was passed to 'cart_items'.
        """
        if not isinstance(value, list) or len(value) == 0:
            raise serializers.ValidationError("cart_items must be a non-empty list of items.")
        
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Each item in cart_items must be an object/dict.")
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must contain 'product_id' and 'quantity'.")
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
                
            # Verify product exists in database before proceeding to create()
            if not MyProduct.objects.filter(id=item['product_id']).exists():
                raise serializers.ValidationError(f"Product with ID {item['product_id']} does not exist.")

        return value  # Always return the validated value
    
    def create(self, validated_data):
        cart_items = validated_data.pop('cart_items')
        calculated_total = 0
        formatted_items = []

        # Backend securely fetches true product prices from the database
        for item in cart_items:
            product = MyProduct.objects.get(id=item['product_id'])
            # Use discount price if available, otherwise regular price
            price = product.dis_price if product.dis_price else product.price
            
            item_total = price * item['quantity']
            calculated_total += item_total

            formatted_items.append({
                'product_id': product.id,
                'title': product.title,
                'price': float(price),
                'quantity': item['quantity'],
                'subtotal': float(item_total)
            })

        # Inject auto-calculated fields before saving to database
        validated_data['total_price'] = calculated_total
        validated_data['items'] = formatted_items
        
        return super().create(validated_data)