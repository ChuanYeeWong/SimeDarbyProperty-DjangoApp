from rest_framework import serializers
from billings.models import Invoice,BillType,Payment
from djmoney.money import Money
import datetime
class BillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillType
        fields=(
            'id',
            'name',
        ) 
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields=(
            'amount',
            'payment_date',
            'status',
            'invoices',
            'remark',
            'receipt',
        )
class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields=(
            'amount',
            'remark',
            'receipt',
            'invoices',
        )
    def get_current_user(self):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user
        return None
    def create(self,validated_data):
        payment = Payment.objects.create(
            amount = validated_data['amount'],
            payment_date = datetime.datetime.now().date(),
            remark = validated_data['remark'],
            receipt = validated_data['receipt'],
            invoices = validated_data['invoices'],
        )
        return payment
class InvoiceSerializer(serializers.ModelSerializer):
    bill_type = BillTypeSerializer()
    payment_set = PaymentSerializer(many=True)
    paid_amount =serializers.SerializerMethodField()  
    def get_paid_amount(self, obj):
        res = Payment.objects.filter(invoices=obj.id,status='S')
        total = Money(0,'MYR')
        for p in res:
            total +=p.amount
        return "{0:.2f}".format(total.amount)
    class Meta:
        model = Invoice
        fields=(
            'id',
            'name',
            'status',
            'bill_type',
            'amount',
            'remainder',
            'bill_date',
            'payment_set',
            'paid_amount',
        )