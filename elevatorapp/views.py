from rest_framework.decorators import action
from .elevator_controller import ElevatorController
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Elevator, ElevatorRequest
from .serializers import ElevatorSerializer, ElevatorRequestSerializer

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        try:
            elevator = self.get_object()
            elevator.status = "running"
            elevator.save()
            return Response({"message": f"Elevator {pk} has started running."}, status=HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        try:
            elevator = self.get_object()
            ElevatorController.stop_elevator(elevator)
            return Response({"message": f"Elevator {pk} has been stopped."}, status=HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move_to_floor(self, request, pk=None):
        try:
            target_floor = request.data.get('target_floor')
            if target_floor is None or not isinstance(target_floor, int):
                return Response({"error": "Invalid target_floor provided."}, status=HTTP_400_BAD_REQUEST)

            elevator = self.get_object()
            ElevatorController.move_elevator(elevator, target_floor)
            return Response({"message": f"Elevator {pk} is moving to floor {target_floor}."}, status=HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST)

    # ... previous viewset code ...

class ElevatorRequestView(APIView):
    def post(self, request, elevator_id):
        try:
            floor = request.data.get('floor')
            if floor is None or not isinstance(floor, int):
                return Response({"error": "Invalid floor provided."}, status=HTTP_400_BAD_REQUEST)

            elevator = Elevator.objects.get(pk=elevator_id)
            elevator_request = ElevatorRequest(elevator=elevator, floor=floor)
            elevator_request.save()
            return Response({"message": f"Request added to Elevator {elevator_id} queue."}, status=HTTP_201_CREATED)
        except Elevator.DoesNotExist:
            return Response({"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST)

class ElevatorMaintenanceView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.operational = False
            elevator.save()
            return Response({"message": f"Elevator {elevator_id} is now under maintenance."}, status=HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST)

class ElevatorDoorOpenView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.door_open = True
            elevator.save()
            return Response({"message": f"The door of Elevator {elevator_id} is now open."}, status=HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST)

class ElevatorDoorCloseView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.door_open = False
            elevator.save()
            return Response({"message": f"The door of Elevator {elevator_id} is now closed."}, status=HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST)