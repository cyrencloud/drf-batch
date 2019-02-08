from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(http_method_names=['PATCH'])
def view_200(request):
    return Response(data=request.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def view_201(request):
    return Response(data=request.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['PUT'])
def view_400(request):
    return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)
