# 导入Django和DRF相关模块
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

from api import models  # 导入自定义的模型


# Create your views here.


# CBV
# 序列化器


# 序列化器：用于将模型数据序列化为JSON格式
# 三个序列化器类，分别对应三个模型（UserInfo、BusInfo、TicketInfo）
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


# 用户认证类，用于验证用户登录信息
class Authenticate:
    def authenticate(self, name, password):
        # 根据用户名获取用户对象
        user = models.UserInfo.objects.get(name=name)
        if user:
            # 使用UserInfoSerializer进行用户信息序列化
            serializer = UserInfoSerializer(instance=user, many=False)
            # 检查密码是否匹配
            if check_password(password, serializer.data["password"]):
                return user
            else:
                return None
        else:
            return None


# 权限检查类，用于验证请求是否携带有效的访问令牌
class Permission_check:
    def check(self, request):
        url = "/your-token-verify-url/"
        data = {"token": request.headers["token"]}
        factory = APIRequestFactory()
        # 构造POST请求
        request = factory.post(url, data, format="json")
        # 创建TokenVerifyView视图对象
        view = TokenVerifyView.as_view()
        # 发送验证请求，根据响应的状态码判断令牌是否有效
        response = view(request)
        # 根据响应的状态码判断令牌是否有效
        if response.status_code == 200:
            # 令牌有效，继续你的逻辑
            return True
        else:
            # 令牌无效，返回错误信息
            return False


# 查询所有用户信息的视图类
class CheckUserInfo(APIView):
    def get(self, request):
        # 实例化权限检查对象
        a = Permission_check()
        # 如果用户未通过权限检查，返回未经授权的消息
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        # 查询所有用户信息
        logger.debug(request.user)
        user_list = models.UserInfo.objects.all()
        # 使用UserInfoSerializer进行序列化
        serializer = UserInfoSerializer(instance=user_list, many=True)
        # 返回序列化后的数据
        return Response(serializer.data)


# 用户注册的视图类
class User_register(APIView):
    def post(self, request):
        # 如果请求数据中包含密码，则对密码进行加密
        if "password" in request.data:
            request.data["password"] = make_password(request.data["password"], None, "pbkdf2_sha256")
        else:
            # 如果没有提供密码，返回错误信息
            return JsonResponse({"msg": "Password is needed", "code": 400}, status=400)
        # 使用UserInfoSerializer进行数据序列化
        serializer = UserInfoSerializer(data=request.data)
        # 校验数据是否有效
        if serializer.is_valid():
            # 保存用户信息
            serializer.save()
            return JsonResponse({"msg": "register success", "code": 200}, status=200)
        else:
            # 返回序列化错误信息
            response = Response(serializer.errors)
            response.status_code = 400
            return response


# 用户登录的视图类
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("name")
        password = request.data.get("password")
        # 实例化认证对象
        a = Authenticate()
        # 调用认证方法验证用户信息
        user = a.authenticate(name=username, password=password)

        if user:
            # 如果认证成功，生成访问令牌，并返回用户信息和令牌
            serializer = UserInfoSerializer(instance=user, many=False)
            access = AccessToken.for_user(user)
            data = {"access_token": str(access), "id": serializer.data["id"], "name": serializer.data["name"],
                    "is_admin": serializer.data["is_admin"]}
            return Response(data)
        else:
            # 认证失败，返回错误信息
            return Response({"error": "Invalid credentials"}, status=401)


# 操作一个用户的视图类
class UserDetailView(APIView):
    # 查询一个用户的信息
    def get(self, request, username):
        # 实例化权限检查对象
        a = Permission_check()
        # 如果用户未通过权限检查，返回未经授权的消息
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        # 查询用户信息
        user = models.UserInfo.objects.get(name=username)
        # 使用UserInfoSerializer进行序列化
        user_data = UserInfoSerializer(instance=user, many=False).data
        # 不返回密码信息
        user_data.pop("password")
        return Response(user_data)

    # 更新用户信息
    def put(self, request, username):
        # 实例化权限检查对象
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        # 查询需要更新的用户信息
        update_userinfo = models.UserInfo.objects.get(name=username)
        # 如果请求数据中包含密码，则对密码进行加密
        if "password" in request.data:
            request.data["password"] = make_password(request.data["password"], None, "pbkdf2_sha256")
        # 使用UserInfoSerializer进行数据序列化
        serializer = UserInfoSerializer(instance=update_userinfo, data=request.data, partial=True)

        if serializer.is_valid():
            # 保存更新后的用户信息
            serializer.save()
            update_user = UserInfoSerializer(instance=update_userinfo, many=False)
            user = models.UserInfo.objects.get(id=update_user.data['id'])
            # 使用UserInfoSerializer进行序列化
            user_data = UserInfoSerializer(instance=user, many=False).data
            # 不返回密码信息
            user_data.pop("password")
            return Response(user_data)

        else:
            # 返回序列化错误信息
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
        # 查询需要删除的用户信息
        the_user = models.UserInfo.objects.filter(name=username)
        if len(the_user) == 0:
            response = Response("没有这个用户")
            response.status_code = 400
            return response
        else:
            user_info = UserInfoSerializer(instance=the_user.first(), many=False)
            # 查询用户关联的车票信息
            ticket_list = models.TicketInfo.objects.filter(u_id=user_info.data["id"])
            logger.info(ticket_list)
            ticket_info_list = TicketInfoSerializer(instance=ticket_list, many=True)
            logger.info(ticket_info_list.data)
            # 删除用户关联的车票信息
            for ticket in ticket_info_list.data:
                a = TicketDetailView()
                a.delete(request, ticket["id"])
            # 删除用户信息
            the_user.delete()
            response = Response("SUCCESS")
            response.status_code = 400
            return response


# 查询所有汽车信息的视图类
class CheckBusInfo(APIView):
    def get(self, request):
        bus_list = models.BusInfo.objects.all()

        serializer = BusInfoSerializer(instance=bus_list, many=True)
        return Response(serializer.data)


# 车次注册的视图类
class Bus_register(APIView):
    def post(self, request):
        # 实例化权限检查对象
        serializer = BusInfoSerializer(data=request.data)
        # 如果用户未通过权限检查，返回未经授权的消息
        if serializer.is_valid():
            # 保存车次信息
            serializer.save()
            return Response(serializer.data)
        else:
            # 返回序列化错误信息
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


# 操作车次和用户关系的类
class operate_bus_users:
    # 添加用户到车次（原子操作）
    @transaction.atomic
    def add_users(self, b_id):
        # 获取需要更新的车次信息（原子操作）
        update_businfo = models.BusInfo.objects.select_for_update().get(id=b_id)
        # 使用BusInfoSerializer进行数据序列化
        bus_serializer = BusInfoSerializer(instance=update_businfo, many=False).data
        # 剩余座位数减一
        bus_serializer["remained_seats"] = bus_serializer["remained_seats"] - 1
        # 使用BusInfoSerializer进行数据序列化
        logger.info(bus_serializer["remained_seats"])
        new_bus_serializer = BusInfoSerializer(instance=update_businfo, data=bus_serializer)
        # 校验数据是否有效，并检查剩余座位是否合理
        if new_bus_serializer.is_valid() and bus_serializer["remained_seats"] <= bus_serializer["seats"]:
            # 保存更新后的车次信息
            new_bus_serializer.save()
            return Response(new_bus_serializer.data)
        else:
            # 返回序列化错误信息或剩余座位超额的错误信息
            if bus_serializer["remained_seats"] <= bus_serializer["seats"]:
                response = Response(new_bus_serializer.errors)
            else:
                response = Response("剩余座位超过额定座位")
            response.status_code = 400
            return response

    # 从车次中删除用户（原子操作）
    @transaction.atomic
    def delete_users(self, b_id):
        # 获取需要更新的车次信息（原子操作）
        update_businfo = models.BusInfo.objects.select_for_update().get(id=b_id)
        # 使用BusInfoSerializer进行数据序列化
        bus_serializer = BusInfoSerializer(instance=update_businfo, many=False).data
        # 剩余座位数加一
        bus_serializer["remained_seats"] = bus_serializer["remained_seats"] + 1
        new_bus_serializer = BusInfoSerializer(instance=update_businfo, data=bus_serializer)
        # 校验数据是否有效，并检查剩余座位是否合理
        if new_bus_serializer.is_valid() and bus_serializer["remained_seats"] <= bus_serializer["seats"]:
            new_bus_serializer.save()
            return Response(new_bus_serializer.data)
        else:
            # 返回序列化错误信息或剩余座位超额的错误信息
            if bus_serializer["remained_seats"] <= bus_serializer["seats"]:
                response = Response(new_bus_serializer.errors)
            else:
                response = Response("剩余座位超过额定座位")
            response.status_code = 400
            return response


# 查询同一用户所有车票信息的视图类
class CheckUserTicketInfo(APIView):
    def get(self, request, u_id):
        # 权限检查
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        # 查询特定用户的所有车票信息
        ticket_list = models.TicketInfo.objects.filter(u_id=u_id)
        # 使用TicketInfoSerializer进行数据序列化
        serializer = TicketInfoSerializer(instance=ticket_list, many=True)
        # 为每张车票添加关联的汽车信息
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


# 车票注册
class Ticket_register(APIView):
    def post(self, request):
        # 权限检查
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        serializer = TicketInfoSerializer(data=request.data)
        # 校验数据
        if serializer.is_valid():
            a = operate_bus_users()
            response = a.add_users(b_id=request.data["b_id"])
            # 如果添加用户到车次的操作失败，直接返回错误响应
            if response.status_code == 400:
                return response
            # 保存车票信息
            serializer.save()
            return Response(serializer.data)
        else:
            response = Response(serializer.errors)
            response.status_code = 400
            return response


# 操作一个车票的视图类
class TicketDetailView(APIView):
    # 查询一个车票
    def get(self, request, t_id):
        # 权限检查
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        bus = models.TicketInfo.objects.get(id=t_id)
        # 使用TicketInfoSerializer进行数据序列化
        serializer = TicketInfoSerializer(instance=bus, many=False)
        return Response(serializer.data)

    # 更新车次信息（更改状态）
    def put(self, request, t_id):
        #权限检查
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        update_ticketinfo = models.TicketInfo.objects.get(id=t_id)
        # 使用TicketInfoSerializer进行数据序列化
        serializer = TicketInfoSerializer(instance=update_ticketinfo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            check_ticketinfo = models.TicketInfo.objects.get(id=t_id)
            ticket_info = TicketInfoSerializer(instance=check_ticketinfo, many=False).data
            # 如果车票状态为已完成、已退款或已失效，则调用删除用户从车次中的方法
            if ticket_info["status"] == "F" or ticket_info["status"] == "T" or ticket_info["status"] == "I":
                a = operate_bus_users()
                response = a.delete_users(b_id=ticket_info["b_id"])
                if response.status_code == 400:
                    return response
            return Response(serializer.data)

        else:
            response = Response(serializer.errors)
            response.status_code = 400
            return response

    # 删除车票信息的视图方法
    def delete(self, request, t_id):
        # 权限检查
        a = Permission_check()
        if not a.check(request):
            response = Response("unauthenticated users")
            response.status_code = 401
            return response
        # 获取车票关联的车次ID
        ticket_model = models.TicketInfo.objects.get(id=t_id)

        ticket_info = TicketInfoSerializer(instance=ticket_model, many=False).data
        b_id = ticket_info["b_id"]
        a = operate_bus_users()
        # 调用删除用户从车次中的方法
        response = a.delete_users(b_id=b_id)
        if response.status_code == 400:
            return response
        ticket_model.delete()
        return Response("Success")
