from rest_framework import serializers
from .models import EqContracts, EqTransactions



class EqContractSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    contract_num = serializers.CharField(max_length=20)
    acc_num = serializers.CharField(max_length=28)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    commission = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    date_add = serializers.DateField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    id_client_id = serializers.IntegerField()
    unp = serializers.CharField(source='id_client.unp', read_only=True)
    name = serializers.CharField(source='id_client.name', read_only=True)


    def create(self, validated_data):
        return EqContracts.objects.create(**validated_data)


    # наверное нужно будет удалить?
    def update(self, instance, validated_data):
        instance['contract_num'] = validated_data.get('contract_num', instance['contract_num'])
        instance['acc_num'] = validated_data.get('acc_num', instance['acc_num'])
        instance['balance'] = validated_data.get('balance', instance['balance'])
        instance['commission'] = validated_data.get('commission', instance['commission'])
        instance['is_active'] = validated_data.get('is_active', instance['is_active'])

        instance.save()
        return instance



class EqTransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    date_transaction = serializers.DateTimeField(read_only=True)
    sum_transaction = serializers.DecimalField(max_digits=15, decimal_places=2)
    sum_commission = serializers.DecimalField(max_digits=15, decimal_places=2)
    num_card = serializers.CharField()

    contract_id = serializers.IntegerField()
    contract_num = serializers.CharField(source='contract.contract_num', read_only=True)
    contract_acc_num = serializers.CharField(source='contract.acc_num', read_only=True)


    def create(self, validated_data):
        contract_id = validated_data.pop('contract_id')

        try:
            contract = EqContracts.objects.get(id=contract_id)
        except EqContracts.DoesNotExist:
            raise serializers.ValidationError({"contract_id": "Договор не найден"})
        return EqTransactions.objects.create(contract=contract, **validated_data)

