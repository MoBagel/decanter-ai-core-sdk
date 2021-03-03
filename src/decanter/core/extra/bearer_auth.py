import requests
class BearerAuth(requests.auth.AuthBase):
        def __init__(self, apikey):
            self.apikey = apikey
        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.apikey
            return r