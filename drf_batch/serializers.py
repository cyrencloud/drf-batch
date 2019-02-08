from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=(
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("PATCH", "PATCH"),
        ("DELETE", "DELETE"),
    ))
    path = serializers.CharField(max_length=255)  # TODO: what is the max length of a path?
    data = serializers.Serializer(required=False)
