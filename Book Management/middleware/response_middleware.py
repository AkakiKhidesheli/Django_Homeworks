from django.utils.timezone import now


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.pink = '\033[38;2;255;105;180m'
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.reset = '\033[0m'

    def __call__(self, request):
        response_start = now()
        response = self.get_response(request)
        response_end = now()

        response_time = response_end - response_start

        print(f'{self.green}Response Time: {self.reset}{response_time} '
              f'{self.yellow}Address:{self.reset} {request.get_full_path()} '
              f'{self.pink}Method:{self.reset} {request.method}')
        return response
