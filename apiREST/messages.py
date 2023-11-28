import asyncio

from rest_framework import generics, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from djTBotCore.manager import TBotManager
from djTBotCore import TBotSentMessage

class MessageBroadcast(generics.GenericAPIView,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):

    permission_classes = [IsAuthenticated]
    pagination_class = (TokenAuthentication, )
    # queryset = models.Locations.objects.get_all()

    content = {
        'status': '',
        'message': None,
        'data': None,
    }

    def post(self, request, *args, **kwargs):
        data = request.data
        message = data["message"]

        try:
            tbot_manager = TBotManager.get_manager()
            tbot_manager.send_broadcast_message(TBotSentMessage(text=message, broadcast=True))
            status_resp = status.HTTP_200_OK
        except BaseException as e:
            # TODO Create logger
            # logger.critical(f"Error on executing request [{str(request)}] execute 'self.list': {str(e)}")
            status_resp = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.content['status'] = 'error'
            self.content['message'] = 'Internal server error.'
            self.content['data'] = None

        self.content['status'] = "OK"

        return Response(self.content, status=status_resp)

#
# class LocationsRGUD(generics.GenericAPIView,
#                     mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin):
#     permission_classes = [IsAuthenticated]
#     pagination_class = CustomPaginator
#     queryset = models.Locations.objects.get_all()
#
#     def get(self, request, *args, **kwargs):
#         try:
#             self.serializer_class = serializers.LocationsListSerializer
#             return_response = self.retrieve(request, *args, **kwargs)
#         except:
#             pass
#
#         return return_response
#
#     def put(self, request, *args, **kwargs):
#         self.serializer_class = serializers.LocationsListSerializer
#         return_response = self.update(request, *args, **kwargs)
#         return return_response
#
#     def delete(self, request, *args, **kwargs):
#         self.serializer_class = serializers.LocationsListSerializer
#         return_response = self.destroy(request, *args, **kwargs)
#         return return_response
