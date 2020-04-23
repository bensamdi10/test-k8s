from content.models import Comment, CommentResponse
import base64
import sys, zipfile, os, os.path, re
from django.core.files.base import ContentFile
from django.conf import settings
import uuid

class CategoryUtils:


    def generateUID(self):
        return str(uuid.uuid4())[:8]



    def save(self, request, data, comment_object=None):

        if comment_object == None:
            comment = Comment()
            uid = self.generateUID()
            comment.uid = uid
        else:
            comment = comment_object

        comment.message = data["message"]
        comment.name_user = data["name_user"]
        comment.email_user = data["email_user"]
        comment.status = "pending"

        comment.save()

        return {"status": "success", "message": "Tag saved"}


    def update(self, request, data, commet):
        return self.save(request, data, commet)


    def getComment(self, uid):
        comment = Comment.objects.all().filter(uid=uid)
        if comment.count() == 1:
            return comment[0]
        else:
            return None

    def saveResponse(self, request, data, response_object=None):

        if response_object == None:
            response = CommentResponse()
            uid = self.generateUID()
            response.uid = uid
        else:
            response = response_object

        response.message = data["message"]
        response.name_user = data["name_user"]
        response.email_user = data["email_user"]
        response.status = "pending"
        comment_parent = self.getComment(data["comment_parent"])
        if not comment_parent == None:
            response.comment = comment_parent
            response.save()
            return {"status": "success", "message": "Tag saved"}
        else:
            return {"status": "error", "message": "error for parent comment"}


    def updateResponse(self, request, data, response):
        return self.saveResponse(request, data, response)

