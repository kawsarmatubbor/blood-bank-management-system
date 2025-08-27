from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from . import models
import uuid

class RegistrationViewSet(APIView):
    def get(self, request):
        return Response({
            "message" : "Registration(GET)"
        })
    
    def post(self, request):
        serializer = serializers.RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = str(uuid.uuid4())
            models.Verification.objects.create(
                user = user,
                token = token
            )

            verification_url = f"http://127.0.0.1:8000/api/verification/{token}/"
            subject = "Verify your email address"
            message = f"Verification URL : {verification_url}"
            
            send_mail(
                subject=subject,
                message=message,
                from_email="kawsarmatubbordec@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response({
                "message" : "Please check your email to verify."
            })
        return Response(serializer.errors)
    
@api_view(['GET'])
def verification_view(request, token):
    try:
        verification = models.Verification.objects.get(token=token)
        user = verification.user
        user.is_active = True
        user.save()

        verification.delete()
        
        return Response({
            "success" : "Email verification successful."
        })
    
    except models.Verification.DoesNotExist:
        return Response({
            "error" : "Invalid token."
        })
    
    except models.CustomUser.DoesNotExist:
        return Response({
            "error" : "User does not exist."
        })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh = request.data.get('refresh')

        if not refresh:
            return Response({
                "error" : "Refresh token is required."
            })

        token = RefreshToken(refresh)
        token.blacklist()
        return Response({
            "success" : "Logout successful."
        })
    
    except:
        return Response({
            "error" : "Invalid token."
        })
    
class ProfileDetailViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.ProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = serializers.ProfileSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class BloodRequestViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        blood_requests = models.BloodRequest.objects.filter(is_active = True)
        serializer = serializers.BloodRequestSerializer(blood_requests, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.BloodRequestSerializer(data = request.data)
        if serializer.is_valid():
            user = request.user
            serializer.save(patient = user, blood_group = user.blood_group)
            return Response(serializer.data)
        return Response(serializer.errors)
    
class BloodRequestDetailViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            blood_request = models.BloodRequest.objects.get(pk = pk)
            serializer = serializers.BloodRequestSerializer(blood_request)
            return Response(serializer.data)
        
        except models.BloodRequest.DoesNotExist:
            return Response({
                "error" : "Request does not exist."
            })
        
    def put(self, request, pk):
        try:
            blood_request = models.BloodRequest.objects.get(pk = pk)
            serializer = serializers.BloodRequestSerializer(blood_request, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        
        except models.BloodRequest.DoesNotExist:
            return Response({
                "error" : "Request does not exist."
            })
        
class DonationViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        donations = models.Donation.objects.filter(donor = request.user)
        serializer = serializers.DonationSerializer(donations, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.DonationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class DonationDetailViewSet(APIView):
    def get(self, request, pk):
        try:
            donation = models.Donation.objects.get(pk = pk, donor = request.user)
            serializer = serializers.DonationSerializer(donation)
            return Response(serializer.data)
        
        except models.Donation.DoesNotExist:
            return Response({
                "error" : "Donation not found."
            })