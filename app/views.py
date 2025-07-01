import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Property
from datetime import datetime

API_BASE_URL = "https://api-fxz7qcfy4q-uc.a.run.app"

def agent_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            # Store username in session
            request.session['username'] = username
            request.session['password'] = password
            return redirect("property_list")
        else:
            return HttpResponse("Username and password are required", status=400)

    return render(request, "agent_login.html")




API_BASE_URL = "https://api-fxz7qcfy4q-uc.a.run.app"  # Replace with actual API base

def dashboard(request):
    agent_id = request.session.get('username')
    if not agent_id:
        return redirect("agent_login")

    monthly_counts = {month: 0 for month in range(1, 13)}
    current_year = datetime.now().year

    try:
        url = f"{API_BASE_URL}/{agent_id}/properties"
        response = requests.get(url)
        properties_data = response.json()

        for prop in properties_data:
            created_at = prop.get("createdAt")

            # Extract timestamp or ISO date string
            if isinstance(created_at, dict):
                date_value = created_at.get("$date")
                if isinstance(date_value, dict):
                    timestamp = int(date_value.get("$numberLong", 0)) / 1000
                    dt = datetime.fromtimestamp(timestamp)
                elif isinstance(date_value, str):
                    dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                else:
                    continue
            elif isinstance(created_at, str):
                if created_at.isdigit():
                    dt = datetime.fromtimestamp(int(created_at) / 1000)
                else:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            else:
                continue

            if dt.year == current_year:
                monthly_counts[dt.month] += 1

    except Exception as e:
        print(f"Error: {e}")

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_data = [(month_names[i - 1], monthly_counts[i]) for i in range(1, 13)]

    return render(request, 'dashboard.html', {
        'monthly_data': monthly_data,
        'current_year': current_year
    })




def property_list(request):
    agent_id = request.session.get('username')
    if not agent_id:
        return redirect("agent_login")

    try:
        # Make API call
        url = f"{API_BASE_URL}/{agent_id}/properties"
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse response
        properties_data = response.json()
        properties = [Property(data) for data in properties_data]
        
        context = {
            'properties': properties,
            'agent_id': agent_id,
        }
        return render(request, "properties_list.html", context)

    except requests.RequestException as e:
        print(f"API Error: {e}")
        return HttpResponse("Failed to fetch properties", status=500)

def agent_logout(request):
    request.session.flush()
    return redirect("agent_login")


def property_add(request):
    if request.method == "POST":
        agent_id = request.session.get('username')
        if not agent_id:
            return redirect("agent_login")

        property_data = {
            "location": request.POST.get("location"),
            "name": request.POST.get("name"),
            "type": request.POST.get("type"),
            "subtype": request.POST.get("subtype"),
            "bhk": int(request.POST.get("bhk") or 0),
            "sqft": request.POST.get("sqft"),
            "price": int(request.POST.get("price") or 0),
            "plotArea": request.POST.get("plotArea"),
            "unit": request.POST.get("unit"),
            "status": request.POST.get("status"),
            "remarks": request.POST.get("remarks"),
            "Pricingoptions": request.POST.get("pricingOptions"),
            "propertyDescription": request.POST.get("propertyDescription"),
            "ownerName": request.POST.get("ownerName"),
            "phoneNumber": request.POST.get("phoneNumber"),
            "whatsappNumber": request.POST.get("whatsappNumber"),
            "agent": agent_id,
            # Handle images if your API supports file uploads
        }

        try:
            url = f"{API_BASE_URL}/{agent_id}/properties"
            response = requests.post(url, json=property_data)
            response.raise_for_status()
            return redirect("property_list")
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return HttpResponse("Failed to add property", status=500)

    return render(request, "property_add.html")


def property_delete(request, property_id):
    agent_id = request.session.get('username')
    if not agent_id:
        return redirect("agent_login")

    try:
        url = f"{API_BASE_URL}/{agent_id}/properties/{property_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return redirect("property_list")
    except requests.RequestException as e:
        print(f"❌ Delete API Error: {e}")
        return HttpResponse("Failed to delete property", status=500)
    

def property_edit(request, property_id):
    agent_id = request.session.get('username')
    if not agent_id:
        return redirect("agent_login")

    if request.method == "GET":
        try:
            url = f"{API_BASE_URL}/{agent_id}/properties/{property_id}"
            response = requests.get(url)
            response.raise_for_status()
            property_data = response.json()
            return render(request, "property_edit.html", {"property": property_data})
        except requests.RequestException as e:
            print(f"❌ Fetch API Error: {e}")
            return HttpResponse("Failed to load property", status=500)
    elif request.method == "POST":
        updated_data = {
            "location": request.POST.get("location"),
            "name": request.POST.get("name"),
            "type": request.POST.get("type"),
            "subtype": request.POST.get("subtype"),
            "bhk": int(request.POST.get("bhk") or 0),
            "sqft": request.POST.get("sqft"),
            "price": int(request.POST.get("price") or 0),
            "plotArea": request.POST.get("plotArea"),
            "unit": request.POST.get("unit"),
            "status": request.POST.get("status"),
            "remarks": request.POST.get("remarks"),
            "Pricingoptions": request.POST.get("pricingOptions"),
            "propertyDescription": request.POST.get("propertyDescription"),
            "ownerName": request.POST.get("ownerName"),
            "phoneNumber": request.POST.get("phoneNumber"),
            "whatsappNumber": request.POST.get("whatsappNumber"),
        }

        try:
            url = f"{API_BASE_URL}/{agent_id}/properties/{property_id}"
            response = requests.put(url, json=updated_data)
            response.raise_for_status()
            return redirect("property_list")
        except requests.RequestException as e:
            print(f"❌ Update API Error: {e}")
            return HttpResponse("Failed to update property", status=500)

