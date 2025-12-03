from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .utils import generate_tracking_number
from .models import Carrier, Shipment, Package

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


def generate_tracking_view(self, request):
    """Admin view to generate tracking number"""
    import json
    from django.http import JsonResponse
    
    # Try to get parameters from both GET and POST
    if request.method == 'GET':
        carrier_id = request.GET.get('carrier_id')
        carrier_name = request.GET.get('carrier_name', '')
    else:
        try:
            data = json.loads(request.body)
            carrier_id = data.get('carrier_id')
            carrier_name = data.get('carrier_name', '')
        except:
            carrier_id = None
            carrier_name = ''
    
    print(f"DEBUG: Received carrier_id={carrier_id}, carrier_name={carrier_name}")
    
    if not carrier_id and not carrier_name:
        return JsonResponse({'success': False, 'error': 'Carrier information is required'})
    
    # Generate tracking number
    try:
        if carrier_name:
            tracking_number = generate_tracking_number(carrier_name)
        elif carrier_id:
            try:
                carrier = Carrier.objects.get(id=carrier_id)
                tracking_number = generate_tracking_number(carrier.name)
            except Carrier.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Carrier not found'})
        else:
            return JsonResponse({'success': False, 'error': 'No carrier information provided'})
        
        # Check for uniqueness
        from .models import Shipment
        # Limit retries to prevent infinite loop
        max_retries = 5
        retry_count = 0
        
        while Shipment.objects.filter(shipment_number=tracking_number).exists() and retry_count < max_retries:
            if carrier_name:
                tracking_number = generate_tracking_number(carrier_name)
            elif carrier_id:
                carrier = Carrier.objects.get(id=carrier_id)
                tracking_number = generate_tracking_number(carrier.name)
            retry_count += 1
        
        print(f"DEBUG: Generated tracking number: {tracking_number}")
        
        return JsonResponse({
            'success': True,
            'tracking_number': tracking_number
        })
        
    except Exception as e:
        print(f"DEBUG: Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
def generate_tracking_number_view(request):
    """AJAX view to generate tracking number"""
    try:
        data = json.loads(request.body)
        carrier_id = data.get('carrier_id')
        carrier_name = data.get('carrier_name', '')
        
        if not carrier_id and not carrier_name:
            return JsonResponse({'success': False, 'error': 'Carrier information is required'})
        
        # If we have carrier_name, use it directly
        if carrier_name:
            tracking_number = generate_tracking_number(carrier_name)
        else:
            # Try to get carrier name from ID
            from .models import Carrier
            try:
                carrier = Carrier.objects.get(id=carrier_id)
                tracking_number = generate_tracking_number(carrier.name)
            except Carrier.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Carrier not found'})
        
        # Check if it's unique (optional)
        while Shipment.objects.filter(shipment_number=tracking_number).exists():
            # Regenerate if duplicate (very rare but possible)
            tracking_number = generate_tracking_number(carrier_name or (carrier.name if carrier else ''))
        
        return JsonResponse({
            'success': True,
            'tracking_number': tracking_number
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    


def about_page(request):
    """About Us page"""
    return render(request, 'about.html')

def blog_page(request):
    """Blog page"""
    return render(request, 'blog.html')