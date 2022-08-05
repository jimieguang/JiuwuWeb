from django.contrib import admin

# Register your models here.
from userIssue.models import User, PrivateMessage
from goodsIssue.models import Goodsissue, MessageCompose, MessageComment

admin.site.register(Goodsissue)
admin.site.register(MessageCompose)
admin.site.register(MessageComment)
admin.site.register(User)
admin.site.register(PrivateMessage)



