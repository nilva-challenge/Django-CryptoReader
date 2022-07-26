from rest_framework import serializers
from Encryptor.hasher_tools import check_pass_phrase
from kucoin.KucoinRequestHandler import now_in_mili


class KucoinOrderSerializer(serializers.Serializer):
    STATUS_CHOICES = (('active', 'active'), ('done', 'done'))
    SIDE_CHOICES = (('buy', 'buy'), ('sell', 'sell'))

    TYPE_CHOICES = (('limit', 'limit'), ('market', 'market'),
                    ('limit_stop', 'limit_stop'),
                    ('market_stop', 'market_stop'))

    TRADE_TYPE_CHOICES = (('TRADE', 'TRADE'), ('MARGIN_TRADE ', 'MARGIN_TRADE '))

    status = serializers.ChoiceField(required=False,write_only=True,choices=STATUS_CHOICES,default='active')
    symbol = serializers.CharField(required=False, write_only=True)
    side = serializers.ChoiceField(required=False, write_only=True, choices=SIDE_CHOICES)
    type = serializers.ChoiceField(required=False, write_only=True, choices=TYPE_CHOICES)
    tradeType = serializers.ChoiceField(required=False, write_only=True, choices=TRADE_TYPE_CHOICES)
    startAt = serializers.CharField(required=False, write_only=True)
    endAt = serializers.CharField(required=False, write_only=True)

    security_pass_phrase = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context.get('user')
        if not check_pass_phrase(user,attrs.get('security_pass_phrase')):
            raise serializers.ValidationError({"Security Pass Phrase":"Wrong password"})
        del attrs['security_pass_phrase']
        time_attrs = []

        if 'startAt' not in attrs and 'endAt' not in attrs :
            time_attrs = None
            return attrs, time_attrs

        if 'startAt' in attrs:
            time_attrs.append(int(attrs.get('startAt')))
            del attrs['startAt']
        else:
            time_attrs.append(1)

        if 'endAt' in attrs:
            time_attrs.append(int(attrs.get('endAt')))
            del attrs['endAt']
        else:
            time_attrs.append(now_in_mili() + 10)


        return attrs , time_attrs

