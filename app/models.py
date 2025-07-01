from django.db import models


class Property:
    def __init__(self, data):
        self.id = data.get('_id', '')
        self.location = data.get('location', '')
        self.remarks = data.get('remarks')
        self.verified = data.get('verified', '')
        self.name = data.get('name', '')
        self.type = data.get('type', '')
        self.subtype = data.get('subtype', '')
        self.bhk = data.get('bhk', 0)
        self.sqft = data.get('sqft', '')
        self.price = data.get('price', 0)
        self.plot_area = data.get('plotArea', '')
        self.unit = data.get('unit', '')
        self.listed_on = data.get('listedOn', 0)
        self.status = data.get('status', '')
        self.agent = data.get('agent')
        self.pricing_options = data.get('Pricingoptions', '')
        self.property_description = data.get('propertyDescription', '')
        self.images = data.get('images', [])
        self.owner_name = data.get('ownerName', '')
        self.phone_number = data.get('phoneNumber', '')
        self.whatsapp_number = data.get('whatsappNumber', '')
        self.property_id = data.get('propertyId', '')