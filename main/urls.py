from django.urls import path
from .views import *

urlpatterns = [
    path("loans/", CreateLoanAPIView.as_view(), name="create-loan"),
    path("customers/", CreateCustomerView.as_view(), name="create-customer"),
    path("loans/<uuid:loan_id>/", LoanDetailView.as_view(), name="loan-detail"),
    path("loans/<uuid:loan_id>/payments/", LoanPaymentView.as_view(), name="record-payment"),
    path("loans/<uuid:loan_id>/ledger/", LoanLedgerView.as_view(), name="loan-ledger"),
    path("customers/<uuid:customer_id>/overview/", CustomerLoanOverviewAPIView.as_view()),
]
