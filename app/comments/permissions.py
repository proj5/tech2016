from rest_framework import permissions


class IsCommentOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, comment):
        if request.user:
            return comment.created_by.user == request.user
        return False
