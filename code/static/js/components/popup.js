import invock, {Component} from "invock-js";
import FormCommon from "./common/form";
import Plugins from "../plugins/plugins";
import PopupProject from "./popup/popup_project";
import PopupEnvironnement from "./popup/popup_env";
import PopupContainer from "./popup/popup_container";
import PopupService from "./popup/popup_service";
import PopupVariable from "./popup/popup_variable";
import PopupDeployment from "./popup/popup_deployment";
import PopupIngress from "./popup/popup_ingress";
import PopupJob from "./popup/popup_job";
import PopupVolume from "./popup/popup_volume";
import PopupTemplate from "./popup/popup_template";
import VariableTemplate from "./common/variable_template";
import CommandTemplate from "./common/command_template";
import CommandInlineTemplate from "./common/command_inline_template";

import ContainerTemplate from "./common/container_template";
import AnnotationTemplate from "./common/annotation_template";
import EnvVariableTemplate from "./common/env_variable_template";
import PopupContainerExisted from "./popup/popup_container_existed";
import PopupVolumeExisted from "./popup/popup_volume_existed";

class Popup extends Component {
    
    constructor(params) {
        super(params);
        this.form = null;
        this.status = "create";
        this.env_variables = [];
        this.events = {
            "click .action-popup" : "applyAction",
            "click .accordeon-trigger" : "openAccordeon",
            "click .switcher" : "changeSwitcher",
            "click #select-type-job" : "changeJobType",
            "click .remove-item" : "removeItemInline",
            "change #select-variales" : "addEnvVariable",
            "change .select-template" : "ApplyTemplate"
            
            
        };
    }
    
    
    ApplyTemplate(evt, self) {
        var uid = this.val();
        var type = this.data("type");
        if (uid !== "" && uid !== " ") {
            var template = self.getTemplate(uid);
            if ( self.props.element === "container" ) {
                //var data = Object.assign({}, self.props.data);
                //data.commands = template.data;
                //self.setStateStore(data, true, true);
                var l_commands = template.data.length;
                for ( var c = 0; c < l_commands; c++ ) {
                    var parent = self.parent.find("#commands-items").find(".subs-container");
                    if ( parent !== null ) {
                        var object_command = template.data[c];
                        object_command.count = c+1;
                        self.renderTemplate("CommandTemplate", parent, object_command);
                    }
                }
                
                self.initSelects();
            }
            
            if ( self.props.element === "service" ) {
                var parent_before_install = self.parent.find("#before-install-inputs").find(".subs-container");
                var parent_script = self.parent.find("#script-inputs").find(".subs-container");
                var parent_after_success = self.parent.find("#after-success-inputs").find(".subs-container");
                var parent_deploy = self.parent.find("#deploy-inputs").find(".subs-container");
                
                self.renderTemplateSectionService("before_install", template.data.before_install, parent_before_install);
                self.renderTemplateSectionService("script", template.data.script, parent_script);
                self.renderTemplateSectionService("after_success", template.data.after_success, parent_after_success);
                self.renderTemplateSectionService("deploy", template.data.deploy, parent_deploy);
            }
        }
        
        if ( self.props.element === "ingress" ) {
            var parent = null;
            if ( type === "annotations" ) {
                parent = self.parent.find("#container-annotations").find(".subs-container");
                
            }
            if( type === "containers" ) {
                parent = self.parent.find("#container-containers").find(".subs-container");
            }
            
            var l_commands = template.data.length;
            for ( var c = 0; c < l_commands; c++ ) {
                if ( parent !== null ) {
                    var object_command = template.data[c];
                    object_command.count = c+1;
                    self.renderTemplate("CommandTemplate", parent, object_command);
                }
            }

            self.initSelects();
        }
    }
    
    
    renderTemplateSectionService(type, data, parent, ) {
        
        var l_commands = data.length;
        for ( var c = 0; c < l_commands; c++ ) {
            if ( parent !== null ) {
                var object_command = data[c];
                object_command.count = c+1;
                object_command.type_command = type;
                console.log(object_command);
                this.renderTemplate("CommandInlineTemplate", parent, object_command);
            }
        }
    }
    
    getTemplate(uid) {
        var l = this.props.data.templates.length;
        var result = null;
        if ( l > 0 ) {
            for ( var i = 0; i < l; i++ ) {
                var item = this.props.data.templates[i];
                if ( item.uid === uid ) {
                    result = item;
                    i = l;
                }
            }
        }
        return result;
        
    }
    
    addEnvVariable(evt, self) {
        var value = this.val();
        var container = this.getParent().find("#container-env-variables-items");
        if ( container !== null && value !== "") {
            this.findAll("option")[0].removeAttr("selected");
            var name = this.find("option[value='"+value+"']").data("name");
            var props = {
                "name" : name, 
                "uid" : value,
            }
            self.renderTemplate("EnvVariableTemplate", container, props, null);        
            this.findAll("option")[0].setAttribute("selected", "selected");
        } 
    }
    
    removeItemInline(evt, self) {
        var parent = this.closests(".inline-block-item");
        var uid = this.data("uid");
        var state = this.data("state");
        if ( parent !== null ) {
            if ( state === "remove" ) {
                self.removeVar(uid)
            }
            parent.animate(0.5, { "opacity" : 0, onComplete : function() {parent.remove(); } });
        }
    }
    
    removeVar(uid) {
        var self = this;
        var url = "/api/backend/delete-element/variable/"+uid+"/";
        
        self.http.url = url;
        self.http.fetch(function(response) {
           self.displayMessage(response.status, response.message);
        });
    }
    
    changeJobType(evt, self) {
        var type = this.val();
        var cron_param = self.parent.find(".cron-param");
        if ( type === "cron" ) {
            if ( cron_param !== null ) {
                cron_param.removeClass("none");
            }
        }
        else {
            if ( cron_param !== null ) {
                cron_param.addClass("none");
            }
        }
    }
    
    changeSwitcher(evt, self) {
        var class_active = this.hasClass("active");
        var input = this.find("input");
        var label_yes = this.data("yes");
        var label_no = this.data("no");
        var text_handler = this.find(".text-handler");
        if ( class_active === true ) {
            this.removeClass("active");
            if( input !== null ) {
                input.val("false");
            }
            if( text_handler !== null ) {
                text_handler.html(label_no);
            }
        }
        else {
            this.addClass("active");
            if( input !== null ) {
                input.val("true");
            }
            if( text_handler !== null ) {
                text_handler.html(label_yes);
            }
        }
    }
    
    
    openAccordeon(evt, self) {
        var parent = this.closests(".accordeon-container");
        if ( parent !== null ) {
            var class_open = parent.hasClass("open");
            var active_accordeon = self.parent.find(".accordeon-container.open");
            if ( active_accordeon !== null &&  active_accordeon !== parent) {
                active_accordeon.removeClass("open");
            }
            if ( class_open === true ) {
                parent.removeClass("open");
            }
            else {
                parent.addClass("open");
            }
            
        }
    }
    
    applyAction(evt, self) {
        var action = this.data("action");
        
        if ( action === "close" ) {
            self.close();
        }
        if ( action === "add_variable" ) {
            self.addVariable(this);
        }
        
        if ( action === "add_command" ) {
            self.addCommand(this);
        }
        
        if ( action === "add_inline_command" ) {
            self.addInlineCommand(this);
        }
        
        if ( action === "add_container_ingress" ) {
            self.addInlineContainer(this);
        }
        
        if ( action === "add_annotation_ingress" ) {
            self.addInlineAnnotation(this);
        }
        
        
    }
    
    
    addInlineAnnotation(element) {
        var parent = element.closests("#container-annotations");
        if ( parent !== null ) {
            var count = parent.findAll(".inline-annotation-item").length+1;
            
            this.renderTemplate("AnnotationTemplate", parent.find(".subs-container"), { count : count});
        }
    }
    
    
    
    addInlineContainer(element) {
        var self = this;
        var url = "/api/backend/get-clusters/"+Config.env+"/";
        this.http.url = url;
        this.http.fetch(function(response) {
           var parent = element.closests("#container-containers");
            if ( parent !== null ) {
                var count = parent.findAll(".inline-container-item").length+1;

                var sub_container = parent.find(".subs-container");


                self.renderTemplate("ContainerTemplate", sub_container, { count : count, list : response.data});
            }
        });
        
        
        
        
    }  
    
    addInlineCommand(element) {
        var parent = element.closests(".container-commands-inputs");
        if ( parent !== null ) {
            var count = parent.findAll(".inline-command-inline-item").length+1;
            
            var sub_container = parent.find(".subs-container");
            
            
            this.renderTemplate("CommandInlineTemplate", sub_container, { count : count, "type_command" : sub_container.data("type")});
        }
    }
    
    
    addCommand(element) {
        var parent = element.closests("#commands-items");
        if ( parent !== null ) {
            var count = parent.findAll(".inline-command-item").length+1;
            
            this.renderTemplate("CommandTemplate", parent.find(".subs-container"), { count : count});
        }
    }
    
    
    addVariable(element) {
        var parent = element.closests("#env-variables-items");
        if ( parent !== null ) {
            var count = parent.findAll(".inline-variable-item").length+1;
            
            this.renderTemplate("VariableTemplate", parent.find(".subs-container"), { count : count});
        }
    }
    
    
    
    renderTemplate(name, parent, props={}) {
        this.renderOtherComponent(name, props, parent, null);
    }
    
    
    close() {
        
        var self = this;
        this.parent.find(".overlay-popup").animate(0.5, { "opacity" : 0, onComplete : function() {
                self.parent.find(".overlay-popup").remove();
            } 
        });
        
        this.parent.find(".container-popup").animate(0.5, { "opacity" : 0, onComplete : function() {
                self.parent.find(".container-popup").remove();
                self.setStateStore({ commands : [] }, false, true);
            } 
        });
        this.env_variables = [];
    }
    
    open() {
        var self = this;
        var scrollTop = document.documentElement.scrollTop;
        this.parent.find(".container-popup").css({ top : scrollTop  });
        this.parent.find(".overlay-popup").fadeIn();
        this.parent.find(".container-popup").fadeIn();
        
        
        
        
    }
    
    
    convertDomToObject(doms) {
        var l = doms.length;
        var result = [];
        if ( l > 0) {
            for (var i = 0; i < l; i++) {
                var item_dom = doms.eq(i);
                var inputs = item_dom.findAll("[name]");
                var l_inputs = inputs.length;
                var object = {};
                
                for (var j = 0; j < l_inputs; j++) {
                    var item_input = inputs.eq(j);
                    var k = i+1;
                    var name = item_input.getAttribute("name").split("_"+k)[0];
                    object[name] = item_input.val();
                }
                result.push(object);
            }
        }
        
        return result;
    }
    
    convertInlineToObject(doms) {
        var l = doms.length;
        var result = [];
        if ( l > 0) {
            for (var i = 0; i < l; i++) {
                var item_dom = doms.eq(i);
                result.push(item_dom.data("uid"));
            }
        }
        return result;
    }
    
    processusSerializeData(data) {
        
        var commands_dom = this.parent.findAll(".inline-command-item");
        
        var variables_dom = this.parent.findAll(".inline-variable-item");
        
        var variables = this.parent.findAll(".inline-env-variable-item");
        
        var before_install = this.parent.findAll(".inline-command_before_install");
        var script = this.parent.findAll(".inline-command_script");
        var after_success = this.parent.findAll(".inline-command_after_success");
        var deploy = this.parent.findAll(".inline-command_deploy");
        
        var containers = this.parent.findAll(".inline-container-item");
        
        var annotations = this.parent.findAll(".inline-annotation-item");
        
        var commands_object = this.convertDomToObject(commands_dom);
        var variables_item_object = this.convertDomToObject(variables_dom);
        
        
        var before_install_object = this.convertDomToObject(before_install);
        var script_object = this.convertDomToObject(script);
        var after_success_object = this.convertDomToObject(after_success);
        var deploy_object = this.convertDomToObject(deploy);
        var containers_object = this.convertDomToObject(containers);
        var annotations_object = this.convertDomToObject(annotations);
        
        
        var variables_object = this.convertInlineToObject(variables);
        
        data.commands = commands_object;
        data.variables_items = variables_item_object;
        data.variables = variables_object;
        data.before_install = before_install_object;
        data.script = script_object;
        data.after_success = after_success_object;
        data.deploy = deploy_object;
        data.containers = containers_object;
        data.annotations = annotations_object;
        
        return data;
    }
    
    initForm(type, uid=null) {
        var self = this;
        var form_common = this.getClone("FormCommon");
        form_common.type_submit = "ajax";
        
        if (this.props.status === "create") {
            form_common.url_ajax = "/api/backend/save-element/"+type+"/";
        }
        else if (uid !== null){
            form_common.url_ajax = "/api/backend/update-element/"+type+"/"+uid+"/";
        }
        
        
        form_common.init();
        
        form_common.observerChanges = function(index, last_index) {
            if (index === last_index ) {
                var serialize = self.parent.find("form").serialize("object");
                serialize.project = self.props.project;
                serialize.environnement = self.props.env;
                serialize.parent = self.props.parent;
                
                serialize = self.processusSerializeData(serialize);
                
                
                
                //console.log(serialize);
                
                self.data_form = serialize;
                
                
               //dom.get(".loading-form").show();
               form_common.data_ajax = self.data_form;

                form_common.observerAjax = function(response) {
                    var callback_ = function() { location.reload(); };
                    if ( type === "deployment" || type === "container" || type === "volume" || type === "job" || type === "service" ) {
                        var callback_ = function() { location.reload(); };
                    }
                    else {
                        var callback_ = null
                    }
                    self.displayMessage(response.status, response.message, callback_);
                    //dom.get(".loading-form").hide();
                    self.close();
                    if ( typeof self.props.after_action !== "undefined") {
                        if ( typeof self.props.after_action === "function") {
                            self.props.after_action.call(this, self, response);
                        }
                    }
                };
            }
        };
    }
    
    
    displayMessage(status, message, callback=null) {
        
        this.renderOtherComponent("Message", { type : status, "message" :  message, "callback": callback }, dom.get("#prepend-body"), null);
        
    }
    
    afterRender() {
        
        var self = this;
        this.initSelects();
        
        this.open();
        
        
        var timer_fade = setTimeout(function() {
            self.initForm(self.props.element, self.props.uid);
        }, 700);
    }
    
    initSelects() {
        var selects = this.parent.findAll("select");
        var l_selects = selects.length;
        for ( var s = 0; s < l_selects; s++ ) {
            var item_select = selects.eq(s);
            var value = item_select.data("value");
            var option_target = item_select.find("option[value='"+value+"']");
            if (option_target !== null) {
                option_target.setAttr("selected", "selected");
            }
        }
    }
    
    
    
    render() {
        var html = "";
        
        if (this.props.element === "project") {
            html = PopupProject();
        }
        
        if (this.props.element === "environnement") {
            html = PopupEnvironnement();
        }
        
        if (this.props.element === "container") {
            html = PopupContainer();
        }
        if (this.props.element === "container_existed") {
            html = PopupContainerExisted();
        }
        
        if (this.props.element === "service") {
            html = PopupService();
        }
        
        if (this.props.element === "variable") {
            html = PopupVariable();
        }
        
        if (this.props.element === "deployment") {
            html = PopupDeployment();
        }
        
        if (this.props.element === "ingress") {
            html = PopupIngress();
        }
        
        if (this.props.element === "job") {
            html = PopupJob();
        }
        
        if (this.props.element === "volume") {
            html = PopupVolume();
        }
        
        if (this.props.element === "volume_existed") {
            html = PopupVolumeExisted();
        }
        
        if (this.props.element === "template") {
            html = PopupTemplate();
        }
        
        return html;
        
    }
    
}


invock.export("Popup", Popup, "commands,data");

invock.mount({ parent : "#prepend-body", root : "{% FormCommon parent_name='#prepend-body' %}" });