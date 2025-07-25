from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from .serializers import *
from django.shortcuts import get_object_or_404
from .models import Loan, Customer, Payment


# API to create a new loan
class CreateLoanAPIView(APIView):
    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save()
            # Prepare response with key loan details
            response_data = {
                "loan_id": str(loan.loan_id),
                "customer_id": str(loan.customer.customer_id),
                "total_amount_payable": float(loan.total_amount),
                "monthly_emi": float(loan.monthly_emi),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to create a new customer
class CreateCustomerView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# API to fetch detailed loan information using loan_id
class LoanDetailView(APIView):
    def get(self, request, loan_id):
        loan = get_object_or_404(
            Loan.objects.select_related("customer"), loan_id=loan_id
        )

        # Return customer and loan-related information
        return Response(
            {
                "loan_id": str(loan.loan_id),
                "customer_name": loan.customer.name,
                "customer_email": loan.customer.email,
                "customer_address": loan.customer.address,
                "loan_amount": float(loan.principal_amount),
                "interest_rate": float(loan.interest_rate),
                "loan_period_years": loan.loan_period_years,
                "total_interest": float(loan.total_interest),
                "total_amount_payable": float(loan.total_amount),
                "monthly_emi": float(loan.monthly_emi),
            }
        )


# API to record a loan payment for a given loan_id
class LoanPaymentView(APIView):
    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, loan_id=loan_id)
        serializer = PaymentSerializer(data=request.data, context={"loan": loan})

        if serializer.is_valid():
            payment = serializer.save()

            # Update loan payment-related fields
            loan.amount_paid += payment.amount
            loan.balance_amount = loan.total_amount - loan.amount_paid
            loan.emis_left = max(0, round(loan.balance_amount / loan.monthly_emi))
            loan.save()

            return Response(
                {
                    "payment_id": str(payment.payment_id),
                    "loan_id": str(loan.loan_id),
                    "message": "Payment recorded successfully.",
                    "remaining_balance": float(loan.balance_amount),
                    "emis_left": loan.emis_left,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to return loan ledger info (all details including payment history, etc.)
class LoanLedgerView(APIView):
    def get(self, request, loan_id):
        loan = get_object_or_404(Loan, loan_id=loan_id)
        serializer = LedgerSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API to fetch all loans associated with a customer
class CustomerLoanOverviewAPIView(APIView):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, customer_id=customer_id)
        loans = customer.loans.all()

        if not loans.exists():
            return Response(
                {"detail": "No loans found for this customer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CustomerLoanOverviewSerializer(
            {"customer_id": str(customer.customer_id), "loans": loans}
        )
        return Response(serializer.data)
