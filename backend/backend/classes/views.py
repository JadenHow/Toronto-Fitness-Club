from . import client
from classes.models import ClassInstances
from classes.serializers import ClassInstancesSerializer
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from subscriptions.models import SubscriptionInstance
from users.models import Enrolled, RegisterUser
from users.serializers import EnrolledSerializer
import datetime

class EnrolAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes= [permissions.IsAuthenticated]

    def post(self, request, studio_id, class_id):
        class_instance = get_object_or_404(ClassInstances, pk=class_id)

        if not get_object_or_404(RegisterUser, user=request.user.id).subscribed:
            return Response({"msg" : "not subscribed"}, status=404)

        if get_object_or_404(SubscriptionInstance, user=request.user.id).renewal_date < class_instance.class_date:
            return Response({"msg" : "subscription will be expired before the class, please enrol after your subscription is renewed or subscribe to a longer subscription"}, status=404)

        # print(request.user)
        curr_time = datetime.datetime.now().time()
        today = datetime.date.today()

        # can't already be enrolled
        if Enrolled.objects.filter(class_instance = class_id, user = request.user.id).exists():
            print(Enrolled.objects.filter(class_instance = class_id, user = request.user.id))
            return Response({
                "msg": "Already enrolled" 
            }, status=404)


        if class_instance.currently_enrolled < class_instance.capacity and class_instance.class_date >= today:
            if class_instance.class_date == today and class_instance.start_time <= curr_time:
                return Response({
                    "msg": "Class has already passed" 
                    })

            data = {
                'user': request.user.id,
                'class_instance': class_id
            }

            serializer = EnrolledSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                class_instance.currently_enrolled += 1
                class_instance.save()

            return Response({
                "msg": "Successfully Enrolled" 
            }, status=200)
        else:
            return Response({"msg" : "Doens't work"}, status=404)


class DropAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, studio_id, class_id):
        if not ClassInstances.objects.filter(parent_class=class_id).exists:
            return Response({"msg" : "Class doesn't exist"}, status=404)

        print(class_id, request.user.id)
        enrolled_instance = Enrolled.objects.filter(class_instance=class_id, user = request.user.id)
        print(enrolled_instance)
        if enrolled_instance.exists():
            enrolled_instance.delete()

            # subract currently enrolled
            class_instance = get_object_or_404(ClassInstances, pk=class_id)
            class_instance.currently_enrolled -= 1
            class_instance.save() 

            return Response({
                "msg": "Successfully dropped" 
            }, status=200)
        else: 
            return Response({
                "msg": "Not enrolled" 
            }, status=404)


class ClassSearchAPIView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = ClassInstancesSerializer
    queryset = ''
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        start = request.GET.get('start') or None
        end = request.GET.get('end') or None
        starttime = request.GET.get('starttime') or None
        endtime = request.GET.get('endtime') or None

        results = client.perform_search(query, start=start, end=end, starttime=starttime, endtime=endtime)
        page = self.paginate_queryset(results['hits'])
        return self.get_paginated_response(page)

class_search_view = ClassSearchAPIView.as_view()

class EnrolMultipleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes= [permissions.IsAuthenticated]

    def post(self, request, studio_id, class_id):
        class_instance = get_object_or_404(ClassInstances, pk=class_id)

        if not get_object_or_404(RegisterUser, user=request.user.id).subscribed:
            return Response({"msg" : "not subscribed"}, status=404)

        if get_object_or_404(SubscriptionInstance, user=request.user.id).renewal_date < class_instance.class_date:
            return Response({"msg" : "subscription will be expired before the class, please enrol after your subscription is renewed or subscribe to a longer subscription"}, status=404)

        curr_time = datetime.datetime.now().time()
        today = datetime.date.today()

        all_class_instances = ClassInstances.objects.filter(parent_class = class_instance.parent_class)

        for class_instance in all_class_instances:
            # Can't already be enrolled
            if Enrolled.objects.filter(class_instance = class_instance.pk, user = request.user.id).exists():
                continue
            if class_instance.currently_enrolled < class_instance.capacity and class_instance.class_date >= today:
                if class_instance.class_date == today and class_instance.start_time <= curr_time:
                    continue
            if get_object_or_404(SubscriptionInstance, user=request.user.id).renewal_date < class_instance.class_date:
                continue
            
            data = {
                'user': request.user.id,
                'class_instance': class_instance.pk
            }

            serializer = EnrolledSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                class_instance.currently_enrolled += 1
                class_instance.save()

        return Response({
            "msg": "Successfully enrolled to all future occurrences" 
        }, status=200)

class DropMultipleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, studio_id, class_id):
        if not ClassInstances.objects.filter(parent_class=class_id).exists:
            return Response({"msg" : "Class doesn't exist"}, status=404)
        
        class_instance = get_object_or_404(ClassInstances, pk=class_id)

        all_class_instances = ClassInstances.objects.filter(parent_class = class_instance.parent_class)

        for class_instance in all_class_instances:
            enrolled_instance = Enrolled.objects.filter(class_instance=class_instance.pk, user = request.user.id)
        
            if enrolled_instance.exists():
                enrolled_instance.delete()

                class_instance_object = get_object_or_404(ClassInstances, pk=class_instance.pk)
                class_instance_object.currently_enrolled -= 1
                class_instance_object.save() 

        return Response({
            "msg": "Successfully dropped all future occurrences" 
        }, status=200)
