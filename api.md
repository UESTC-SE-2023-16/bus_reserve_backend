## API文档

### 用户服务

****

#### 查看所有用户（token）

- URL：/user/getUserInfo/

- 请求方式：get

- **请求参数：**

  ```JSON
  {
  	"token":"XXX"
  }
  ```

  

- 返回结果：

| 字段 |       备注       |
| :--: | :--------------: |
| data | 返回用户信息序列 |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": [
        {
            "id": 1,
            "name": "admin",
            "password": "admin",
            "is_admin": true
        },
        {
            "id": 2,
            "name": "zhao",
            "password": "7846451",
            "is_admin": false
        }
    ]
}
```

#### 注册用户

- URL:/user/register/
- 请求方式：post
- 请求参数

|   字段   |   备注   | 是否必须 |
| :------: | :------: | :------: |
|   name   |  用户名  |    是    |
| password | 用户密码 |    是    |

- ~~返回结果：~~

|     字段     |         备注          |
| :----------: | :-------------------: |
|    ~~id~~    |  ~~自动生成自增id~~   |
|   ~~name~~   |       ~~名称~~        |
| ~~password~~ |       ~~密码~~        |
| ~~is_admin~~ | ~~固定为false，只读~~ |

```json
{
    "msg": "register success",
    "code": 200
}
```

插入失败：

（没有密码字段）

```json
{
    "msg": "Password is needed",
    "code": 400
}
```

（名称字段为空）

```json
{
    "msg": "请求成功",
    "code": 400,
    "data": {
        "name": [
            "This field may not be blank."
        ]
    }
}
```

#### 登录

url :/user/login/

请求方式：post

请求参数

| 字段     | 备注     | 是否必须 |
| -------- | -------- | -------- |
| name     | 用户名   | 是       |
| password | 用户密码 | 是       |

返回结果

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMTExNjAyLCJpYXQiOjE3MDIxMTA3MDIsImp0aSI6ImIzM2RjMDk0MjYzMjRiZjA5NjgwMjE5OTI1ZjQwOWEwIiwidXNlcl9pZCI6Mjl9.OvntNRI9Ql6w59rN85adhSZCRjoSbdlhgYledozzZ-s",
        "id": 29,
        "name": "asdf"
    }
}
```

登录失败（密码不正确）

```json
{
    "msg": "请求成功",
    "code": 401,
    "data": {
        "error": "Invalid credentials"
    }
}
```

登录失败（错误的用户名）

```json
{
    "msg": "服务器错误:UserInfo matching query does not exist.",
    "code": 500,
    "data": {}
}
```

#### 获取单个用户信息(token)

- url :/user/<str:username/>

  例如：

  ```http
  http://xxx.xxx:xxxx/user/GAO/
  ```

- 请求方式：get

- 参数

  ```json
  {
  	"token":"XXX"
  }
  ```

  

- 返回结果

|     字段     |      备注      |
| :----------: | :------------: |
|      id      | 自动生成自增id |
|     name     |      名称      |
| ~~password~~ |    ~~密码~~    |
|   is_admin   |   false/true   |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "id": 29,
        "name": "asdf",
        "is_admin": false
    }
}
```

查找失败(没有这个用户名)：

```json
{
    "msg": "服务器错误:UserInfo matching query does not exist.",
    "code": 500,
    "data": {}
}
```



#### 更新用户信息(token)

- url：/user/<str:username>/

- 例如：

  ```http
  http://xxx.xxx:xxxx/user/GAO/
  ```

- 请求方式：put

- 请求参数

|   字段    |   备注    | 是否必须 |
| :-------: | :-------: | :------: |
|   name    |  用户名   |    否    |
| password  | 用户密码  |    否    |
| **token** | **token** |  **是**  |

- 返回结果

|     字段     |      备注      |
| :----------: | :------------: |
|      id      | 自动生成自增id |
|     name     |      名称      |
| ~~password~~ |    ~~密码~~    |
|   is_admin   |   false/true   |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "id": 2,
        "name": "zhao1",
        "is_admin": false
    }
}
```

```json
{
    "msg": "请求成功",
    "code": 401,
    "data": "unauthenticated users"
}
```



#### 删除用户账户(token)

- url：/user/<str:username/>

- 例如：

  ```http
  http://xxx.xxx:xxxx/user/GAO/
  ```

- 请求方式：delete

- 请求参数

  ```json
  {
  	"token":"XXX"
  }
  ```

  

- 返回结果

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": "Success"
}
```

注意删除用户账户后对应的车票也被一并删除

### 车次管理

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### 查看所有车次

- URL：/bus/getBusInfo/
- 请求方式：get
- 请求参数：无

- 返回结果：

| 字段 |       备注       |
| :--: | :--------------: |
| data | 返回车次信息序列 |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": [
        {
            "id": 3,
            "busnum": "b19",
            "depart": "shanghai",
            "destination": "beijing",
            "departtime": "2022-09-07",
            "seats": 35,
            "remained_seats": 3,
            "fare": 20
        },
        {
            "id": 4,
            "busnum": "b17",
            "depart": "beijing",
            "destination": "shanghai",
            "departtime": "2022-09-11",
            "seats": 34,
            "remained_seats": 39,
            "fare": 20
        },
        {
            "id": 5,
            "busnum": "B23",
            "depart": "chengdu",
            "destination": "shanghai",
            "departtime": "2022-09-07",
            "seats": 35,
            "remained_seats": 35,
            "fare": 20
        },
        {
            "id": 6,
            "busnum": "b57",
            "depart": "chengdu",
            "destination": "shanghai",
            "departtime": "2022-09-07",
            "seats": 35,
            "remained_seats": 35,
            "fare": 20
        }
    ]
}
```

#### 注册车次

- URL:/bus/register/
- 请求方式：post
- 请求参数

|      字段      |   备注   |  是否必须  |
| :------------: | :------: | :--------: |
|     busnum     | 车辆编号 |     是     |
|     depart     |   始发   |     是     |
|  destination   |   终点   |     是     |
|   departtime   | 出发时间 |     是     |
|     seats      |   座位   | 否，默认35 |
| remained_seats | 剩余座位 | 否，默认35 |
|      fare      |   票价   | 否，默认20 |

- 返回结果：

|      字段      |      备注      |
| :------------: | :------------: |
|       id       | 自动生成自增id |
|     busnum     |    车辆编号    |
|     depart     |      始发      |
|  destination   |      终点      |
|   departtime   |    出发时间    |
|     seats      |      座位      |
| remained_seats |    剩余座位    |
|      fare      |      票价      |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "id": 6,
        "busnum": "b56",
        "depart": "chengdu",
        "destination": "shanghai",
        "departtime": "2022-09-07",
        "seats": 35,
        "remained_seats": 35,
        "fare":20
    }
}
```

插入失败(bus num不能重复)：

```json
{
    "msg": "请求成功",
    "code": 400,
    "data": {
        "busnum": [
            "bus info with this busnum already exists."
        ]
    }
}
```

插入失败(格式不正确，缺少busbum字段)：

```json
{
    "msg": "请求成功",
    "code": 400,
    "data": {
        "busnum": [
            "This field may not be blank."
        ]
    }
}
```



#### 获取单个车次信息

- url:/bus/<str:b_id>/

  例如：

  ```http
  http://xxx.xxx:xxxx/bus/2/
  ```

- 请求方式：get

- 无参数

- 返回结果

|      字段      |   备注   |
| :------------: | :------: |
|     busnum     | 车辆编号 |
|     depart     |   始发   |
|  destination   |   终点   |
|   departtime   | 出发时间 |
|     seats      |   座位   |
| remained_seats | 剩余座位 |
|      fare      |   票价   |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "id": 6,
        "busnum": "b56",
        "depart": "chengdu",
        "destination": "shanghai",
        "departtime": "2022-09-07",
        "seats": 35,
        "remained_seats": 35,
        "fare":20
    }
}
```

查找失败(没有这个车次id)：

```json
{
    "msg": "服务器错误:BusInfo matching query does not exist.",
    "code": 500,
    "data": {}
}
```



#### 更新车次信息

- url:/bus/<str:b_id>/

  例如：

  ```http
  http://xxx.xxx:xxxx/bus/2/
  ```

- 请求方式：put

- 请求参数

|      字段      |   备注   |     是否必须     |
| :------------: | :------: | :--------------: |
|     busnum     | 车辆编号 |        是        |
|     depart     |   始发   |        是        |
|  destination   |   终点   |        是        |
|   departtime   | 出发时间 |        是        |
|     seats      |   座位   | 否，不输入不改变 |
| remained_seats | 剩余座位 | 否，不输入不改变 |
|      fare      |   票价   | 否，不输入不改变 |

- 返回结果

|      字段      |      备注      |
| :------------: | :------------: |
|       id       | 自动生成自增id |
|     busnum     |    车辆编号    |
|     depart     |      始发      |
|  destination   |      终点      |
|   departtime   |    出发时间    |
|     seats      |      座位      |
| remained_seats |    剩余座位    |
|      fare      |      票价      |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "id": 6,
        "busnum": "b57",
        "depart": "chengdu",
        "destination": "shanghai",
        "departtime": "2022-09-07",
        "seats": 35,
        "remained_seats": 35,
        "fare":20
    }
}
```

更新失败（缺少字段）

```json
{
    "msg": "请求成功",
    "code": 400,
    "data": {
        "depart": [
            "This field is required."
        ]
    }
}
```



#### 删除车次

- url:/bus/<str:b_id>/

  例如：

  ```http
  http://xxx.xxx:xxxx/bus/2/
  ```

- 请求方式：delete

- 请求参数：无

- 返回结果

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": "Success"
}
```

注意删除车次后对应的车票也被一并删除

### 车票管理

------------------------------------------------------------------------------------------------------------------------------------

#### 车票状态表

| 状态符号 | 表示状态         |
| -------- | ---------------- |
| “S”      | 提交（未缴费）   |
| “N”      | 正常（已缴费）   |
| “F”      | 完成             |
| “T”      | 取消             |
| “I”      | 无效（其它情况） |

状态为S、N时占用1个座位

状态为F、T、I时不占用座位

#### 查看用户对应的车票(token)

- URL：ticket/getUserTicketInfo/<str:u_id>/

- 例如：

  ```http
  http://127.0.0.1:8000/ticket/getUserTicketInfo/2/
  ```

- 请求方式：get

- **请求参数**

  ```json
  {
  	"token":"XXX"
  }
  ```

  

- 返回结果：

| 字段 |       备注       |
| :--: | :--------------: |
| data | 返回车票信息序列 |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": [
        {
            "id": 2,
            "status": "S",
            "u_id": 2,
            "b_id": 3,
            "bus_info": {
                "id": 3,
                "busnum": "b19",
                "depart": "shanghai",
                "destination": "beijing",
                "departtime": "2022-09-07",
                "seats": 35,
                "remained_seats": 3,
                "fare":20
            }
        },
        {
            "id": 5,
            "status": "F",
            "u_id": 2,
            "b_id": 4,
            "bus_info": {
                "id": 4,
                "busnum": "b17",
                "depart": "beijing",
                "destination": "shanghai",
                "departtime": "2022-09-11",
                "seats": 34,
                "remained_seats": 39,
                "fare":20
            }
        }
    ]
}
```

#### 查看车次对应的车票

- URL：ticket/getBusTicketInfo/<str:b_id>/

- 例如：

  ```http
  http://127.0.0.1:8000/ticket/getBusTicketInfo/4/
  ```

- 请求方式：get

- 请求参数：无

- 返回结果：

| 字段 |       备注       |
| :--: | :--------------: |
| data | 返回车票信息序列 |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": [
        {
            "id": 4,
            "status": "S",
            "u_id": 2,
            "b_id": 4
        },
        {
            "id": 6,
            "status": "N",
            "u_id": 3,
            "b_id": 4
        }
    ]
}
```

#### 注册车票(token)

- URL:/ticket/register/
- 请求方式：post
- 请求参数

|   字段    |   备注    |                           是否必须                           |
| :-------: | :-------: | :----------------------------------------------------------: |
|   b_id    |  车辆id   |                 用户表外键，用户表中必须存在                 |
|   u_id    |  用户id   |                 车次表外键，车次表中必须存在                 |
|  status   |   状态    | **使用本接口时，设定为S（提交）、N（已支付）符合逻辑，不输入默认S** |
| **token** | **token** |                            **是**                            |

- 返回结果：

|  字段  |       备注        |
| :----: | :---------------: |
|   id   |  自动生成自增id   |
| status | 状态信息，默认为S |
|  u_id  |    用户表外键     |
|  b_id  |    车次表外键     |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "id": 7,
        "status": "S",
        "u_id": 19,
        "b_id": 4
    }
}
```

插入失败：

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "u_id": [
            "Invalid pk \"52\" - object does not exist."
        ]
    }
}
```



```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "u_id": [
            "This field may not be null."
        ]
    }
}
```

没有权限

```json
{
    "msg": "请求成功",
    "code": 401,
    "data": "unauthenticated users"
}
```



#### 获取单个车票信息(token)

- url:/ticket/<str:t_id>/

  例如：

  ```http
  http://127.0.0.1:8000/ticket/4/
  ```

- 请求方式：get

- 参数

  ```json
  {
  	"token":"XXX"
  }
  ```

- 返回结果

|  字段  |      备注      |
| :----: | :------------: |
|   id   | 自动生成自增id |
| status |    状态信息    |
|  u_id  |   用户表外键   |
|  b_id  |   车次表外键   |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "id": 4,
        "status": "T",
        "u_id": 2,
        "b_id": 4
    }
}
```

查找失败(没有这个车票id)：

```json
{
    "msg": "服务器错误:TicketInfo matching query does not exist.",
    "code": 500,
    "data": {}
}
```

没有权限：

```json
{
    "msg": "请求成功",
    "code": 401,
    "data": "unauthenticated users"
}
```



#### 更新车票信息（更改状态）(token)

对于状态的更新，如下的改变符合逻辑：

| 更改前状态  | 更改后状态                              |
| ----------- | --------------------------------------- |
| S（提交）   | N（已支付）、T（取消）、I（其它情况）   |
| N（已支付） | F（行程结束）、T（取消）、I（其它情况） |

- url:/ticket/<str:t_id>/

  例如：

  ```http
  http://127.0.0.1:8000/ticket/4/
  ```

- 请求方式：put

- 请求参数

|   字段    |   备注    |       是否必须       |
| :-------: | :-------: | :------------------: |
|   b_id    |  车辆id   |          否          |
|   u_id    |  用户id   |          否          |
|  status   |   状态    | 不必须，不输入不更改 |
| **token** | **token** |        **是**        |

- 返回结果

|  字段  |        备注        |
| :----: | :----------------: |
|   id   |   自动生成自增id   |
| status | 状态信息（已更改） |
|  u_id  |     用户表外键     |
|  b_id  |     车次表外键     |

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": {
        "id": 4,
        "status": "N",
        "u_id": 2,
        "b_id": 4
    }
}
```

更改失败（状态不在“SINFT”中）

```JSON
{
    "msg": "请求成功",
    "code": 400,
    "data": {
        "status": [
            "\"A\" is not a valid choice."
        ]
    }
}
```

没有权限：

```json
{
    "msg": "请求成功",
    "code": 401,
    "data": "unauthenticated users"
}
```



#### 删除车票（将车票从数据库中删除而不是标记为T：取消）(token)

- url:/ticket/<str:t_id>/

  例如：

  ```http
  http://127.0.0.1:8000/ticket/4/
  ```

- 请求方式：delete

- 请求参数

  ```json
  {
  	"token":"XXX"
  }
  ```

  

- 返回结果

```json
{
    "msg": "请求成功",
    "code": 200,
    "data": "Success"
}
```

没有权限：

```json
{
    "msg": "请求成功",
    "code": 401,
    "data": "unauthenticated users"
}
```



