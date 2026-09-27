from django.shortcuts import render
from .models import *
from django.http import JsonResponse

def home(request):
    context = {'amenities':Amenities.objects.all()}
    return render(request,'home.html',context)

def get_hotel(request):
    try:
        hotel_objs = Hotel.objects.all()
        sort_by = request.GET.get('sort_by')

        if sort_by == 'asc':
            hotel_objs = hotel_objs.order_by('hotel_price')

        elif sort_by == 'desc':
            hotel_objs = hotel_objs.order_by('-hotel_price')

        amount = request.GET.get('amount')

        if amount:
            hotel_objs = hotel_objs.filter(
                hotel_price__lte=amount
            )

        amenities = request.GET.get('amenities')

        if amenities:
            amenities = amenities.split(',')

            hotel_objs = hotel_objs.filter(
                amenities__id__in=amenities
            ).distinct()

        payload = []

        for hotel in hotel_objs:
            payload.append({
                'hotel_name': hotel.hotel_name,
                'hotel_price': hotel.hotel_price,
                'hotel_description': hotel.hotel_description,
                'banner_image': str(hotel.banner_image),
                'amenities': hotel.get_amenities()
            })

        return JsonResponse(payload, safe=False)

    except Exception as e:
        print(e)
        return JsonResponse({
            'message': 'Something went wrong!'
        }, status=500)
