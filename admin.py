from django.contrib import admin

# Register your models here.
from .models import Mail
import copy
from django.contrib import admin
from .models import (MailServiceProvider,
                     MailTemplate,
                     MailUser,
                     MailRecord)
from DjiStudio.utils import (MyAdmin,
                             get_model_field_names,
                             request_user_is_in_permit_groups)


@admin.register(MailUser)
class MailUserAdmin(MyAdmin):
    list_display = get_model_field_names(model=MailUser)


@admin.register(MailServiceProvider)
class MailServiceProviderAdmin(MyAdmin):
    list_display = get_model_field_names(model=MailServiceProvider)


@admin.register(MailRecord)
class MailRecordAdmin(MyAdmin):
    list_display = get_model_field_names(model=MailRecord)




@admin.register(MailTemplate)
class MailTemplateAdmin(MyAdmin):
    filter_horizontal = ['receieve_groups', ]
    list_display = get_model_field_names(model=MailTemplate,
                                         except_names=['receieve_groups', ])
    hide_fields = ["slug", "is_html", ]
    not_hide_group_names = ["大疆管理员", ]

    def get_fields(self, request, obj=None):
        fields = copy.deepcopy(super(MailTemplateAdmin, self).get_fields(request, obj=obj))
        if not request_user_is_in_permit_groups(request.user, self.not_hide_group_names):
            if not request.user.is_superuser:
                for hide_field in self.hide_fields:
                    if hide_field in fields:
                        fields.remove(hide_field)

        return fields

    def get_list_display(self, request):
        list_display = copy.deepcopy(self.list_display)
        if not request_user_is_in_permit_groups(request.user, self.not_hide_group_names):
            if not request.user.is_superuser:
                for hide_field in self.hide_fields:
                    if hide_field in list_display:
                        list_display.remove(hide_field)

        return list_display


class MailAdmin(MyAdmin):
    list_display = get_model_field_names(Mail)

admin.site.register(Mail, MailAdmin)
