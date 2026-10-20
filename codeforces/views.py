from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import sync_user_codeforces

User = get_user_model()


class CodeforcesConnectView(APIView):
    """
    POST /api/codeforces/connect/
    Connect or update the authenticated user's Codeforces handle.
    Body: { "handle": "tourist" }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        handle = request.data.get('handle', '').strip()
        if not handle:
            return Response(
                {'error': 'Codeforces handle is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.codeforces_handle = handle
        request.user.is_handle_verified = False
        request.user.save(update_fields=['codeforces_handle', 'is_handle_verified'])
        return Response({
            'message': f'Handle updated to {handle}. Use /api/codeforces/sync/ to fetch data.',
            'handle': handle,
        })


class CodeforcesSyncView(APIView):
    """
    POST /api/codeforces/sync/
    Trigger a full synchronization of Codeforces data for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        handle = user.codeforces_handle
        if not handle:
            return Response(
                {'error': 'No Codeforces handle connected. Use /api/codeforces/connect/ first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            result = sync_user_codeforces(user, handle)
            return Response({
                'message': f'Sync complete for handle: {handle}',
                'result': result,
            })
        except Exception as e:
            return Response(
                {'error': f'Sync failed: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class CodeforcesStatusView(APIView):
    """
    GET /api/codeforces/status/
    Get the Codeforces connection status for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'handle': user.codeforces_handle or None,
            'is_handle_verified': user.is_handle_verified,
            'connected': bool(user.codeforces_handle),
        })
