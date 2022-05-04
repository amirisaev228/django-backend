from rest_framework.decorators import api_view

from .models import Genre, Book, Order

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    GenreSerializer, BookSerializer, OrderSerializer,
)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def genres(request):
    try:
        return Response(GenreSerializer(Genre.objects.all(), many=True).data, status=status.HTTP_200_OK)
    except:
        return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def genre(request, id):
    try:
        return Response(GenreSerializer(Genre.objects.get(id=id)).data, status=status.HTTP_200_OK)
    except:
        return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def books_by_genre(request, id):
    try:
        genre = Genre.objects.get(id=id)
        return Response(BookSerializer(genre.book_set.all(), many=True).data, status=status.HTTP_200_OK)
    except:
        return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BooksView(APIView):
    def get(self, request):
        try:
            return Response(BookSerializer(Book.objects.all(), many=True).data, status=status.HTTP_200_OK)
        except:
            return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        genre = Genre.objects.get(name=request.data.get('genre'))
        Book.objects.create(
            name=request.data.get('name'),
            genre=genre,
            author=request.data.get('author'),
            description=request.data.get('description'),
            image=request.data.get('image'),
            price=request.data.get('price')
        )

        return Response({"": ""}, status=status.HTTP_201_CREATED)


class BookDetailedView(APIView):
    def get(self, request, id):
        try:
            return Response(BookSerializer(Book.objects.get(id=id)).data, status=status.HTTP_200_OK)
        except:
            return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'GET'])
def order_book(request):
    if request.method == 'POST':
        book = Book.objects.get(id=request.data.get('book'))
        Order.objects.create(
            name = request.data.get('name'),
            status = request.data.get('status'),
            phone = request.data.get('phone'),
            address = request.data.get('address'),
            book = book
        )
        return Response({"":""}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        return Response(OrderSerializer(Order.objects.all(), many=True).data, status=status.HTTP_200_OK)


class OrderInfo(APIView):
    def get(self,request, id):
        return Response(OrderSerializer(Order.objects.get(id=id)).data, status=status.HTTP_200_OK)

    def put(self,request, id):
        order = Order.objects.get(id=id)
        order.status = request.data.get('status')
        order.save()
        return Response({"":""}, status=status.HTTP_200_OK)

    def delete(self,request,id):
        order = Order.objects.get(id=id)
        order.delete()
        return Response({"":""}, status=status.HTTP_200_OK)
