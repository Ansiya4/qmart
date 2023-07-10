from django.db import models
from product.models import Product
from loginSystem.models import Account
from django.db.models import F,Sum



class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        cartItems = CartItem.objects.filter(cart=self.id).annotate(total=F('price')*F('quantity')).values()
        TotalSum = cartItems.aggregate(totalSum=Sum('total'))
        return TotalSum['totalSum']
   
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.price * self.quantity
   


