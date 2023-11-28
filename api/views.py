from api import models
from loguru import logger
from rest_framework import serializers
from rest_framework.views import APIView
from django.shortcuts import HttpResponse
from rest_framework.response import Response

# Create your views here.


# CBV
# 序列化器


# 三个序列化器类
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.UserInfo


class BusInfoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.BusInfo


class TicketInfoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.TicketInfo


# 查询所有用户信息
class CheckUserInfo(APIView):
    def get(self, request):
        logger.debug(request.user)
        user_list = models.UserInfo.objects.all()

        serializer = UserInfoSerializer(instance=user_list, many=True)
        return Response(serializer.data)


# 用户注册
class User_register(APIView):
    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        # 校验数据
        if serializer.is_valid():
            # new_user = models.UserInfo.objects.create(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# 操作一个用户
class UserDetailView(APIView):
    # authentication_classes = []
    # 查询一个用户
    def get(self, request, username):
        user = models.UserInfo.objects.get(name=username)
        serializer = UserInfoSerializer(instance=user, many=False)
        return Response(serializer.data)

    # 更新用户信息
    def put(self, request, username):
        update_userinfo = models.UserInfo.objects.get(name=username)
        # 序列化器对象
        serializer = UserInfoSerializer(instance=update_userinfo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    # 删除用户
    def delete(self, request, username):
        the_user = models.UserInfo.objects.filter(name=username)
        if len(the_user) == 0:
            return HttpResponse("没有这个用户")
        else:
            the_user.delete()
            return Response("Success")


# 查询所有汽车信息
class CheckBusInfo(APIView):
    def get(self, request):
        bus_list = models.BusInfo.objects.all()

        serializer = BusInfoSerializer(instance=bus_list, many=True)
        return Response(serializer.data)


# 车次注册
class Bus_register(APIView):
    def post(self, request):
        serializer = BusInfoSerializer(data=request.data)
        # 校验数据
        if serializer.is_valid():
            # new_user = models.UserInfo.objects.create(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# 操作一个车次
class BusDetailView(APIView):
    # 查询一个车次
    def get(self, request, b_id):
        bus = models.BusInfo.objects.get(id=b_id)
        serializer = BusInfoSerializer(instance=bus, many=False)
        return Response(serializer.data)

    # 更新车次信息
    def put(self, request, b_id):
        update_businfo = models.BusInfo.objects.get(id=b_id)
        # 序列化器对象
        serializer = BusInfoSerializer(instance=update_businfo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    # 删除车次
    def delete(self, request, b_id):
        models.BusInfo.objects.filter(id=b_id).delete()
        return Response("Success")


# 查询所有同一用户车票信息
class CheckUserTicketInfo(APIView):
    def get(self, request, u_id):
        ticket_list = models.TicketInfo.objects.filter(u_id=u_id)

        serializer = TicketInfoSerializer(instance=ticket_list, many=True)
        return Response(serializer.data)


# 查询所有同一车次车票信息
class CheckBusTicketInfo(APIView):
    def get(self, request, b_id):
        ticket_list = models.TicketInfo.objects.filter(b_id=b_id)

        serializer = TicketInfoSerializer(instance=ticket_list, many=True)
        return Response(serializer.data)


# 车票注册(状态：S:'提交')
class Ticket_register(APIView):
    def post(self, request):
        serializer = TicketInfoSerializer(data=request.data)
        # 校验数据
        if serializer.is_valid():
            # new_user = models.UserInfo.objects.create(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# 操作一个车票
class TicketDetailView(APIView):
    # 查询一个车票
    def get(self, request, t_id):
        bus = models.TicketInfo.objects.get(id=t_id)
        serializer = TicketInfoSerializer(instance=bus, many=False)
        return Response(serializer.data)

    # 更新车次信息（更改状态）
    def put(self, request, t_id):
        update_ticketinfo = models.TicketInfo.objects.get(id=t_id)
        # 序列化器对象
        serializer = TicketInfoSerializer(instance=update_ticketinfo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    # 删除车票信息
    def delete(self, request, t_id):
        models.TicketInfo.objects.filter(id=t_id).delete()
        return Response("Success")
