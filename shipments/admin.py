from django.contrib import admin
from .models import (
    Shipment, Package,
    Courier, ShipmentType, Mode, Product, PaymentMode,
    Carrier, Country, StatusType, PieceType
)


# -----------------------------
# PACKAGE INLINE - CHANGED TO STACKEDINLINE
# -----------------------------
class PackageInline(admin.StackedInline):  # Changed from TabularInline to StackedInline
    model = Package
    extra = 1
    
    # Custom fields to display packages as form fields
    fields = (
        ('qty', 'piece_type'),
        'description',
        ('length_cm', 'width_cm', 'height_cm'),
        'weight_kg',
    )


# -----------------------------
# SHIPMENT ADMIN
# -----------------------------
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    inlines = [PackageInline]

    fieldsets = (
        ("Shipper Details", {
            "fields": (
                ("shipper_name", "shipper_phone"),
                ("shipper_address", "shipper_email"),
            )
        }),
        ("Receiver Details", {
            "fields": (
                ("receiver_name", "receiver_phone"),
                ("receiver_address", "receiver_email"),
            )
        }),
        ("Shipment Details", {
            "fields": (
                ("shipment_number", "shipment_type"),
                ("courier", "weight_kg"),
                ("packages", "mode"),
                ("product", "quantity"),
                ("total_freight", "payment_mode"),
                ("carrier", "carrier_reference_no"),
                ("origin", "destination"),
                ("departure_time", "pickup_time"),
                ("pickup_date", "expected_delivery_date"),
                "comments",
            )
        }),
        ("Current Status", {
            "fields": (
                ("date", "time"),
                ("location", "status"),
                "remarks",
            )
        }),
    )

    class Media:
        css = {
            "all": ("admin/css/two_column.css",)
        }


# REGISTER DROPDOWN MODELS
admin.site.register(Courier)
admin.site.register(ShipmentType)
admin.site.register(Mode)
admin.site.register(Product)
admin.site.register(PaymentMode)
admin.site.register(Carrier)
admin.site.register(Country)
admin.site.register(StatusType)
admin.site.register(PieceType)