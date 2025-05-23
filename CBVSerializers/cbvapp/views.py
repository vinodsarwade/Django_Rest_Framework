from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from cbvapp.models import Student
from cbvapp.serializers import StudentSerializer

#using class based view
from rest_framework.views import APIView
# using mixins ,generics
from rest_framework import generics, mixins
#using viewset
from rest_framework import viewsets

'''here we are using pagination locally in our class. but you can add it in setting.py globally, is uses default page_size for your project level.'''
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

####  using viewset ####
#using viewset you can write all your operations in a single class. 
#you can use this in urls by connecting routers to default router of rest_framework.
#and register your class with your class name.then use include to use all routers urls.

'''if you have to use this pagination class then add it in StudentViewSet class'''
# class StudentPagination(PageNumberPagination):
#     page_size = 4

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # pagination_class = StudentPagination 
    pagination_class = LimitOffsetPagination 



#######   using generics   ########
#in mixins we need to write just two classes but in which we need to write seperate methods for each request
# to avoid writting many methods we use generics in which we dont need to write any method just write  queryset and serializer_class
#it will auto handle request using ListCreateAPIView,RetrieveUpdateDestroyAPIView. it has many  more methods like
# ListAPIView,CreateAPIView,RetriveAPIView,DestroyAPIView,UpdateAPIView, RetriveUpdateAPIView, RetriveDestroyAPIView.
'''
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
'''


#####    using mixins     ######
#to avoid writing same code many times in class based view we use mixins. 
#mixins have many methods like ListModelMixin,CreateModelMixin for non primary key based operation
#and UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, for primary key based operation.
#in mixins we just need queryset object and serializer_class in which all the code internaly handle by mixins.
#then just need to write method and return the request back.
'''
class StudentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    
class StudentDetail(mixins.UpdateModelMixin, mixins.DestroyModelMixin,mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    def put(self, request, pk):
        return self.update(request, pk)
    def delete(self, request, pk):
        return self.destroy(request, pk)
'''


#######   class based views    #####
#in using cbv you need to write seperate classes for primary key and non primary key based operations.
#and write seperate methods to handle the each request, in this case we need to write more code.
'''
class StudentList(APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer= StudentSerializer(student, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = StudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class StudentDetail(APIView):
    def get_object(self, pk):
        try:
            student = Student.objects.get(pk=pk)
            return student
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        student = self.get_object(pk=pk)
        serializer = StudentSerializer(student, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''