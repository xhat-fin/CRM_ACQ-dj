from django.urls import path
from .views import (EqTransactionAPIView, EqContractAPIView, EqContractAPIViewID, EqTransactionAPIViewID,
                    EqTransactionContractAPIViewID, EqClientContractAPIViewID)



urlpatterns = [
    path('', EqContractAPIView.as_view(), name='contracts'),
    path('<int:id>/', EqContractAPIViewID.as_view(), name='contract_id'),
    path('eq-client/<int:id>/', EqClientContractAPIViewID.as_view(), name='client_contract_id'),
    path('transactions/', EqTransactionAPIView.as_view(), name='transactions'),
    path('transactions/<int:id>/', EqTransactionAPIViewID.as_view(), name='transaction_id'),
    path('transactions-contract/<int:id>/', EqTransactionContractAPIViewID.as_view(), name='transactions_contract_id'),

]