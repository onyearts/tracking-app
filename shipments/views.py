from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import TemplateView
from .models import Shipment, Package

# Create your views here.
def home_view(request):
    context = {
        'page_title': 'Package Tracker - Home',
    }
    return render(request, 'home.html', context)


# track page views logic
def track_shipment(request):
    shipment = None
    packages = []
    tracking_number = ""
    
    # Check both GET and POST methods
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number', '').strip()
    elif request.method == 'GET':
        # Allow tracking number in URL parameter too
        tracking_number = request.GET.get('tracking_number', '').strip()
    
    if tracking_number:
        try:
            # Case-sensitive search
            shipment = Shipment.objects.get(shipment_number__exact=tracking_number)
            packages = Package.objects.filter(shipment=shipment)
        except Shipment.DoesNotExist:
            shipment = None
        except Exception as e:
            # Log the error for debugging
            print(f"Error fetching shipment: {e}")
            shipment = None
    
    return render(request, 'track.html', {
        'shipment': shipment,
        'tracking_number': tracking_number,
        'packages': packages
    })