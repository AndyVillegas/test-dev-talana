import datetime

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from adventure import models, notifiers, repositories, serializers, usecases


class CreateVehicleAPIView(APIView):
    def post(self, request: Request) -> Response:
        payload = request.data
        repo = self.get_repository()
        usecase = usecases.CreateVehicle(repo).set_params(
            payload
        )
        vehicle = usecase.execute()
        return Response(
            {
                "id": vehicle.id,
                "name": vehicle.name,
                "passengers": vehicle.passengers,
                "vehicle_type": vehicle.vehicle_type.name,
            },
            status=201,
        )

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


class StartJourneyAPIView(generics.CreateAPIView):
    serializer_class = serializers.JourneySerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.StartJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


class StopJourneyAPIView(generics.UpdateAPIView):
    serializer_class = serializers.EmptyJourneySerializer
    queryset = models.Journey.objects

    def perform_update(self, serializer):
        repo = self.get_repository()
        usecase = usecases.StopJourney(repo).set_params(self.get_object())
        usecase.execute()

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()
