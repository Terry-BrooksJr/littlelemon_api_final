from django.db import models
from django.contrib.auth.models import User, Group


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=200, db_index=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(db_index=True)
    Category = models.ForiegnKey(Category, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "menu item"
        verbose_name_plural = "menu items"

    def __str__(self):
        return f"{self.title} ({self.category})"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    items = models.ManyToManyField(MenuItem, through="CartItem")
    quantity = models.SmallIntergetField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "cart"
        verbose_name_plural = "carts"

    def __str__(self):
        return f"{self.user.username}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.SmallIntergetField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "cart item"
        verbose_name_plural = "cart items"

    def __str__(self):
        return f"{self.menu_item.title} ({self.cart.user.username})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True
    )
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


class OrderTime(models.Model):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntergetField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("order", "menuitem")
