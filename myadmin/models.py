from django.db import models
from datetime import datetime
#员工账号信息模型
class User(models.Model):
    username = models.CharField(max_length=50)    #员工账号
    nickname = models.CharField(max_length=50)    #昵称
    password_hash = models.CharField(max_length=100)#密码
    password_salt = models.CharField(max_length=50)    #密码干扰值
    status = models.IntegerField(default=1)    #状态:1正常/2禁用/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,
                'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "user"  # 更改表名

#店铺信息模型
class Shop(models.Model):
    name = models.CharField(max_length=255)         #店铺名称
    cover_pic = models.CharField(max_length=255)    #封面图片
    banner_pic = models.CharField(max_length=255)   #图标Logo
    address = models.CharField(max_length=255)      #店铺地址
    phone = models.CharField(max_length=255)        #联系电话
    status = models.IntegerField(default=1)         #状态:1正常/2暂停/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        shopname = self.name.split("-")
        return {'id':self.id,'name':shopname[0],'shop':shopname[1],'cover_pic':self.cover_pic,'banner_pic':self.banner_pic,'address':self.address,'phone':self.phone,
                'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "shop"  # 更改表名
#菜品分类信息模型
class Category(models.Model):
    shop_id = models.IntegerField()        #店铺id
    name = models.CharField(max_length=50,default='')#分类名称
    types = models.IntegerField()
    status = models.IntegerField(default=1)        #状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    class Meta:
        db_table = "category"  # 更改表名

#菜品信息模型
class Product(models.Model):
    shop_id = models.IntegerField()        #店铺id
    shop_name = models.CharField(max_length=45,default='')  # 店名
    category_id = models.IntegerField()    #菜品分类id
    cover_pic = models.CharField(max_length=50)    #菜品图片
    name = models.CharField(max_length=50)#菜品名称
    price = models.FloatField()    #菜品单价
    status = models.IntegerField(default=1)        #状态:1正常/2售罄/9下架
    is_special = models.IntegerField(default=0)  # 是否为特色菜   0不是/1是
    types = models.IntegerField(default=1)  # 是否为特色菜   0不是/1是
    sales = models.BigIntegerField(default=0)   # 累计销量
    info = models.CharField(max_length=50,default="   ") # 特点标签
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id':self.id,'shop_name':self.shop_name,'shop_id':self.shop_id,'category_id':self.category_id,'cover_pic':self.cover_pic,'name':self.name,'price':self.price,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "product"  # 更改表名

#会员信息模型
class Member(models.Model):
    nickname = models.CharField(verbose_name='您的昵称',max_length=50)    #昵称
    name = models.CharField(verbose_name='登录账号', max_length=128, unique=True)  # 网上昵称，有唯一性
    password_hash = models.CharField(max_length=100)  # 密码
    password_salt = models.CharField(max_length=50)  # 密码干扰值
    avatar = models.CharField(max_length=255)    #头像
    mobile = models.CharField(max_length=50)    #电话
    money = models.CharField(max_length=50,default='0')   # 账户余额
    cost = models.FloatField(default=0)   # 账户余额
    address = models.CharField(max_length=255,default="暂无")  # 常用地址
    is_vip = models.IntegerField(default=0)        # 是否会员 0不是/1是
    status = models.IntegerField(default=1)        #状态:1正常/2禁用/9删除
    email = models.EmailField(verbose_name='邮箱', unique=True)
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间
    introduce = models.TextField(verbose_name='个人简介', default="这个人太懒了，什么都没有留下")

    def toDict(self):
        return {'id':self.id,'nickname':self.nickname,'avatar':self.avatar,'mobile':self.mobile,'is_vip':self.is_vip,'introduce':self.introduce,"address":self.address,'name':self.name,'email':self.email,'money':self.money,
                'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "member"  # 更改表名

# 订单模型
class Orders(models.Model):
    name = models.CharField(max_length=45)  # 菜名
    shop_name = models.CharField(max_length=45,default='')  # 店名
    shop_id = models.IntegerField()   #店铺id号
    product_id = models.IntegerField()   #菜品id号
    member_id = models.IntegerField() #用户id
    # user_id = models.IntegerField()   #操作员id
    price = models.FloatField()     #单价
    num = models.IntegerField(default=0)     #数量
    status = models.IntegerField(default=1)   #订单状态:1过行中/2无效/3已完成
    whole_price = models.FloatField(default=0.0)
    payment_status = models.IntegerField(default=1)   #支付状态:1未支付/2已支付/3已退款
    create_at = models.DateTimeField(default=datetime.now)  #创建时间
    update_at = models.DateTimeField(default=datetime.now)  #修改时间

    class Meta:
        db_table = "orders"  # 更改表名


# 订单详情模型
class OrderDetail(models.Model):
    order_id = models.IntegerField()  #订单id
    product_id = models.IntegerField()  #菜品id
    product_name = models.CharField(max_length=50) #菜品名称
    price = models.FloatField()     #单价
    quantity = models.IntegerField()  #数量
    status = models.IntegerField(default=1) #状态:1正常/9删除

    class Meta:
        db_table = "order_detail"  # 更改表名


# 支付信息模型
class Payment(models.Model):
    order_id = models.IntegerField()  #订单id号
    member_id = models.IntegerField() #会员id
    money = models.FloatField()     #支付金额
    type = models.IntegerField()      #付款方式：1会员付款/2收银收款
    bank = models.IntegerField(default=1) #收款银行渠道:1微信/2余额/3现金/4支付宝
    status = models.IntegerField(default=1) #支付状态:1未支付/2已支付/3已退款
    create_at = models.DateTimeField(default=datetime.now)  #创建时间
    update_at = models.DateTimeField(default=datetime.now)  #修改时间

    class Meta:
        db_table = "payment"  # 更改表名
