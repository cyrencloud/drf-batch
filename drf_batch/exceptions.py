class RequestFailed(Exception):
    def __init__(self, request):
        super().__init__(f'batch request failed with status code: {request["response"]["status_code"]}')
        self.request = request
