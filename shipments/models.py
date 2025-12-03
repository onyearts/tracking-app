from django.db import models


# -----------------------------
# DROPDOWN MODELS
# -----------------------------
class ShipmentType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Courier(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Mode(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PaymentMode(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Carrier(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class StatusType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PieceType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# -----------------------------
# MAIN SHIPMENT MODEL
# -----------------------------
class Shipment(models.Model):
    # Manual number for now
    shipment_number = models.CharField(max_length=200)

    # Shipper
    shipper_name = models.CharField(max_length=200)
    shipper_phone = models.CharField(max_length=200)
    shipper_address = models.CharField(max_length=255)
    shipper_email = models.EmailField()

    # Receiver
    receiver_name = models.CharField(max_length=200)
    receiver_phone = models.CharField(max_length=200)
    receiver_address = models.CharField(max_length=255)
    receiver_email = models.EmailField()

    # Shipment details
    shipment_type = models.ForeignKey(ShipmentType, on_delete=models.SET_NULL, null=True)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    packages = models.IntegerField()
    mode = models.ForeignKey(Mode, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    total_freight = models.CharField(max_length=200)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True)
    carrier = models.ForeignKey(Carrier, on_delete=models.SET_NULL, null=True)
    carrier_reference_no = models.CharField(max_length=200, null=True, blank=True)
    origin = models.ForeignKey(Country, related_name="origin_country", on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey(Country, related_name="dest_country", on_delete=models.SET_NULL, null=True)

    departure_time = models.TimeField()
    pickup_time = models.TimeField()
    pickup_date = models.DateField()
    expected_delivery_date = models.DateField()

    comments = models.TextField(blank=True, null=True)

    # current status
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="location_country")
    status = models.ForeignKey(StatusType, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Shipment {self.shipment_number}"


# -----------------------------
# PACKAGE INLINE MODEL
# -----------------------------
class Package(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="packages_list")
    qty = models.IntegerField()
    piece_type = models.ForeignKey(PieceType, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    length_cm = models.DecimalField(max_digits=10, decimal_places=2)
    width_cm = models.DecimalField(max_digits=10, decimal_places=2)
    height_cm = models.DecimalField(max_digits=10, decimal_places=2)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Package {self.qty}x {self.piece_type}"
