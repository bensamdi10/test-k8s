# -*- coding: utf-8 -*-


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from account.models import Profil
from django.contrib.auth.models import User
import datetime
from datetime import datetime
import time
import uuid
from .forms import ProfilForm, LoginForm, PasswordForm, ForgetPasswordForm, EditProfilForm, AboutProfilForm, SecuityProfilForm, AuthorForm
from project_infra.template_view_custom import TemplateViewCustom
from project_infra.template_view_site import TemplateViewSite
import base64
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.html import strip_tags

# Create your views here.

# CREATE PAGES
class CreateProfil(TemplateViewCustom):
    template_name = "create_profil.html"
    login = False

    def get(self, request):
        form = ProfilForm
        from_invitaion =  request.GET.get('from-invitation')
        token_invitation =  request.GET.get('token')


        if from_invitaion == None :
            return render(request, self.template_name,{"form": form})
        else :
            profil_temp = Profil.objects.filter(token_invitation=token_invitation)
            if len(profil_temp) == 0:
                return redirect('/account/invitations/')
            else:
                profil_temp = profil_temp[0]
                form = ProfilForm(initial={'first_name': profil_temp.first_name, 'last_name': profil_temp.last_name, 'email': profil_temp.email })
                return render(request, self.template_name, { "form" : form, "from_invitaion" : from_invitaion, "token_invitation" : token_invitation })
    def getAttribute(self, attr, data):
        return data[attr]

    def createToken(self):
        return uuid.uuid4()

    def post(self, request):
        form = ProfilForm(request.POST)


        if form.is_valid():

            data = form.cleaned_data
            email = self.getAttribute("email", data)
            password = self.getAttribute("password", data)
            confirm_password = self.getAttribute("confirm_password", data)
            user_exist = User.objects.filter(username=email)
            profil = Profil.objects.all().filter(email=email)

            if user_exist.count() == 0 :
                if password and (password == confirm_password):
                    user = User()
                    user.username = email
                    user.first_name = self.getAttribute("first_name", data)
                    user.last_name = self.getAttribute("last_name", data)

                    user.email = email
                    user.is_active = True
                    user.set_password(password)
                    user.save()

                    if profil.count() == 1:
                        profil = profil[0]
                    else:
                        profil = Profil()
                    profil.user = user
                    profil.first_name = self.getAttribute("first_name", data)
                    profil.last_name = self.getAttribute("last_name", data)

                    profil.type = self.getAttribute("type", data)
                    profil.email = email

                    profil.gender = self.getAttribute("gender", data)

                    token_profil = self.createToken()
                    profil.token = token_profil





                    profil.sendMail({   "token" : profil.token, "first_name" : user.first_name, "last_name" :  user.last_name  })
                    profil.save()

                    photo_base64 = data["photo_base64"]
                    if not photo_base64 == "" and not photo_base64 == "photo":
                        format, imgstr = photo_base64.split(';base64,')
                        ext = format.split('/')[-1]
                        data_file = ContentFile(base64.b64decode(imgstr))
                        file_name = str(profil.id) + "." + ext
                        profil.photo.save(file_name, data_file, save=True)

                    id = str(profil.id)

                    if profil.type == "author" :

                        url = "/account/create-author-account/?profil=" + id
                        return redirect(url)

                    return redirect('/account/custom-centres/'+id+"/")
                    #return redirect('/account/complete-profil/')
            else :
                return render(request, self.template_name, {"form": form, "message" : "Un profil avec meme adresse email existe deja"})


        return render(request, self.template_name, {"form" : form})


    def generateUID(self):
        return str(uuid.uuid4())[:8]

class CreateProfilUser(TemplateViewCustom):
    template_name = "create_profil_user.html"
    login = False

    def getCentres(self, profil):
        sections = Section.objects.all().filter(archive=False)
        categorys_profil = profil.category_set.all().filter(archive=False)
        for section in sections:
            categorys = section.category_set.all().filter(archive=False)
            for cat in categorys_profil:
                for cat_section in categorys:
                    if cat.id == cat_section.id:
                        cat_section.active = True


            section.categorys = categorys


        return sections

    def get(self, request):
        form = ProfilForm(initial={})
        #centres = self.getCentres()
        return render(request, self.template_name, { "form" : form})
    def getAttribute(self, attr, data):
        return data[attr]

    def createToken(self):
        return uuid.uuid4()




    def post(self, request):
        form = ProfilForm(request.POST)



        if form.is_valid():

            data = form.cleaned_data
            email = self.getAttribute("email", data)
            password = self.getAttribute("password", data)
            confirm_password = self.getAttribute("confirm_password", data)
            user_exist = User.objects.filter(username=email)
            user = User()
            profil = Profil.objects.all().filter(email=email)

            if user_exist.count() == 0 :
                if password and (password == confirm_password):
                    user = User()
                    user.username = email
                    user.first_name = self.getAttribute("first_name", data)
                    user.last_name = self.getAttribute("last_name", data)
                    user.email = email
                    user.is_active = True
                    user.set_password(password)
                    user.save()

                    if profil.count() == 1:
                        profil = profil[0]
                    else:
                        profil = Profil()
                    profil.user = user
                    profil.first_name = self.getAttribute("first_name", data)
                    profil.last_name = self.getAttribute("last_name", data)
                    profil.email = email

                    profil.gender = self.getAttribute("gender", data)
                    profil.type = "user"

                    token_profil = self.createToken()
                    profil.token = token_profil
                    profil.sendMail({   "token" : profil.token, "first_name" : user.first_name, "last_name" :  user.last_name  })
                    profil.save()


                    #return redirect('/account/complete-profil/')
                    return redirect('/account/custom-centres/'+profil.id+"/")
            else :
                return render(request, self.template_name, {"form": form, "message" : "Un profil avec meme adresse email existe deja"})


        return render(request, self.template_name, {"form" : form})


    def generateUID(self):
        return str(uuid.uuid4())[:8]

class CreateAuthor(TemplateViewCustom):
    template_name = "create_author.html"
    login = False

    def get(self, request):
        form = AuthorForm
        user = request.user
        profil = Profil.objects.all().filter(user=user)
        if profil.count() == 1:
            profil = profil[0]
            form = ProfilForm(initial={'first_name': profil.first_name, 'last_name': profil.last_name, 'email': profil.email })
        else:
            return redirect("/account/create-profil/")
        return render(request, self.template_name, { "form" : form })


    def getAttribute(self, attr, data):
        return data[attr]

    def createToken(self):
        return uuid.uuid4()

    def post(self, request):
        form = AuthorForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            email = self.getAttribute("email", data)
            user_exist = User.objects.filter(username=email)
            user = User()
            profil = Profil.objects.all().filter(email=email)

            if profil.count() == 1 :
                profil = profil[0]
                author = Author.objects.all().filter(account=profil)

                if author.count() == 0:
                    author  = Author()
                    uid = self.generateUID()
                    author.account = profil
                    author.first_name = self.getAttribute("first_name", data)
                    author.last_name = self.getAttribute("last_name", data)
                    author.email = self.getAttribute("email", data)
                    author.uid = uid
                    author.website = self.getAttribute("website", data)
                    author.facebook = self.getAttribute("facebook", data)
                    author.twitter = self.getAttribute("twitter", data)
                    author.instagram = self.getAttribute("instagram", data)
                    author.linkedin = self.getAttribute("linkedin", data)
                    author.youtube = self.getAttribute("youtube", data)
                    about_text = self.getAttribute("about", data)
                    about_text = strip_tags(about_text)
                    author.about = about_text

                    photo_base64 = data["photo_base64"]

                    if not photo_base64 == "" and not photo_base64 == "photo":
                        format, imgstr = photo_base64.split(';base64,')
                        ext = format.split('/')[-1]
                        data_file = ContentFile(base64.b64decode(imgstr))
                        file_name = str(uid) + "." + ext
                        author.photo.save(file_name, data_file, save=True)

                    author.save()
                    return redirect('/backend/dashboard/')

                return redirect('/account/create-profil/')
            else :
                return redirect('/account/create-profil/')

        return render(request, self.template_name, {"form" : form})


    def generateUID(self):
        return str(uuid.uuid4())[:8]

class CreateAuthorAccount(TemplateViewSite):
    template_name = "create_author_account.html"
    login = False

    def get(self, request):
        form = AuthorForm

        uid_profil = ""
        if "profil" in request.GET :
            uid_profil = request.GET["profil"]




        profil = Profil.objects.all().filter(id=uid_profil)
        if profil.count() == 1:
            profil = profil[0]
            form = ProfilForm(
                initial={'first_name': profil.first_name, 'last_name': profil.last_name, 'email': profil.email})
        else:
            return redirect("/account/create-profil/")

        #form = ProfilForm()
        menu = self.getMenu()
        return render(request, self.template_name, { "form" : form, "menu" :  menu })


    def getAttribute(self, attr, data):
        return data[attr]

    def createToken(self):
        return uuid.uuid4()

    def post(self, request):
        form = AuthorForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            email = self.getAttribute("email", data)
            profil = Profil.objects.all().filter(email=email)

            if profil.count() == 1 :
                profil = profil[0]
                email = self.getAttribute("email", data)
                last_name = self.getAttribute("last_name", data)
                first_name = self.getAttribute("first_name", data)
                author = Author.objects.all().filter(email=email, first_name=first_name, last_name=last_name)

                if author.count() == 0:
                    author  = Author()
                    uid = self.generateUID()
                    author.account = profil
                    author.first_name = self.getAttribute("first_name", data)
                    author.last_name = self.getAttribute("last_name", data)
                    author.email = self.getAttribute("email", data)
                    author.uid = uid
                    author.user_name = email
                    author.phone = ""
                    author.languages = "ar"
                    author.website = self.getAttribute("website", data)
                    author.facebook = self.getAttribute("facebook", data)
                    author.twitter = self.getAttribute("twitter", data)
                    author.instagram = self.getAttribute("instagram", data)
                    author.linkedin = self.getAttribute("linkedin", data)
                    author.youtube = self.getAttribute("youtube", data)
                    about_text = self.getAttribute("about", data)
                    about_text = strip_tags(about_text)
                    author.about = about_text

                    photo_base64 = data["photo_base64"]

                    if not photo_base64 == "" and not photo_base64 == "photo":
                        format, imgstr = photo_base64.split(';base64,')
                        ext = format.split('/')[-1]
                        data_file = ContentFile(base64.b64decode(imgstr))
                        file_name = str(uid) + "." + ext
                        author.photo.save(file_name, data_file, save=True)

                    author.save()
                    return redirect('/account/complete-profil/')
            else :
                return render(request, self.template_name, {"form": form, "message" : "Un profil avec meme adresse email existe deja"})
        menu = self.getMenu()
        return render(request, self.template_name, {"form" : form, "menu" :  menu})


    def generateUID(self):
        return str(uuid.uuid4())[:8]


# COMPLETE PAGES

class CompleteProfil(TemplateViewCustom):
    http_method_names = ['get', ]
    template_name = "complete_profil.html"
    login = False
    def get(self, request):
        return render(request, self.template_name, { "message" : "Verify your email adresse for activate your account"})

class CompleteAuthor(TemplateViewCustom):
    http_method_names = ['get', ]
    template_name = "complete_author.html"
    login = False
    def get(self, request):
        return render(request, self.template_name, { "message" : "Verify your email adresse for activate your account"})

class VerifyProfil(TemplateViewCustom):
    http_method_names = ['get', ]
    template_name = "verify_profil.html"
    login = False

    def createToken(self):
        return uuid.uuid4()

    def profil_exist(self, token):
        if Profil.objects.all().filter(token=token).exists():
            Profil.objects.all().filter(token=token)[0].status_invitation = 'Active'
            return True
        else:
            return False

    def get_profil(self, token):
        return Profil.objects.all().filter(token=token)

    def get(self, request, token, **kwargs):
        #context = super(VerifyProfil, self).get_context_data(**kwargs)
        #token = kwargs["token"]
        exist = self.profil_exist(token)
        if exist:
            profil = self.get_profil(token)[0]
            active_profil = profil.active
            if active_profil == False:
                now = time.strftime("%Y-%m-%d")
                date_created = profil.date_created
                date_format = "%Y-%m-%d"
                a = datetime.strptime(now, date_format)
                d = date_created.strftime("%Y-%m-%d")
                b = datetime.strptime(d, date_format)
                delta = b - a
                if delta.days < 3:
                    profil.active = True
                    user = profil.user
                    user.is_active = True
                    user.save()
                    profil.status_invitation = "Active"
                    profil.save()
                    return render(request, self.template_name, {"message": "Thank you, your account is Active"})
                else:
                    profil.token = self.createToken()
                    profil.date_created = now
                    profil.save()
                    return render(request, self.template_name, {"message": "Token is expired, Verify your email adresse for activate your account"})
            else :
                return redirect('/account/login-profil')
        else :
            return redirect('/account/create-profil/')


# LOGIN 1 LOGOUT PAGES
class LoginProfil(TemplateViewCustom):
    template_name = "login_profil.html"
    next_page = ""
    login = False

    def getAttribute(self, attr, data):
        return data[attr]

    def getAuthor(self, profil):
        author = None
        temp_auhtor = profil.author_set.all()
        if temp_auhtor.count() == 1:
            author = temp_auhtor[0]

        return author

    def get(self, request):
        form = LoginForm
        if request.user.is_authenticated:
            if 'next' in request.GET :
                self.next_page = request.GET["next"]
            if not self.next_page == None and not self.next_page == "" :
                return HttpResponseRedirect(self.next_page)
            else :
                user = request.user
                profil = Profil.objects.all().filter(user=user)
                if profil.count() == 1 :
                    profil = profil[0]

                    if profil.active == False:
                        return HttpResponseRedirect('/account/complete-profil/')

                    else:
                        if profil.type == "author" :
                            auhtor = self.getAuthor(profil)
                            if auhtor == None:
                                return HttpResponseRedirect('/account/create-author/')
                            else:
                                if auhtor.active == True:
                                    return HttpResponseRedirect('/backend/dashboard/')
                                else:
                                    return HttpResponseRedirect('/waiting-page/')


                        if profil.type == "user" and profil.topic_set.all().count() == 0:
                            return HttpResponseRedirect('/account/custom-centres/')

                        if profil.type == "user" and profil.topic_set.all().count() > 0:
                            return HttpResponseRedirect('/')

                        return HttpResponseRedirect('/backend/dashboard/')


        return render(request, self.template_name, {"form": form})


    def post(self, request):
        form = LoginForm(request.POST)
        message = ''
        if "next" in request.GET :
            self.next_page = request.GET["next"]

        if form.is_valid():
            data = form.cleaned_data
            email = self.getAttribute("email", data)
            password = self.getAttribute("password", data)



            user = authenticate(username=email, password=password)

            if user:
                profil = Profil.objects.get(user_id=user.id)
                if profil.active:
                    login(request, user)

                    message = "Your are connected "+user.first_name
                    if not self.next_page == None and not self.next_page == "":
                        return HttpResponseRedirect(self.next_page)
                    else:

                        if profil.type == "author" :
                            auhtor = self.getAuthor(profil)
                            if auhtor == None:
                                return HttpResponseRedirect('/account/create-author/')
                            else:
                                return HttpResponseRedirect('/backend/dashboard/')

                        if profil.type == "user" and profil.category_set.all().count() == 0:
                            return HttpResponseRedirect('/account/custom-centres/')

                        if profil.type == "user" and profil.category_set.all().count() > 0:
                            return HttpResponseRedirect('/')

                        return HttpResponseRedirect('/backend/dashboard/')


                else:
                    message = "Your account is inactive, please activate your account"
                    return HttpResponseRedirect('/account/complete-profil/')

            elif email and password:
                message = "Email adress or password not correct"

        return render(request, self.template_name, {"form" : form, "message" : message})

class LogoutProfil(TemplateViewCustom):
    template_name = "logout_profil.html"
    login = False

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/account/login-profil')


# EDIT PROFIL PAGES
class PasswordProfil(TemplateViewCustom):
    template_name = "password_profil.html"
    login = False

    def createToken(self):
        return uuid.uuid4()

    def getAttribute(self, attr, data):
        return data[attr]

    def get(self, request, token):
        form = PasswordForm
        return render(request, self.template_name, {"form": form, "token" : token})

    def post(self, request, token):
        form = PasswordForm(request.POST)
        message = ''

        if form.is_valid():
            data = form.cleaned_data
            password = self.getAttribute("password", data)
            confirm_password = self.getAttribute("confirm_password", data)
            profil = Profil.objects.all().filter(token=token)
            if len(profil) == 0:
                return HttpResponseRedirect('/account/login-profil/')
            else:
                profil_temp = profil[0]
                user = User.objects.all().filter(email=profil_temp.email)
                if len(user) > 0:
                    if (password == confirm_password) and password:
                        user = user[0]
                        user.set_password(password)
                        profil = Profil.objects.get(user_id=user.id)
                        profil.active = False
                        profil.token = self.createToken()
                        user.save()
                        profil.save()
                        message = "Your account is inactive, please activate your account, by verify your email adress"
                        status_email = profil_temp.sendMail({ "company" : profil.company.uid,  "token": profil.token, "first_name" :profil.first_name, "last_name" :profil.last_name })
                        return redirect('/account/complete-profil/')
                        #return render(request, self.template_name, {"form": form, "message": message, "type" : "success", "token" : token})
                    else :
                        message = 'Password and confirm password not matched'

                    if not confirm_password:
                        message = 'Please confirm password'
        return render(request, self.template_name, {"form": form, "message": message, 'type' : "error", "token" : token})

class ForgetPassword(TemplateViewCustom):
    template_name = "forget_password.html"
    login = False

    def createToken(self):
        return uuid.uuid4()

    def getAttribute(self, attr, data):
        return data[attr]

    def get(self, request):
        form = ForgetPasswordForm
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        message = ''

        if form.is_valid():
            data = form.cleaned_data
            email = self.getAttribute("email", data)
            users = User.objects.all().filter(username=email)
            if len(users) == 0:
                render(request, self.template_name, {"form": form, "message": "This email adress not exist"})
            else:
                profil = Profil.objects.all().filter(email=email)[0]
                token = profil.token
                profil.sendMailPassord({ "token" : profil.token })
                return HttpResponseRedirect('/account/forget-password-complete/')



        return render(request, self.template_name, {"form": form, "message": message})

class ForgetpasswordComplete(TemplateViewCustom):
    template_name = "forget_password_complete.html"
    login = False

    def createToken(self):
        return uuid.uuid4()

    def getAttribute(self, attr, data):
        return data[attr]

    def get(self, request):
        return render(request, self.template_name, {})

class EditProfil(TemplateViewSite):
    http_method_names = ['get', 'post']
    template_name = "edit_profil.html"

    def getAttribute(self, attr, data):
        return data[attr]

    def get(self, request):
        menu = self.getMenu()
        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            form = EditProfilForm(initial={'first_name': profil.first_name, 'last_name': profil.last_name, 'email': profil.email, 'phone': profil.phone  })
            return render(request, self.template_name, { "form": form, "profil" : profil, "menu" : menu})
        else:
            return redirect('/account/logout-profil/')

    def post(self, request):
        menu = self.getMenu()
        form = EditProfilForm(request.POST)
        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() == 1:
            profil = profil[0]
            if form.is_valid():
                data = form.cleaned_data

                profil.first_name = self.getAttribute("first_name", data)
                profil.last_name = self.getAttribute("last_name", data)
                profil.email = self.getAttribute("email", data)
                profil.phone = self.getAttribute("phone", data)

                profil.save()

                form = EditProfilForm(initial={'first_name': profil.first_name, 'last_name': profil.last_name, 'email': profil.email,'phone': profil.phone})
                return render(request, self.template_name, { "form": form, "message": "Your profile is up to date with success", "menu" :  menu})
            else:
                form = EditProfilForm(initial={'first_name': profil.first_name, 'last_name': profil.last_name, 'email': profil.email,'phone': profil.phone})
                return render(request, self.template_name, { "form": form, "menu" : menu})
        else:
            return redirect('/account/logout-profil/')

class AboutProfil(TemplateViewSite):
    http_method_names = ['get', 'post']
    template_name = "about_profil.html"

    def getAttribute(self, attr, data):
        return data[attr]

    def get(self, request):
        menu = self.getMenu()
        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            form = AboutProfilForm(initial={'about': profil.about, 'gender': profil.gender, 'image': profil.photo})
            return render(request, self.template_name, { "form": form, "profil": profil, "menu" :  menu})
        else:
            return redirect('/account/logout-profil/')

    def post(self, request):
        menu = self.getMenu()
        form = AboutProfilForm(request.POST, request.FILES)
        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            if form.is_valid():
                data = form.cleaned_data

                about_text = self.getAttribute("about", data)
                about_text = strip_tags(about_text)
                profil.about = about_text
                profil.gender = self.getAttribute("gender", data)

                photo_base64 = data["photo_base64"]
                if not photo_base64 == "" and not photo_base64 == "photo":
                    format, imgstr = photo_base64.split(';base64,')
                    ext = format.split('/')[-1]
                    data_file = ContentFile(base64.b64decode(imgstr))
                    file_name = str(profil.id) + "." + ext
                    profil.photo.save(file_name, data_file, save=True)

                profil.save()

                form = AboutProfilForm(initial={'about': profil.about, 'gender': profil.gender})
                return render(request, self.template_name, { "status" : "success", "form": form, "menu" :  menu, "profil" : profil, "message": "تم تحديث ملفك الشخصي بنجاح "})
            else:
                form = AboutProfilForm(initial={'about': profil.about, 'gender': profil.gender})
                return render(request, self.template_name, { "status" : "error", "form": form, "profil" : profil, "message" : "Profil not exist", "menu" : menu})
        else:
            return redirect('/account/logout-profil/')

class SecurityProfil(TemplateViewSite):
    http_method_names = ['get', 'post']
    template_name = "security_profil.html"

    def get(self, request):
        menu = self.getMenu()
        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            form = SecuityProfilForm
            return render(request, self.template_name, {"form": form, "profil": profil, "menu" :  menu})
        else:
            return redirect('/account/logout-profil/')

    def getAttribute(self, attr, data):
        return data[attr]

    def redirect(self):
        return HttpResponseRedirect('/account/login-profil')

    def post(self, request):

        form = SecuityProfilForm(request.POST)
        user = request.user
        profils = profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            if form.is_valid():
                data = form.cleaned_data
                current_password = self.getAttribute("current_password", data)
                new_password = self.getAttribute("new_password", data)
                confirm_new__password = self.getAttribute("confirm_new_password", data)
                user_temp = authenticate(username=request.user.email, password=current_password)
                if user_temp == None:
                    return render(request, self.template_name, { "form": form, "message": 'Current password is not correct', "type": "error"})
                else:
                    if (new_password == confirm_new__password) and new_password:
                        user.set_password(new_password)
                        user.save()
                        message = "Password has been successfully changed"
                        return render(request, self.template_name, {"form": form, "message": message, "type": "success"})
            else:
                return render(request, self.template_name, {"form": form})
        else:
            return redirect('/account/logout-profil/')



        #user = request.user
        #profil = Profil.objects.get(user_id=user.id)


# UPDATE SETTINGS PROFIL
class CustomCentres(TemplateViewSite):
    http_method_names = ['get', ]
    template_name = "custom_centres.html"
    login = False

    def getCentres(self, profil):
        categorys = Category.objects.all().filter(archive=False).order_by("id")
        topics_profil = profil.topic_set.all().filter(archive=False)
        topics = Topic.objects.all().filter(archive=False)

        for cat in categorys:
            cat_topics = cat.topic_set.all().filter(archive=False).order_by("id")
            for top in cat_topics:
                for temp_top in topics_profil:
                    if top.id == temp_top.id:
                        top.selected = True


            cat.topics = cat_topics


        return categorys


    def get(self, request, id):

        profil = Profil.objects.all().filter(id=id)
        if profil.count() == 1:
            profil = profil[0]
        else:
            return redirect("/account/create-profil/")
        centres = self.getCentres(profil)
        update = False
        if "update" in request.GET or profil.topic_set.all().count() > 0 and profil.active == True:
            update = True

        menu = self.getMenu()
        return render(request, self.template_name, { "centres" : centres , "profil" : profil, "update" : update, "menu": menu})

class MyBookmarks(TemplateViewSite):
    http_method_names = ['get', ]
    template_name = "my_bookmarks.html"
    login = False

    def getBookmarks(self, profil):
        bookmarks = profil.bookmark_set.all()

        return bookmarks

    def getProfil(self, request):
        profil = Profil.objects.all().filter(user=request.user)
        if profil.count() == 1:
            profil = profil[0]
            return profil
        else:
            return None


    def get(self, request):

        profil = self.getProfil(request)
        if profil == None:
            return redirect("/account/create-profil/")
        else:
            bookmarks = self.getBookmarks(profil)
            articles_not_read = []
            articles_readed = []

            for bookmark in bookmarks:
                articles_not_read.append(bookmark.article)

            menu = self.getMenu()
            return render(request, self.template_name, { "bookmarks" : bookmarks , "profil" : profil, "menu": menu, "articles_not_read" : articles_not_read})

class CustomizeMyHome(TemplateViewSite):
    http_method_names = ['get', 'post']
    template_name = "customize_my_home.html"

    def get(self, request):
        menu = self.getMenu()
        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]

            return render(request, self.template_name, {"profil": profil, "count_themes": 12, "count_layouts" : 5, "menu" :  menu})
        else:
            return redirect('/account/logout-profil/')









