from loguru import logger
from django.db import transaction
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenVerifyView
from django.contrib.auth.hashers import make_password, check_password

from api import models

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
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        logger.debug(request.user)
        user_list = models.UserInfo.objects.all()

        serializer = UserInfoSerializer(instance=user_list, many=True)
        return Response(serializer.data)


# 用户注册
class User_register(APIView):
    def post(self, request):
        if "password" in request.data:
            request.data["password"] = make_password(request.data["password"], None, "pbkdf2_sha256")
        else:
            return JsonResponse({"msg": "Password is needed", "code": 400}, status=400)
        serializer = UserInfoSerializer(data=request.data)
        # 校验数据
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"msg": "register success", "code": 200}, status=200)
        else:
            response = Response(serializer.errors)
            response.status_code = 400
            return response


class Authenticate:
    def authenticate(self, name, password):
        user = models.UserInfo.objects.get(name=name)
        if user:
            serializer = UserInfoSerializer(instance=user, many=False)
            if check_password(password, serializer.data["password"]):
                return user
            else:
                return None
        else:
            return None


class Permission_check:
    def check(self, request):
        url = "/your-token-verify-url/"
        data = {"token": request.headers["token"]}
        factory = APIRequestFactory()
        request = factory.post(url, data, format="json")
        # 根据响应的状态码判断令牌是否有效
        view = TokenVerifyView.as_view()
        response = view(request)
        if response.status_code == 200:
            # 令牌有效，继续你的逻辑
            return True
        else:
            # 令牌无效，返回错误信息
            return False


# 用户登录
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("name")
        password = request.data.get("password")

        a = Authenticate()
        user = a.authenticate(name=username, password=password)

        if user:
            serializer = UserInfoSerializer(instance=user, many=False)
            access = AccessToken.for_user(user)
            data = {"access_token": str(access), "id": serializer.data["id"], "name": serializer.data["name"],
                    "is_admin": serializer.data["is_admin"]}
            return Response(data)
        else:
            return Response({"error": "Invalid credentials"}, status=401)


# 操作一个用户
class UserDetailView(APIView):
    # authentication_classes = []
    # 查询一个用户
    def get(self, request, username):
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        user = models.UserInfo.objects.get(name=username)
        user_data = UserInfoSerializer(instance=user, many=False).data
        user_data.pop("password")
        return Response(user_data)

    # 更新用户信息
    def put(self, request, username):
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        update_userinfo = models.UserInfo.objects.get(name=username)
        # 序列化器对象
        if "password" in request.data:
            request.data["password"] = make_password(request.data["password"], None, "pbkdf2_sha256")
        serializer = UserInfoSerializer(instance=update_userinfo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            update_user = UserInfoSerializer(instance=update_userinfo, many=False)
            user = models.UserInfo.objects.get(id=update_user.data['id'])
            user_data = UserInfoSerializer(instance=user, many=False).data
            user_data.pop("password")
            return Response(user_data)

        else:
            response = Response(serializer.errors)
            response.status_code = 400
            return response

    # 删除用户
    def delete(self, request, username):
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        the_user = models.UserInfo.objects.filter(name=username)
        if len(the_user) == 0:
            response = Response("没有这个用户")
            response.status_code = 400
            return response
        else:
            user_info = UserInfoSerializer(instance=the_user.first(), many=False)
            ticket_list = models.TicketInfo.objects.filter(u_id=user_info.data["id"])
            logger.info(ticket_list)
            ticket_info_list = TicketInfoSerializer(instance=ticket_list, many=True)
            logger.info(ticket_info_list.data)
            for ticket in ticket_info_list.data:
                a = TicketDetailView()
                a.delete(request, ticket["id"])
            the_user.delete()
            response = Response("SUCCESS")
            response.status_code = 400
            return response


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
            response = Response(serializer.errors)
            response.status_code = 400
            return response


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
        serializer = BusInfoSerializer(instance=update_businfo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            response = Response(serializer.errors)
            response.status_code = 400
            return response

    # 删除车次
    def delete(self, request, b_id):
        models.BusInfo.objects.filter(id=b_id).delete()
        return Response("Success")


class operate_bus_users:
    @transaction.atomic
    def add_users(self, b_id):
        update_businfo = models.BusInfo.objects.select_for_update().get(id=b_id)
        bus_serializer = BusInfoSerializer(instance=update_businfo, many=False).data
        bus_serializer["remained_seats"] = bus_serializer["remained_seats"] - 1
        logger.info(bus_serializer["remained_seats"])
        new_bus_serializer = BusInfoSerializer(instance=update_businfo, data=bus_serializer)
        if new_bus_serializer.is_valid() and bus_serializer["remained_seats"] <= bus_serializer["seats"]:
            new_bus_serializer.save()
            return Response(new_bus_serializer.data)
        else:
            if bus_serializer["remained_seats"] <= bus_serializer["seats"]:
                response = Response(new_bus_serializer.errors)
            else:
                response = Response("剩余座位超过额定座位")
            response.status_code = 400
            return response

    @transaction.atomic
    def delete_users(self, b_id):
        update_businfo = models.BusInfo.objects.select_for_update().get(id=b_id)
        bus_serializer = BusInfoSerializer(instance=update_businfo, many=False).data
        bus_serializer["remained_seats"] = bus_serializer["remained_seats"] + 1
        new_bus_serializer = BusInfoSerializer(instance=update_businfo, data=bus_serializer)
        if new_bus_serializer.is_valid() and bus_serializer["remained_seats"] <= bus_serializer["seats"]:
            new_bus_serializer.save()
            return Response(new_bus_serializer.data)
        else:
            if bus_serializer["remained_seats"] <= bus_serializer["seats"]:
                response = Response(new_bus_serializer.errors)
            else:
                response = Response("剩余座位超过额定座位")
            response.status_code = 400
            return response


# 查询所有同一用户车票信息
class CheckUserTicketInfo(APIView):
    def get(self, request, u_id):
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        ticket_list = models.TicketInfo.objects.filter(u_id=u_id)

        serializer = TicketInfoSerializer(instance=ticket_list, many=True)
        for ticket in serializer.data:
            bus = models.BusInfo.objects.get(id=ticket["b_id"])
            bus_serializer = BusInfoSerializer(instance=bus, many=False)
            ticket["bus_info"] = bus_serializer.data
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
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        serializer = TicketInfoSerializer(data=request.data)
        # 校验数据
        if serializer.is_valid():
            # new_user = models.UserInfo.objects.create(**serializer.validated_data)
            a = operate_bus_users()
            response = a.add_users(b_id=request.data["b_id"])
            if response.status_code == 400:
                return response
            serializer.save()
            return Response(serializer.data)
        else:
            response = Response(serializer.errors)
            response.status_code = 400
            return response


# 操作一个车票
class TicketDetailView(APIView):
    # 查询一个车票
    def get(self, request, t_id):
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        bus = models.TicketInfo.objects.get(id=t_id)
        serializer = TicketInfoSerializer(instance=bus, many=False)
        return Response(serializer.data)

    # 更新车次信息（更改状态）
    def put(self, request, t_id):
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        update_ticketinfo = models.TicketInfo.objects.get(id=t_id)
        # 序列化器对象
        serializer = TicketInfoSerializer(instance=update_ticketinfo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            check_ticketinfo = models.TicketInfo.objects.get(id=t_id)
            ticket_info = TicketInfoSerializer(instance=check_ticketinfo, many=False).data
            if ticket_info["status"] == "F" or ticket_info["status"] == "T" or ticket_info["status"] == "I":
                a = operate_bus_users()
                response = a.delete_users(b_id=request.data["b_id"])
                if response.status_code == 400:
                    return response
            return Response(serializer.data)

        else:
            response = Response(serializer.errors)
            response.status_code = 400
            return response

    # 删除车票信息
    def delete(self, request, t_id):
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        ticket_model = models.TicketInfo.objects.get(id=t_id)

        ticket_info = TicketInfoSerializer(instance=ticket_model, many=False).data
        b_id = ticket_info["b_id"]
        a = operate_bus_users()
        response = a.delete_users(b_id=b_id)
        if response.status_code == 400:
            return response
        ticket_model.delete()
        return Response("Success")
