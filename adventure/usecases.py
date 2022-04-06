from __future__ import annotations

from . import models
from .notifiers import Notifier
from .repositories import JourneyRepository


class CreateVehicle:
    def __init__(self, repository: JourneyRepository):
        self.repository = repository

    def set_params(self, data: dict) -> CreateVehicle:
        self.data = data
        return self

    def execute(self) -> models.Vehicle:
        vehicle_type = models.VehicleType.objects.get(name=self.data["vehicle_type"])
        vehicle = models.Vehicle.objects.create(
            name=self.data["name"],
            passengers=self.data["passengers"],
            vehicle_type=vehicle_type,
        )
        return vehicle


class StartJourney:
    def __init__(self, repository: JourneyRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def set_params(self, data: dict) -> StartJourney:
        self.data = data
        return self

    def execute(self) -> models.Journey:
        car = self.repository.get_or_create_car()
        vehicle = self.repository.create_vehicle(vehicle_type=car, **self.data)
        if not vehicle.can_start():
            raise StartJourney.CantStart("vehicle can't start")

        journey = self.repository.create_journey(vehicle)
        self.notifier.send_notifications(journey)
        return journey

    class CantStart(Exception):
        pass


class StopJourney:
    def __init__(self, repository: JourneyRepository):
        self.repository = repository

    def set_params(self, data: models.Journey) -> StopJourney:
        self.data = data
        return self

    def execute(self) -> models.Journey:
        journey = self.repository.stop_journey(self.data)
        return journey
