# -*- coding: utf-8 -*-


from django.contrib.auth.models import User

from account.models import Profil



class ProfilUser:
    def __init__(self):
        self.profil = None

    def checkUser(self, request):
        #request.user.is_authenticated()
        user = request.user.id
        profil = Profil.objects.all().filter(user_id=user)
        if profil.count() > 0 :
            profil = profil[0]
            if request.user.is_authenticated and profil.active:
                self.profil = profil
                return True
        else :
            return False


    def getProfil(self, request):
        user = request.user.id
        profil = Profil.objects.all().filter(user_id=user)
        if profil.count() > 0:
            profil = profil[0]
            return profil
        else:
            return False
    def getCompany(self, request):
        user = request.user.id
        profil = Profil.objects.all().filter(user_id=user)
        if profil.count() > 0:
            profil = profil[0]
            return profil.company
        else:
            return False


    def checkAccess(self, type, request):
        company = self.getCompany(request)
        pack = company.pack
        result = False
        if type == "conversion":
            result = self.conversionAcess(pack, company.uid)

        return result


    def conversionAcess(self, pack, company):
        conversions = Ad.objects.all().filter(company=company)
        result = False
        if pack == "start":
            if conversions.count() < 151:
                result = True
        if pack == "basic":
            if conversions.count() < 301:
                result = True
        if pack == "pro":
            if conversions.count() < 501:
                result = True

        if pack == "entreprise":
            if conversions.count() < 601:
                result = True

        return result