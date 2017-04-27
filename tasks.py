# -*- coding: utf-8 -*-
"""
@file:      tasks.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.5
@editor:    Vim
@create:    4/6/17 6:33 PM
@description:

"""

from .utils import Email
from celery.task import task
from .models import MailTemplate, MailRecord, MailUser
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.utils import timezone
import time


@task
def unit_send_email(receiver_email, slug, kwargs):
    """使用邮件模板， 分离出收件人单元

    :param receiver_email: 收件人邮箱
    :param slug: 邮件模板索引
    :param kwargs: 模板中的变量数据集
    :return:
    """

    template = MailTemplate.objects.get(slug=slug)
    template.generate_template_variables(kwargs)
    print(template.body)

    email = Email(
        sender=template.sent_by.email_address,
        receiver=receiver_email,
        subject=template.title,
        content=template.body,
        subtype="html" if template.is_html else "plain",
        ssl=template.sent_by.service_provider.use_ssl
    )

    try:
        email.conn_server(template.sent_by.service_provider.host,
                          template.sent_by.service_provider.port)
        email.login(template.sent_by.email_address,
                    template.sent_by.password)
        email.send()
        email.close()
        success, res = True, "{} sent to {} OK!".format(template.title, receiver_email)
    except Exception as e:
        success, res = False, str(e)

    record = MailRecord.objects.create(
        to_email=receiver_email,
        sent_by=MailUser.objects.get(email_address=email.sender).__str__(),
        template_slug=template.slug,
        body=template.body,
        title=template.title,
        send_time=timezone.now(),
        success=success
    )

    if not success:
        record.err_msg = res

    record.save()

    return res


@task
def send_email(slug, kwargs):
    """使用邮件模板， 群发到抄送用户组

    :param slug: 邮件模板索引
    :param kwargs: 模板中的变量数据集
    :return:
    """

    template = MailTemplate.objects.get(slug=slug)
    for receive_django_user in User.objects.filter(
        Q(groups__in=template.receieve_groups.all()) |
        Q(username=kwargs['username'])
    ).distinct():
        receiver_email = receive_django_user.email
        unit_send_email.delay(receiver_email, slug, kwargs)
        time.sleep(3)