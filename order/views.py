from django.shortcuts import render
from rest_framework import status
# Create your views here.
import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order,Address
from cart.models import Cart,Cartitem
from rest_framework import generics
from .serializers import Addressserializer,Orderserializer
from product.models import Productvariant


class Addressview(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Addressserializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # If first address, mark as default
        if not Address.objects.filter(user=self.request.user).exists():
            serializer.save(user=self.request.user, is_default=True)
        else:
            serializer.save(user=self.request.user)

class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(user=self.request.user)
        address_id = request.data.get("address_id")
        address = Address.objects.get(id=address_id, user=request.user)
        amount = int(sum(item.product.price * item.quantity for item in cart.cartitem.all()) * 100)
        
        if amount< 100:
            return Response(
                {"detail": "Minimum order amount should be at least ₹1."},
                status=status.HTTP_400_BAD_REQUEST
    )
        # Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create Razorpay order
        razorpay_order = client.order.create({
            "amount": int(amount), 
            "currency": "INR", 
            "payment_capture": "1"
        })
         
        if hasattr(cart, "order"):
            return Response(
                {"detail": "Order already exists for this cart", "order_id": cart.order.id},
                status=400
            )
        # Save Order in DB
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            address=address,
            razorpay_order_id=razorpay_order["id"],
            amount=amount / 100  # store in rupees
        )

        return Response({
            "order_id": razorpay_order["id"],
            "amount": amount / 100,
            "currency": "INR",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        })


class VerifyPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"]
            })

            order = Order.objects.get(razorpay_order_id=data["razorpay_order_id"])
            order.razorpay_payment_id = data["razorpay_payment_id"]
            order.razorpay_signature = data["razorpay_signature"]
            order.is_paid = True
            order.save()
            order.cart.cartitem.all().delete()


            return Response({"status": "Payment successful"}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        

class DirectBuyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        address_id = request.data.get("address_id")

        # Fetch product variant
        try:
            product = Productvariant.objects.get(id=product_id)
        except Productvariant.DoesNotExist:
            return Response({"detail": "Product not found."}, status=404)

        # Check stock
        if quantity > product.stock:
            return Response(
                {"detail": f"Only {product.stock} items left in stock."},
                status=400
            )

        # Fetch user address
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({"detail": "Address not found."}, status=404)

        # Calculate amount in paise
        amount = int(product.price * quantity * 100)
        if amount < 100:
            return Response(
                {"detail": "Minimum order amount should be at least ₹1."},
                status=400
            )

        # Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create Razorpay order
        razorpay_order = client.order.create({
            "amount": amount, 
            "currency": "INR", 
            "payment_capture": "1"
        })

        # Save order in DB
        order = Order.objects.create(
            user=request.user,
            address=address,
            razorpay_order_id=razorpay_order["id"],
            amount=product.price * quantity
        )

        return Response({
            "order_id": razorpay_order["id"],
            "amount": product.price * quantity,
            "currency": "INR",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        })
