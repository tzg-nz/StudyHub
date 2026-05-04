from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import AccessTokenRecord


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None
        try:
            validated_token = self.get_validated_token(access_token)
            jti = validated_token.get('jti')
            if jti and AccessTokenRecord.objects.filter(jti=jti, is_blacklisted=True).exists():
                return None
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception:
            return None


class BlacklistJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, validated_token = result
        jti = validated_token.get('jti')
        if jti and AccessTokenRecord.objects.filter(jti=jti, is_blacklisted=True).exists():
            return None
        return (user, validated_token)
