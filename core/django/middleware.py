from django.contrib.auth.middleware import AuthenticationMiddleware


class ProfileAuthenticationMiddleware(AuthenticationMiddleware):
    """
    usage:
        1. create `profile` property in django user to return profile object
        2. register this middleware in django settings
        3. use `request.profile` to get user profile in every views
    """
    def process_request(self, request):
        super(ProfileAuthenticationMiddleware, self).process_request(request)
        profile = getattr(request.user, 'profile', None)
        setattr(request, 'profile', profile)
