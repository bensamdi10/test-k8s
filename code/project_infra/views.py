#-*- coding: utf-8 -*-


from django.shortcuts import render, redirect
from django.conf import settings
from project_infra.template_view_site import TemplateViewSite
from project.models import Project
from environnement.models import Environnement


language = settings.LANGUAGE


# PAGES DYNAMICS
class Home(TemplateViewSite):
    http_method_names = ['get', ]
    template_name = 'home.html'
    name = "home"

    def get(self, request):

        projects = Project.objects.all().filter(archive=False)
		print("test")
        return render(request, self.template_name, { "projects" : projects })

class Workspace(TemplateViewSite):
    http_method_names = ['get', ]
    template_name = 'home.html'
    name = "home"


    def baseElements(self, uid, type):
        elements = []
        if type == "project" :
            elements = Project.objects.all().filter(archive=False)
            for pr in elements:
                if pr.uid == uid:
                    pr.current = True
                    pr.save()
                else:
                    pr.current = False
                    pr.save()
        if type == "env":
            elements = Environnement.objects.all().filter(archive=False)
            for en in elements:
                if en.uid == uid:
                    en.current = True
                    en.save()
                else:
                    en.current = False
                    en.save()

        return elements

    def getEnvVariables(self, environnement):
        variables = environnement.variable.all().filter(archive=False)
        return variables

    def mergeQuery(self, q1, q2):
        q3 = q1.union(q2)
        q3 = q3.distinct()
        return q3

    def get(self, request, project, env):
        deployments = []
        ingress = []
        services = []
        jobs = []
        environnement = Environnement.objects.all().filter(uid=env)
        if environnement.count() == 1:
            environnement = environnement[0]
            environnement.container_count = 0
            services = environnement.service_set.all().filter(archive=False).order_by("id")
            jobs = environnement.job_set.all().filter(archive=False).order_by("id")
            deployments = environnement.deployment_set.all().filter(archive=False).order_by("id")
            variables = self.getEnvVariables(environnement)
            for deploy in deployments:
                containers = deploy.container_set.all().filter(archive=False)

                deploy.containers = containers
                environnement.container_count = environnement.container_count+containers.count()
                for cont in containers:
                    cont_variables = cont.variable.all().filter(archive=False)
                    variables = self.mergeQuery(variables, cont_variables)

                if deploy.clusterip_set.all().count() > 0 :
                    deploy.cluster_ip = deploy.clusterip_set.all()[0]
                volumes = deploy.persistent_volume.all().filter(archive=False)
                deploy.volumes = volumes

            ingress = environnement.ingress_set.all().filter(archive=False)[0]


        object_view = {
            "projects": self.baseElements(project, "project"),
            "current_project": project,
            "current_env": env, "envs": self.baseElements(env, "env"), "environnement" : environnement,
            "deployments" : deployments,
            "ingress" : ingress,
            "variables" : variables.order_by("id"),
            "services" : services,
            "jobs" : jobs
        }

        return render(request, self.template_name, object_view)




class RunEnv(TemplateViewSite):
    http_method_names = ['get', ]
    template_name = 'trace.html'
    name = "home"

    def get(self, request, env):
        return render(request, self.template_name, { "env" : env, 'label': "env_message" })

class ConnectCli(TemplateViewSite):
    http_method_names = ['get', ]
    template_name = 'blank.html'
    name = "connect-cli"

    def get(self, request):
        return render(request, self.template_name, { 'message': "connect CLI" })




