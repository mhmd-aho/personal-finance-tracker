from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
# Create your models here.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
@receiver(post_delete,sender= Profile)
def delete_user_profile(sender,instance,**kwargs):
    if instance.user:
        instance.user.delete()
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='transactions')
    def save(self, *args, **kwargs):
        with transaction.atomic():
            profile = self.profile
            amount = self.amount
            type = self.type
            if self.pk:
                old_transaction = Transaction.objects.get(pk=self.pk)
                self.__adjust_balance(old_transaction,undo=True)
            self.__adjust_balance(self,undo=False)
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.__adjust_balance(self,undo=True)
        super().delete(*args, **kwargs)
    def __adjust_balance(self,instance,undo=False):
        is_expense = instance.type == 'expense'
        if undo:
           change = instance.amount if is_expense else -instance.amount
        else:
            change = -instance.amount if is_expense else instance.amount
        self.profile.balance = F('balance') + change
        self.profile.save(update_fields=['balance'])
        self.profile.refresh_from_db()
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='budgets')
    def __str__(self):
        return self.category.name