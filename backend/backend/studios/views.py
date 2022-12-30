from . import client
from .models import Studio
from .serializers import StudioSerializer
from classes.models import ClassInstances
from classes.serializers import ClassInstancesSerializer
from django.shortcuts import get_object_or_404
from geopy.distance import geodesic as GD
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.

class NearbyStudioListAPIView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = StudioSerializer

    def get(self, request):
        user_latitude = request.data.get("latitude")
        user_longitude = request.data.get("longitude")

        queryset = Studio.objects.all()
        data = StudioSerializer(queryset, many=True, context={'request': request}).data
        
        list_of_studios = []
        for obj in data:
            studio_latitude = obj["latitude"]
            studio_longitude = obj["longitude"]

            user_location = (user_latitude, user_longitude)
            studio_location = (studio_latitude, studio_longitude)

            distance = GD(user_location, studio_location).km
            list_of_studios.append((distance, obj))
        
        list_of_studios.sort(key=lambda tup: tup[0])
        new_list = []
        for obj_new in list_of_studios:
            data = {
                'pk': obj_new[1]['pk'],
                'owner': obj_new[1]['owner'],
                'name': obj_new[1]['name'],
                'phone_number': obj_new[1]['phone_number'],
                'address': obj_new[1]['address'],
                'postal_code': obj_new[1]['postal_code'],
                'latitude': obj_new[1]['latitude'],
                'longitude': obj_new[1]['longitude'],
            }
            new_list.append(data)
        
        page = self.paginate_queryset(new_list)
        return self.get_paginated_response(page)

class StudioListAPIView(generics.ListAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

class StudioDetailAPIView(generics.RetrieveAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

class ClassListAPIView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = ClassInstancesSerializer

    def get(self, request, pk):
        studio_obj = get_object_or_404(Studio, pk=pk)

        queryset_future_date = ClassInstances.objects.filter(studio=studio_obj.pk, cancelled = False, class_date__gt = datetime.date.today())
        queryset_today = ClassInstances.objects.filter(studio=studio_obj.pk, cancelled = False, class_date = datetime.date.today(), start_time__gte = datetime.datetime.now().time())

        # union of the two querysets
        cleaned_data = queryset_future_date | queryset_today
        cleaned_data = cleaned_data.order_by("class_date", "start_time")

        data = ClassInstancesSerializer(cleaned_data, many=True).data
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)

class StudioSearchAPIView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = StudioSerializer
    queryset = ''

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        studio = request.GET.get('studio')
        if not query:
            return Response('', status=400)

        classes_results = client.perform_search_studio_class(query, studio)
        
        page = self.paginate_queryset(classes_results['hits'])
        return self.get_paginated_response(page)
