from django.http.request import HttpRequest as Http


class HttpRequest(Http):
    def __init__(self):
        self.data = {}