# shipments/admin.py - UPDATED WITH TABLE IMPROVEMENTS
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.utils.html import format_html
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .models import (
    Shipment, Package,
    Courier, ShipmentType, Mode, Product, PaymentMode,
    Carrier, Country, StatusType, PieceType
)
from .utils import generate_tracking_number


# -----------------------------
# PACKAGE INLINE
# -----------------------------
class PackageInline(admin.StackedInline):
    model = Package
    extra = 1
    fields = (
        ('qty', 'piece_type'),
        'description',
        ('length_cm', 'width_cm', 'height_cm'),
        'weight_kg',
    )


# -----------------------------
# SHIPMENT ADMIN - UPDATED
# -----------------------------
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    inlines = [PackageInline]
    readonly_fields = ('auto_generate_button', 'reference_example',)
    
    # ADD THIS: Better list display with more info
    list_display = (
        'tracking_with_copy',
        'carrier_info',
        'shipper_info',
        'receiver_info',
        'status_info',
        'dates_info',
        'action_buttons'
    )
    
    # ADD THIS: Add filters
    list_filter = ('carrier', 'status', 'shipment_type')
    
    # ADD THIS: Add search
    search_fields = ('shipment_number', 'shipper_name', 'receiver_name', 'carrier__name')
    
    # ADD THIS: Items per page
    list_per_page = 20

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
                ("shipment_number", "auto_generate_button", "shipment_type"),
                ("carrier", "carrier_reference_no", "reference_example"),
                ("courier", "weight_kg"),
                ("packages", "mode"),
                ("product", "quantity"),
                ("total_freight", "payment_mode"),
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
            "all": ("admin/css/two_column.css", "admin/css/shipment_list.css",)
        }
        js = (
            "admin/js/vendor/jquery/jquery.min.js",
            "admin/js/shipment_admin.js",
            "admin/js/copy_tracking.js",
        )

    def reference_example(self, obj):
        """Show example reference number formats"""
        return format_html(
            '''
            <div style="font-size: 11px; color: #666; margin-top: 5px;">
                <strong>Reference No. formats:</strong><br>
                • USPS: USPS-250301-ABC123<br>
                • UPS: UPS-250301-1A2B3C4D<br>
                • FedEx: FED-250301-123456789<br>
                • DHL: DHL-250301-0123456789<br>
                • Amazon: AMZ-250301-ABC123DE
            </div>
            '''
        )
    reference_example.short_description = "Reference No. format"
    

    # ADD THESE METHODS FOR BETTER LIST DISPLAY:
    def tracking_with_copy(self, obj):
        """Display tracking number with copy button"""
        if not obj.shipment_number:
            return "No tracking"
        
        return format_html(
            '''
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-family: monospace; font-weight: bold; 
                           padding: 4px 8px; border-radius: 4px; border: 1px solid #ddd;">
                    {tracking}
                </span>
                <button type="button" class="copy-tracking-btn" 
                        data-tracking="{tracking}" 
                        style="background: #417690; color: white; border: none; 
                               border-radius: 3px; padding: 2px 8px; font-size: 11px; 
                               cursor: pointer;" 
                        title="Copy to clipboard">
                    📋
                </button>
            </div>
            ''',
            tracking=obj.shipment_number
        )
    tracking_with_copy.short_description = "Tracking #"
    
    def carrier_info(self, obj):
        """Display carrier with color"""
        if not obj.carrier:
            return "-"
        
        carrier_colors = {
            'UPS': '#351C15',      # Brown
            'FEDEX': '#4D148C',    # Purple
            'USPS': '#004B87',     # Blue
            'DHL': '#FFCC00',      # Yellow
            'AMAZON': '#FF9900',   # Orange
        }
        
        carrier_name = obj.carrier.name.upper()
        color = carrier_colors.get(carrier_name, '#666666')
        
        return format_html(
            '<span style="background: {color}; color: white; padding: 2px 6px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{name}</span>',
            color=color,
            name=carrier_name[:10]
        )
    carrier_info.short_description = "Carrier"
    
    def shipper_info(self, obj):
        """Display shipper info compactly"""
        return format_html(
            '<div style="font-size: 12px;">'
            '<strong>{name}</strong><br>'
            '<small>{phone}</small>'
            '</div>',
            name=obj.shipper_name[:15] + ("..." if len(obj.shipper_name) > 15 else ""),
            phone=obj.shipper_phone[:12] if obj.shipper_phone else "No phone"
        )
    shipper_info.short_description = "Shipper"
    
    def receiver_info(self, obj):
        """Display receiver info compactly"""
        return format_html(
            '<div style="font-size: 12px;">'
            '<strong>{name}</strong><br>'
            '<small>{phone}</small>'
            '</div>',
            name=obj.receiver_name[:15] + ("..." if len(obj.receiver_name) > 15 else ""),
            phone=obj.receiver_phone[:12] if obj.receiver_phone else "No phone"
        )
    receiver_info.short_description = "Receiver"
    
    def status_info(self, obj):
        """Display status with color"""
        if not obj.status:
            return "-"
        
        status_colors = {
            'PENDING': '#FFA500',      # Orange
            'IN_TRANSIT': '#1E90FF',   # Blue
            'DELIVERED': '#32CD32',    # Green
            'CANCELLED': '#DC143C',    # Red
            'ON_HOLD': '#FFD700',      # Yellow
        }
        
        status_name = obj.status.name.replace('_', ' ').title()
        color = status_colors.get(obj.status.name, '#666666')
        
        return format_html(
            '<span style="background: {color}; color: white; padding: 2px 8px; '
            'border-radius: 10px; font-size: 11px; font-weight: bold;">{status}</span>',
            color=color,
            status=status_name
        )
    status_info.short_description = "Status"
    
    def dates_info(self, obj):
        """Display important dates"""
        pickup = obj.pickup_date.strftime('%b %d') if obj.pickup_date else "-"
        expected = obj.expected_delivery_date.strftime('%b %d') if obj.expected_delivery_date else "-"
        
        return format_html(
            '<div style="font-size: 11px; line-height: 1.3;">'
            '<strong>Pickup:</strong> {pickup}<br>'
            '<strong>Expected:</strong> {expected}'
            '</div>',
            pickup=pickup,
            expected=expected
        )
    dates_info.short_description = "Dates"
    
    def action_buttons(self, obj):
        """Simple action buttons"""
        return format_html(
            '''
            <div style="display: flex; gap: 5px;">
                <a href="{edit_url}" class="button" 
                   style="background: #417690; color: white; padding: 4px 8px; 
                          border-radius: 3px; text-decoration: none; font-size: 12px;">
                    Edit
                </a>
            </div>
            ''',
            edit_url=reverse('admin:shipments_shipment_change', args=[obj.id]),
            track_url=f"#track-{obj.id}"
        )
    action_buttons.short_description = "Actions"
    
    def auto_generate_button(self, obj):
        return format_html(
            '<button type="button" id="generate-tracking" class="button" style="margin-left: 10px;">'
            'Auto-generate</button>'
            '<small style="margin-left: 10px; color: #666;">'
            'Select carrier first, then click to generate</small>'
        )
    auto_generate_button.short_description = "Generate Tracking"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-tracking/', self.admin_site.admin_view(self.generate_tracking_view), 
                 name='generate_tracking'),
        ]
        return custom_urls + urls
    
    def generate_tracking_view(self, request):
        """Admin view to generate tracking number"""
        carrier_id = request.GET.get('carrier_id')
        carrier_name = request.GET.get('carrier_name', '')
        
        if not carrier_id and not carrier_name:
            return JsonResponse({'success': False, 'error': 'Carrier information is required'})
        
        # Generate tracking number
        if carrier_name:
            tracking_number = generate_tracking_number(carrier_name)
        else:
            try:
                carrier = Carrier.objects.get(id=carrier_id)
                tracking_number = generate_tracking_number(carrier.name)
            except Carrier.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Carrier not found'})
        
        # Check for uniqueness
        from .models import Shipment
        while Shipment.objects.filter(shipment_number=tracking_number).exists():
            tracking_number = generate_tracking_number(carrier_name or carrier.name)
        
        return JsonResponse({
            'success': True,
            'tracking_number': tracking_number
        })


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