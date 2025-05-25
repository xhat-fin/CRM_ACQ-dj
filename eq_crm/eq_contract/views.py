from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import EqTransactions, EqContracts
from .serializers import EqContractSerializer, EqTransactionSerializer



class EqContractAPIView(APIView):
    def get(self, request):
        contracts = EqContracts.objects.select_related('id_client').all()
        return Response(EqContractSerializer(contracts, many=True).data)


    def post(self, request):
        serializer = EqContractSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"NewContract": serializer.data})



class EqContractAPIViewID(APIView):
    def get(self, request, id):
        contract = EqContracts.objects.select_related('id_client').get(id=id)
        return Response(EqContractSerializer(contract).data)


    def put(self, request, **kwargs):
        id = kwargs.get('id')
        if not id:
            Response({"error": "id not exists"})
        try:
            instance = EqContracts.objects.get(id=id)
        except:
            return Response({"error": "client not exists"})

        serializer = EqContractSerializer(data=request.data, instance=instance, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({"Contract": serializer.data})



class EqTransactionAPIView(APIView):
    def get(self, request):
        transactions = EqTransactions.objects.select_related('contract').all()
        return Response(EqTransactionSerializer(transactions, many=True).data)

    def post(self, request):
        serializer = EqTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"NewTransaction": serializer.data})



class EqTransactionAPIViewID(APIView):
    def get(self, request, id):
        transaction = EqTransactions.objects.select_related('contract').get(id=id)
        return Response(EqTransactionSerializer(transaction).data)



class EqTransactionContractAPIViewID(APIView):
    def get(self, request, id):
        transactions = EqTransactions.objects.filter(contract_id=id).select_related('contract')
        return Response(EqTransactionSerializer(transactions, many=True).data)