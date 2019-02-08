import json
from copy import copy

from django.conf import settings
from django.db import transaction
from django.urls.exceptions import Resolver404
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RequestSerializer
from .utils import resolve_with_prefix
from .exceptions import RequestFailed


DEFAULT_SKIP_ERRORS = False
DEFAULT_USE_TRANSACTION = True
DEFAULT_CONNECTION_ALIAS = "default"


class Batch(generics.GenericAPIView):
    serializer_class = RequestSerializer

    skip_errors = None
    use_transaction = None
    connection_alias = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s = getattr(settings, 'DRF_BATCH', {})
        self.skip_errors = self.skip_errors or s.get('DEFAULT_SKIP_ERRORS', DEFAULT_SKIP_ERRORS)
        self.use_transaction = self.use_transaction or s.get('DEFAULT_USE_TRANSACTION', DEFAULT_USE_TRANSACTION)
        self.connection_alias = self.connection_alias or s.get('DEFAULT_CONNECTION_ALIAS', DEFAULT_CONNECTION_ALIAS)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(many=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if self.use_transaction:
                with transaction.atomic(self.connection_alias):
                    self.perform()
            else:
                self.perform()
        except RequestFailed as e:
            return Response(data=e.request, status=e.request['response']['status_code'])
        return Response(request.data)

    def perform(self):
        for operation in self.request.data:
            req = self.make_request(operation)
            try:
                view, args, kwargs = resolve_with_prefix(req.path)
            except Resolver404:
                operation["response"] = {
                    "status_code": status.HTTP_404_NOT_FOUND
                }
            else:
                response = view(req, *args, **kwargs)
                operation["response"] = {
                    "status_code": response.status_code,
                    "data": response.data
                }

            if not status.is_success(operation['response']['status_code']) and not self.skip_errors:
                raise RequestFailed(operation)

    def make_request(self, data):
        req = copy(self.request._request)
        req.method = data["method"]
        req.path = data["path"]
        if "data" in data:
            req._body = json.dumps(data["data"]).encode("utf-8")
        return req
