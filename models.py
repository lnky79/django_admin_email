from django.db import models
from UserProfile.models import UserProfile as User
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group


class MailServiceProvider(models.Model):
    name = models.CharField(max_length=30)
    host = models.CharField(max_length=50)
    port = models.IntegerField()
    use_ssl = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "邮件服务商"
        verbose_name_plural = "邮件服务商"


class MailUser(models.Model):
    name = models.CharField(verbose_name="昵称", max_length=50)
    email_address = models.EmailField(verbose_name="邮箱地址")
    password = models.CharField(max_length=50, verbose_name="秘钥")
    service_provider = models.ForeignKey(MailServiceProvider, verbose_name="服务商")

    def __str__(self):
        return self.name + ": " + self.email_address

    class Meta:
        verbose_name = "后台发信邮箱"
        verbose_name_plural = "后台发信邮箱"


class MailTemplate(models.Model):
    name = models.CharField(max_length=30, verbose_name="模板名")
    title = models.CharField(max_length=100, verbose_name="邮件标题")
    sent_by = models.ForeignKey(MailUser, verbose_name="后台发信邮箱")
    body = RichTextField(max_length=5000, verbose_name="邮件正文")
    to_user = models.BooleanField(default=False, verbose_name="用户通知邮件")
    to_admin = models.BooleanField(default=False, verbose_name="后台管理邮件")
    is_html = models.BooleanField(default=True, verbose_name="是html格式")
    slug = models.CharField(max_length=20, unique=True, null=True, verbose_name="模板索引slug")
    receieve_groups = models.ManyToManyField(Group, verbose_name="抄送到组", blank=True)

    def generate_template_variables(self, kwargs):
        for k, v in kwargs.items():
            self.body = self.body.replace("$(%s)" % (k), v)
            self.title = self.title.replace("$(%s)" % (k), v)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "邮件模板"
        verbose_name_plural = "邮件模板"


class MailRecord(models.Model):
    to_email = models.EmailField("收件人邮箱")
    sent_by = models.CharField("后台发件邮箱", max_length=50, null=True)
    template_slug = models.CharField("邮件模板", max_length=30)
    title = models.CharField("邮件标题", max_length=100, null=True)
    body = models.TextField("正文数据", max_length=255, null=True)
    send_time = models.DateTimeField("发送时间")
    success = models.BooleanField("发送成功", default=True)
    err_msg = models.TextField("异常消息", null=True)

    def __str__(self):
        return "{}`s {} mail ___ {}".format(self.to_email,
                                            self.template_slug,
                                            self.send_time.strftime("%Y-%m-%d %h:%M:%s"))

    class Meta:
        verbose_name = "邮件发送记录"
        verbose_name_plural = "邮件发送记录"


class Mail(models.Model):
    sender = models.ForeignKey(User, verbose_name='发送者')
    send_time = models.DateTimeField('发送时间', default=timezone.now)
    message = RichTextField('内容', max_length=1000)
    contact_phone = models.CharField('联系电话', max_length=20)
    contact_name = models.CharField('联系人', max_length=20)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = u'用户意见'
        verbose_name_plural = u'* 用户意见箱'
