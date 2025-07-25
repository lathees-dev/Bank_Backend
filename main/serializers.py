from rest_framework import serializers
from .models import Customer, Loan, Payment
from rest_framework.exceptions import NotFound


# Basic serializer for Customer model
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


# Basic serializer for Loan model
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


# Serializer for creating a new payment record linked to a loan
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["amount", "payment_type", "payment_date"]

    def create(self, validated_data):
        # Context-based loan injection (loan passed from view)
        loan = self.context["loan"]
        return Payment.objects.create(loan_id=loan, **validated_data)


# Serializer for displaying a transaction in a simplified format
class TransactionSerializer(serializers.ModelSerializer):
    transaction_id = serializers.UUIDField(source="payment_id", read_only=True)
    date = serializers.DateTimeField(source="payment_date")
    type = serializers.CharField(source="payment_type")

    class Meta:
        model = Payment
        fields = ["transaction_id", "date", "amount", "type"]


# Serializer for creating a loan with derived financial calculations
class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    loan_period_years = serializers.IntegerField()
    interest_rate_yearly = serializers.DecimalField(max_digits=5, decimal_places=2)

    def create(self, validated_data):
        # Fetch customer or raise 404 if not found
        customer_id = validated_data.get("customer_id")
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            raise NotFound("Customer with the given ID does not exist.")

        # Extract input values
        P = validated_data["loan_amount"]
        N = validated_data["loan_period_years"]
        R = validated_data["interest_rate_yearly"]

        # Simple interest formula
        I = (P * N * R) / 100
        A = P + I
        EMI = A / (N * 12)

        return Loan.objects.create(
            customer=customer,
            principal_amount=P,
            interest_rate=R,
            loan_period_years=N,
            total_interest=I,
            total_amount=A,
            monthly_emi=EMI,
        )


# Serializer to show full loan ledger with payment insights
class LedgerSerializer(serializers.ModelSerializer):
    loan_id = serializers.UUIDField(read_only=True)
    customer_id = serializers.UUIDField(source="customer.customer_id", read_only=True)
    principal = serializers.DecimalField(
        source="principal_amount", max_digits=12, decimal_places=2
    )
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    monthly_emi = serializers.DecimalField(max_digits=12, decimal_places=2)

    # Computed fields based on associated payments
    amount_paid = serializers.SerializerMethodField()
    balance_amount = serializers.SerializerMethodField()
    emis_left = serializers.SerializerMethodField()

    # Nested list of transactions related to this loan
    transactions = TransactionSerializer(source="payments", many=True)

    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "customer_id",
            "principal",
            "total_amount",
            "monthly_emi",
            "amount_paid",
            "balance_amount",
            "emis_left",
            "transactions",
        ]

    def get_amount_paid(self, obj):
        # Sum of all payments made
        return sum(p.amount for p in obj.payments.all())

    def get_balance_amount(self, obj):
        # Remaining amount after payments
        return obj.total_amount - self.get_amount_paid(obj)

    def get_emis_left(self, obj):
        # Estimated EMIs remaining based on current balance
        balance = self.get_balance_amount(obj)
        return max(0, int(balance / obj.monthly_emi))


# Condensed loan summary view for overviews and dashboards
class LoanSummarySerializer(serializers.ModelSerializer):
    loan_id = serializers.UUIDField(read_only=True)
    amount_paid = serializers.SerializerMethodField()
    emis_left = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "principal_amount",
            "total_amount",
            "total_interest",
            "monthly_emi",
            "amount_paid",
            "emis_left",
        ]

    def get_amount_paid(self, loan):
        # Total amount paid so far for the loan
        return sum(payment.amount for payment in loan.payments.all())

    def get_emis_left(self, loan):
        # Remaining EMIs based on outstanding amount
        paid = self.get_amount_paid(loan)
        return max(int((loan.total_amount - paid) // loan.monthly_emi), 0)


# Overview of customer’s loans with summaries
class CustomerLoanOverviewSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField()
    total_loans = serializers.SerializerMethodField()
    loans = LoanSummarySerializer(many=True)

    def get_total_loans(self, obj):
        return len(obj["loans"])
