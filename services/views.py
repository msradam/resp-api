# Create your views here.
import json

from django.conf import settings
from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response

from .resources import find_nearest_hospitals


class List(views.APIView):
    def post(self, request):
        lat = request.data.pop("lat")
        lon = request.data.pop("lon")
        country = request.data.pop("country")
        with open(settings.BASE_DIR + "/services/services_db.json", 'r') as jf:
            services_db = json.load(jf)
            services_db.append(
                [lat] + [lon] + [country] + find_nearest_hospitals(country, lat, lon))
        with open(settings.BASE_DIR + "/services/services_db.json", 'w') as jf:
            json.dump(services_db, jf)
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        if request.data:
            lat = request.data.pop("lat")
            lon = request.data.pop("lon")
            country = request.data.pop("country")
        final_response = []
        with open(settings.BASE_DIR + "/services/services_db.json") as jf:
            services_db = json.load(jf)
            for entry in services_db:
                if entry[2] == country:
                    final_response.append(entry)
        return Response(final_response)
