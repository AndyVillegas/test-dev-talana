from django.db import models

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self):
        import math
        distribution = []
        maximum_passengers_row = 2
        len_rows = math.ceil(self.vehicle_type.max_capacity/maximum_passengers_row)
        onboard_passengers = 0
        for index_row in range(len_rows):
            row = [False, False]
            for passenger in range(maximum_passengers_row):
                if onboard_passengers < self.passengers:
                    row[passenger] = True
                    onboard_passengers += 1
            distribution.append(row)
        return distribution


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self):
        return self.end is not None


def validate_number_plate(plate: str) -> bool:
    splitted_plate = plate.split('-')
    if len(splitted_plate) != 3:
        return False
    return splitted_plate[0].isalpha() and splitted_plate[1].isnumeric() and splitted_plate[2].isnumeric()