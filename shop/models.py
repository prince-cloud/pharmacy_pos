from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    available_quantity = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Product: {self.name[:10]}>'

class Supply(models.Model):
    product = models.ForeignKey(Product, related_name="supplies", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    
    def __repr__(self):
        return f'<Supply: {self.product.name} {self.quantity}>'
    
    def save(self, *args, **kwargs):
        self.product.available_quantity = sum([supply.quantity for supply in self.product.supplies.all()]) + sum([purchase.quantity for purchase in self.product.purchases.all()])
        self.product.save()
        super(Supply, self).save(*args, **kwargs)


class Purchase(models.Model):
    customer = models.CharField(max_length=120, blank=True, null=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'Purchase by {self.customer}'
    
    def __repr__(self):
        return f'<Purchase: GH{self.total_amount} by {self.customer}>'

class ItemPurchase(models.Model):
    product = models.ForeignKey(Product, related_name="purchases", on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, related_name="item_purchases", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
        
    
    def __str__(self):
        return f'Purchase of {self.quantity} {self.product.name}'
    
    def __repr__(self):
        return f'<ItemPurchase: {self.product.name} {self.quantity}>'
    
    def save(self, *args, **kwargs):
        
        super(ItemPurchase, self).save(*args, **kwargs)