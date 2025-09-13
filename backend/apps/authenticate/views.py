from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            if "access" not in tokens or "refresh" not in tokens:
                return Response(
                    {"success": False, "message": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            access_token = tokens["access"]
            refresh_token = tokens["refresh"]

            res = Response({"success": True, "message": "Login successful."}, status=status.HTTP_200_OK)

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                samesite="None",
                secure=True,
                path="/"
            )

            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                samesite="None",
                secure=True,
                path="/"
            )

            return res

        except Exception as e:
            return Response(
                {"success": False, "message": f"Unexpected error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"refreshed": False, "message": "No refresh token provided."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            request.data["refresh"] = refresh_token
            response = super().post(request, *args, **kwargs)

            if "access" not in response.data:
                return Response(
                    {"refreshed": False, "message": "Refresh token is invalid or expired."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            access_token = response.data["access"]

            res = Response({"refreshed": True, "message": "Access token refreshed."}, status=status.HTTP_200_OK)
            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
                path="/"
            )
            return res

        except Exception as e:
            return Response(
                {"refreshed": False, "message": f"Unexpected error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            res = Response({"success": True, "message": "Logged out successfully."}, status=status.HTTP_200_OK)
            res.delete_cookie("access_token", path="/", samesite="None")
            res.delete_cookie("refresh_token", path="/", samesite="None")
            return res

        except Exception as e:
            return Response(
                {"success": False, "message": f"Unexpected error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )