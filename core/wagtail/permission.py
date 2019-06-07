from wagtail.contrib.modeladmin.helpers import PagePermissionHelper


class OwnerPermissionHelper(PagePermissionHelper):
    """admin can see all, normal user can only see their own"""

    def user_can_list(self, user):
        if user.is_admin():
            return True
        return False

    def user_can_edit_obj(self, user, obj):
        if user.is_admin():
            return True
        return obj.owner == user

    def user_can_delete_obj(self, user, obj):
        if user.is_admin():
            return True
        return obj.owner == user
