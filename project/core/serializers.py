from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer



class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Custom serializer inorder to create a new user based on the custom User data model.
    """
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'username',
                  'kucoin_api_key', 'kucoin_api_secret', 'kucoin_passphrase']


class UserSerializer(BaseUserSerializer):
    """
    Custom serializer for representing users infor
    (KuCoin details have been excluded)
    """
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
