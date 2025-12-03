# shipments/utils.py
import random
import string
from datetime import datetime

def generate_tracking_number(carrier_name):
    """
    Generate a unique tracking number based on carrier name
    """
    if not carrier_name:
        return ""
    
    carrier = str(carrier_name).upper().strip()
    
    # USPS (United States Postal Service)
    if 'USPS' in carrier or 'UNITED STATES POSTAL SERVICE' in carrier:
        if random.choice([True, False]):
            # 22-digit format: 9400 1000 0000 0000 0000 00
            number = '94' + ''.join([str(random.randint(0, 9)) for _ in range(20)])
            formatted = ' '.join([number[i:i+4] for i in range(0, len(number), 4)])
            return formatted
        else:
            # Letter format: EC123456789US
            prefix = random.choice(['EA', 'EC', 'CP', 'RA', 'RB', 'RC'])
            middle = ''.join([str(random.randint(0, 9)) for _ in range(9)])
            return f'{prefix}{middle}US'
    
    # UPS (United Parcel Service)
    elif 'UPS' in carrier or 'UNITED PARCEL SERVICE' in carrier:
        # Format: 1Z9999W99999999999
        middle = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        return f'1Z{middle}'
    
    # FedEx (FDX)
    elif 'FEDEX' in carrier or 'FEDERAL EXPRESS' in carrier:
        # Format: 9999 9999 9999 or 9999 9999 9999 999
        length = random.choice([12, 15])
        number = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        formatted = ' '.join([number[i:i+4] for i in range(0, len(number), 4)])
        return formatted
    
    # DHL Express
    elif 'DHL' in carrier:
        # Format: 0000 0000 0000
        number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        formatted = ' '.join([number[i:i+4] for i in range(0, len(number), 4)])
        return formatted.rstrip()
    
    # AMZL (Amazon Logistics)
    elif 'AMAZON' in carrier or 'AMZL' in carrier:
        # Format: TBA123456789000
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        return f'TBA{suffix}'
    
    # Default for other carriers
    else:
        # Generate based on carrier initials + timestamp + random
        initials = ''.join([word[0] for word in carrier.split() if word])[:3].upper()
        if not initials:
            initials = 'TRK'
        timestamp = datetime.now().strftime('%y%m%d%H%M')
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f'{initials}-{timestamp}-{random_part}'