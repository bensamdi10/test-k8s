import invock, {Component} from "invock-js";
import Base from "./base";
import FormCommon from "./common/form";
import Plugins from "../plugins/plugins";
import Message from "./common/message";
import Popup from "./popup";


// kubectl delete -n default cronjob job-cron
// delete -n default job job-migration
// delete -n default pod job-cron-1587151860-bqjsk
// docker system prune --all --force
class Workspace extends Component {
    
    constructor(params) {
        super(params);
        self.terminal = null;
        this.current = {};
        this.context = { "context" : "env", "status" : "pending", "output" : [], "uid" : Config.env, "env" : Config.env, "project" :  Config.project, "env_name" : Config.name_env,  "project_name" : Config.name_project, "workdir" : "", "slug_env" : Config.slug_env, "slug_project" : Config.slug_project };
        this.action = "";
        this.workdir = Config.name_project+"/"+Config.name_env+'/ $ ';
        this.default_workdir = Config.name_project+"/"+Config.name_env+'/ $ ';
        this.callback_socket = {};
        this.events = {
            "change #select-project" :  "changeProject",
            "click .btn-action" : "applyAction",
            "click .btn-inline-action" : "applyInlineAction",
            "click .option-component" : "openOptionsMenu",
            "click #switcher-edition" : "changeEditionMode",
            "click .status-element" : "openNotifStatus",
            "click .btn-action-env" : "applyEnvAction",
        }
    }
    
    
    applyEnvAction(evt, self) {
        var action = this.data("action");
        var uid = this.data("uid");
        var element = this.data("element");
        var slug = this.data("slug");
        self.context.deployment_slug = slug;
        if ( action === "journal-deployment" ) {
            self.showTerminal();
        }
        else {
            var data = JSON.stringify({
                'uid': Config.env,
                "action" : action,
                "output" : [],
                "input" : "",
                "output_errors" : [],
                "workdir" : Config.terminal.workdir,
                "finish_output" : "true",
                "context" : self.context
            });
            self.socket.send(data);
        }
        
        
    }
    
    changeSwitcher(element) {
        var class_active = element.hasClass("active");
        var input = element.find("input");
        var label_yes = element.data("yes");
        var label_no = element.data("no");
        var text_handler = element.find(".text-handler");
        if ( class_active === true ) {
            element.removeClass("active");
            if( input !== null ) {
                input.val("false");
            }
            if( text_handler !== null ) {
                text_handler.html(label_no);
            }
        }
        else {
            element.addClass("active");
            if( input !== null ) {
                input.val("true");
            }
            if( text_handler !== null ) {
                text_handler.html(label_yes);
            }
        }
    }
    
    openNotifStatus(evt, self) {
        var class_open = this.hasClass('open');
        if ( class_open === true ) {
            this.removeClass("open");
        }
        else {
            this.addClass("open");
        }
    }
    
    changeEditionMode(evt, self) {
         var class_active = this.hasClass("active");
        var terminal = dom.get("#terminal");
        var label_yes = this.data("yes");
        var label_no = this.data("no");
        var text_handler = this.find(".text-handler");
        var open_terminal_btn = dom.get("#open-terminal");
        if ( open_terminal_btn !== null ) {
            if ( class_active === true ) {
                this.removeClass("active");
                if( terminal !== null ) {
                    terminal.removeClass("edition-manuel");
                }
                if( text_handler !== null ) {
                    text_handler.html(label_no);
                }
                open_terminal_btn.show();
            }
            else {
                this.addClass("active");
                if( terminal !== null ) {
                    terminal.addClass("edition-manuel");
                }
                if( text_handler !== null ) {
                    text_handler.html(label_yes);
                }
                open_terminal_btn.hide();
                self.closeTerminal();
            }
        }
        
    }
    
    
    openOptionsMenu(evt, self) {
        var options_menu = this.getParent().find(".sub-menu-options");
        if (options_menu !== null) {
            var class_open = options_menu.hasClass("open");
            var class_active = this.hasClass("active");
            
            var option_component = dom.get('.option-component.active');
            var sub_menu_options = dom.get(".sub-menu-options.open"); 

            if (option_component !== null && sub_menu_options !== null) {
                option_component.removeClass("active");
                sub_menu_options.removeClass("open");
                sub_menu_options.fadeOut();
            }
            
            if ( class_open === true && class_active === true ) {
                options_menu.removeClass("open");
                this.removeClass("active");
                options_menu.fadeOut();
            }
            else {
                options_menu.addClass("open");
                this.addClass("active");
                options_menu.fadeIn();
            }
        }
    }
    
    
    applyInlineAction(evt, self) {
        var action = this.data("action");
        var element = this.data("element");
        var uid = this.data("uid");
        var class_switcher = this.hasClass('switcher');
        if( class_switcher === true ) {
            self.changeSwitcher(this);
        }
        
        var url = '/api/backend/update-inline-element/'+element+"/"+uid+"/";
        var serialize = this.getParent().serialize("object");
        self.http.url = url;
        self.http.post(serialize, function(response) {
           self.renderOtherComponent("Message", { type : response.status, "message" : response.message }, dom.get("#prepend-body"), null);
        });
    }
    
    applyAction(evt, self) {
        var action = this.data("action");
        var element =  this.data("element");
        var parent =  this.data("parent");
        var uid =  this.data("uid");
        var extra =  this.data("extra");
        self.action = action;
        if ( extra !== null ) {
            extra = JSON.parse(extra);
        }
         
        var class_action_icon = this.hasClass("action-icon");
        var props = { 
                "env" : Config.env, 
                "project" : Config.project, 
                "parent" : parent,
                "status" : "create",
                "commands" :[],
                "uid" : null,
                data : {},
                after_action : function(popup, response) {
                    if ( response.element === "environnement" ) {
                        location.href = '/workspace/'+Config.project+"/"+response.uid+"/";
                    }
                    if ( response.element === "project" ) {
                        location.href = '/workspace/'+response.uid+"/all/";
                    }
                }
            };
        
        if (action === "add") {
            self.addActionApply(props, element);  
        }
        
        if (action === "add-existed") {
            if (element === "container") {
                var url = "/api/backend/get-containers/"+Config.env+"/";
                self.http.url = url;
                self.http.fetch(function(response) {
                    props.data.containers = response.data;
                   self.renderPopup("container_existed", props);
                });
            } 
            if (element === "volume") {
                var url = "/api/backend/get-volumes/"+Config.env+"/";
                self.http.url = url;
                self.http.fetch(function(response) {
                    props.data.volumes = response.data;
                   self.renderPopup("volume_existed", props);
                });
            }
        }
        
        if (action === "edit" || action === "update") {
            self.editActionApply(element, uid, parent)
            
        }
        
        if ( action === "remove" ) {
            
            self.removeActionApply(element, uid)
        }
        
        if ( class_action_icon === true ) {
            
            var parent_menu = this.closests(".sub-menu-options");
            if ( parent_menu !== null ) {
                parent_menu.fadeOut();
                if( parent_menu.getParent().find(".option-component.active") !== null ) {
                    parent_menu.getParent().find(".option-component.active").removeClass("active");
                }
                
            }
        }
        
        if (action === "save") {
            self.saveActionApply(element, uid, parent);
        }
        
        
        
        if (action === "run-env") {
            self.runEnvActionApply(action, uid, this);
        }
        
        if (action === "run-container") {
            self.runContainerActionApply(action, uid);
        }
        
        if (action === "open-terminal") {
            self.openTerminalActionApply(action, uid);
        }
       /*
        var url = "/api/backend/generate-yaml/"+Config.env+"/";
        self.http.url = url;
        self.http.fetch(function(response) {console.log(response);});
        */
        
        if (action === "open-terminal" || action === "run-container") {
            self.openTerminal();
            
            
        }
        if (action === "close-terminal") {
            self.hideTerminal();
        }

    }
    
    // ACTION APPLY FUNCTIONS
    
    
    // ADD ACTION APPLY
    addActionApply(props, element) {
        var self = this;
        var url = "/api/backend/get-templates/"+element+"/";
        self.http.url = url;
        self.http.fetch(function(response) {
            props.data.templates = response.data;
             if (element === "job") {
                var url = "/api/backend/get-containers/"+Config.env+"/";
                self.http.url = url;
                self.http.fetch(function(response) {
                    props.data.containers = response.data;
                   self.renderPopup(element, props);
                });
            }
            else {      
                if ( element === "container" || element === "service" || element === "variable" ) {
                    var url = "/api/backend/get-env-variables/"+Config.env+"/";
                    self.http.url = url;
                    self.http.fetch(function(response) {
                        props.data.env_variables = self.convertBooleanValuesVars(response.data);
                        console.log(props.data.env_variables);
                        //props.data.env_variables = response.data;
                       self.renderPopup(element, props);
                    });
                }
                else {
                    self.renderPopup(element, props);
                } 
            }




        });
        
    }
    
    
    // EDIT & UPDATE ACTION APPLY
    editActionApply(element, uid, parent) {
        var self = this;
        var data_element = self.getDataElement(element, uid, function(response) {
            var data = response.data[0];
            data = self.convertBooleanValues(data);
            if ( data.hasOwnProperty("variables") === true ) {
                data.variables = self.convertBooleanValuesVars(data.variables);
            }

            var props = { 
                "env" : Config.env, 
                "project" : Config.project, 
                "parent" : parent,
                "data" : data,
                "status" :  "update",
                "uid" : uid,
                "after_action" : function(popup, response) {
                    if ( response.element === "environnement" ) {
                        location.href = '/workspace/'+Config.project+"/"+response.uid+"/";
                    }
                    if ( response.element === "project" ) {
                        location.href = '/workspace/'+response.uid+"/all/";
                    }
                }
            };

            if (  element === "job" ) {
                var url = "/api/backend/get-containers/"+Config.env+"/";
                self.http.url = url;
                self.http.fetch(function(response) {
                    props.data.containers = response.data;
                   self.renderPopup(element, props);
                });
            }
            else {

                if ( element === "container" || element === "service" || element === "variable" ) {
                    var url = "/api/backend/get-env-variables/"+Config.env+"/";
                    self.http.url = url;
                    self.http.fetch(function(response) {
                        
                        props.data.env_variables = self.convertBooleanValuesVars(response.data);
                        console.log(props.data.env_variables);
                        //props.data.env_variables = response.data;
                       self.renderPopup(element, props);
                    });
                }
                else {
                    self.renderPopup(element, props);
                }
            }

        });
    }
    
    // REMOVE  & DELETE ACTION APPLY
    removeActionApply(element, uid) {
        var self = this;
        var url = "/api/backend/delete-element/"+element+"/"+uid+"/";
        
        self.http.url = url;
        self.http.fetch(function(response) {
           self.displayMessage(response.status, response.message);
        });
    }
    
    // SAVE TEMPLATE ACTION APPLY
    saveActionApply(element, uid, parent) {
        var self = this;
        var props = { 
            "env" : Config.env, 
            "project" : Config.project, 
            "parent" : parent,
            "status" : "create",
            "uid" : uid,
            data : { "uid" : uid }
        };

        self.renderPopup("template", props);
    }
    
    
    // RUN ENVIRONNEMENT APPLY ACTION
    runEnvActionApply(action, uid, element_dom) {
        var self = this;
        var class_running = element_dom.hasClass("on-env");
        var class_error = element_dom.hasClass("off-env");
        var slug = element_dom.data("slug");
        if ( class_running === true) {
            element_dom.removeClass("on-env");
            element_dom.addClass("off-env");
            dom.get("body").removeClass("env-running");
            element_dom.html("ENV Turn OFF ...");
            self.runSocket("off-env", uid);
            
            self.callback_socket["terminate-env"] = { 
                "element" :element_dom, 
                "fn" :  function(element) {
                    element.removeClass("off-env");
                    element.removeClass("on-env");
                    element.html("Run ENV");
                    
                    var status_elements = dom.getAll(".status-element");
                    status_elements.removeClass("running pending error");
                    self.closeTerminal();
                }
            };
            
            
        }
        
        
        if ( class_running === false &&  class_error === false) {
            self.current.action = action;
            self.context.context = "env";
            self.context.status = "running";
            self.context.output = ["Start Running the Environnement"];

            element_dom.addClass("on-env");
            element_dom.html("ENV is running");
            dom.get("body").addClass("env-running");
            self.runSocket(action, uid);
            self.showTerminal();
            self.runTerminal();
        }
    }
    
    // RUn CONTAINER ACTION APPLY
    runContainerActionApply(action ,uid) {
        self.context.context = "container";
        self.context.uid = uid;
        self.context.output = ["Start Running the Container"];
        self.context.source = extra.source;
        self.context.name = extra.name;
        self.runSocket(action, uid);
    }
    
    // OPEN TERMINAL ACTION APPLY
    openTerminalActionApply(action ,uid) {
        var self = this;
        self.context.context = "terminal";
        self.context.uid = uid;
        self.context.output = ["Start The Terminal"];
        
        self.runSocket(action, uid);
    }
    
    
    
    openTerminal() {
        var self = this;
        var terminal_dom = dom.get("#container-terminal");
        if ( terminal_dom !== null ) {
            terminal_dom.show(); 
        }
        
        if ( self.terminal === null || typeof self.terminal === "undefined" ) {
            self.runTerminal();
            
        }
        else {
            self.terminal.clear();
            self.terminal.reset();
            self.prompt(self.terminal, Config.name_project+"/"+Config.name_env+'/'+self.context.workdir+' $ ');
        }
        
    }
    
    
    closeTerminal() {
        var self = this;
        var terminal_dom = dom.get("#container-terminal");
        if ( terminal_dom !== null ) {
            terminal_dom.hide();
        }
        if ( self.terminal !== null || typeof self.terminal !== "undefined" ) {
            self.terminal.clear();
            self.terminal.reset();
            self.prompt(self.terminal, Config.name_project+"/"+Config.name_env+'/'+self.context.workdir+' $ ');
        }
    }
    
    hideTerminal() {
        var terminal_dom = dom.get("#container-terminal");
        if ( terminal_dom !== null ) {
            terminal_dom.hide();
        }
    }
    showTerminal() {
        var terminal_dom = dom.get("#container-terminal");
        if ( terminal_dom !== null ) {
            terminal_dom.show();
        }
    }
    
    
    displayMessage(status, message) {
        this.renderOtherComponent("Message", { type : status, "message" :  message, callback : function() { location.reload(); } }, dom.get("#prepend-body"), null);
    }
    
    
    convertBooleanValues(data) {
        for ( var key in data ) {
            if (data.hasOwnProperty(key) === true) {
                if ( typeof data[key] === "boolean" ) {
                    data[key+"_active"] = "active";
                    data[key+"_label"] = "Yes";
                    if( data[key] === false ) {
                         data[key+"_active"] = "";
                        data[key+"_label"] = "No";
                    }
                }
            }
        }
        return data;
    }
    
    
    convertBooleanValuesVars(list) {
        var l = list.length;
        for ( var i = 0; i < l; i++ ) {
            var item = list[i];
            list[i] = this.convertBooleanValues(item);
        }
        console.log(list);
        return list;
    }
    
    
    getDataElement(element, uid, callback) {
        var url = "/api/backend/get-element/"+element+"/"+uid+"/";
        this.http.url = url;
        this.http.fetch(function(response) {
            if( typeof callback === "function" && callback != null ) {
                callback.call(this, response);
            }
        });
    }
    
    changeProject(evt, self) {
        var value = this.val();
        if ( value !== "" ) {
            location.href = "/workspace/"+value+"/all/";
        }
    }
    
    
    
    renderPopup(type, props={}) {
        var parent_popups = dom.get("#prepend-body");
        props.element = type;  
        this.renderOtherComponent("Popup", props, parent_popups, null);
    }
    
    
    afterRender() {
        var self = this;
        if (Config.count_project === 0) {
            this.renderPopup("project", {});
        }
        
        Config.terminal = {  "workdir" : "" };
        
        this.initSelects();
        this.socket = new WebSocket("ws://localhost:8004/connection-cli/");
        this.socket.onmessage = function(e) {
            
            const data = JSON.parse(e.data);
            self.current.action = data.action;
            self.current.name = data.name;
            //console.log(data);
            if ( typeof self.callback_socket[data.action] !== "undefined"  ) {
                if ( self.callback_socket[data.action]["fn"] !== null && typeof self.callback_socket[data.action]["fn"] === "function" ) {
                    self.callback_socket[data.action]["fn"].call(this, self.callback_socket[data.action]["element"]);
                    delete self.callback_socket[data.action];
                }
            }
            
            
            
            if  ( data.action === "output-events" ) {
                self.renderOutputEvents(data);
                var output_event = data.output.action+" "+ data.output.name +" with Status "+data.output.type+" in Phase "+data.output.phase;
                data.output = output_event;
                
                self.printOutputTerminal(data, data.workdir);
            }
            
            if  ( data.action === "terminate-env" ) {
                self.printOutputTerminal(data, data.workdir);
            }
            
            if (data.action === "output-ingress") {
                var span_ip = dom.get(".ip-adress-ingress");
                if ( span_ip !== null ) {
                    span_ip.html(data.output.toString());
                }
            }
            
            if ( self.terminal !== null && typeof self.terminal !== "undefined" ) {
                self.terminal.workdir = data.workdir;
                if ( data.action === "output-terminal" || data.action === "change-dir" ) {
                self.printOutputTerminal(data);
                }
                if ( data.action === "run-inside-container" || data.action === "run-inside-env" ) {
                    self.resetTerminal(data.workdir);
                }

                if ( data.action === "output-inside-containe") {
                    self.printOutputTerminal(data, data.workdir);
                }
            }
            
            
            
            
            
        };

        this.socket.onclose = function(e) {
            console.error('WorkSpace socket closed unexpectedly');
            this.socket = new WebSocket("ws://localhost:8004/connection-cli/");
        };
          
    }
    
    
    
    renderOutputEvents(data) {
        //data.output.name = data.output.name.slice(0, -1);
        var elements = dom.getAll(".widget-parent-event");
        var l_elements= elements.length;
        for ( var i = 0; i < l_elements; i++ ) {
            var element = elements.eq(i);
            var slug = element.data("slug");
            
            if ( data.output.name.indexOf(slug) > -1) {
                var status_element = element.find(".status-element");
                if ( status_element !== null && data.output.message !== "None") {
                    var status_output = data.output.phase;
                    var status = "error";
                    if ( status_output === "Running" || status_output === "running") {
                        status = "running"; 
                    }
                    if ( status_output === "Pending" || status_output === "pending") {
                        status = "pending"; 
                    }
                    if ( status_output === "Error" || status_output === "error" || status_output === "Unschedulable") {
                        status = "error"; 
                    }
                    if ( status_output === "Pending" && data.output.reason === "Unschedulable") {
                        status = "error"; 
                    }
                    status_element.removeClass("pending");
                    status_element.removeClass("error");
                    status_element.removeClass("running");

                    status_element.addClass(status);

                    if ( data.output.message !== null ) {
                        status_element.find(".notif-message-status").find(".text-notif").html(data.output.message);
                    }
                    else {
                        status_element.find(".notif-message-status").find(".text-notif").html("BackOff failure");
                    }


                }
            }
            
        }
        
    }
    
    printOutputTerminal(data) {
        if (data.context.context === this.context.context && this.context.status === "running") {
            Config.terminal.workdir = data.workdir;
            if (data.workdir !== "" && data.workdir !== " ") {
                this.workdir = data.workdir;
            }
            if ( data.workdir === "" || data.workdir === " " ) {
                this.workdir = this.default_workdir;
            }

            if (data.action === "change-dir") {
                this.workdir = Config.name_project+"/"+Config.name_env+'/'+data.workdir+' $ ';
            }
            else {
                if ( Array.isArray(data.output) === true) {
                 var l = data.output.length;
                    for (var i = 0; i < l; i++) {
                        this.terminal.writeln(data.output[i]);
                    }

                }
                else {
                    var split_new_line = data.output.split("\n");
                    var split_new_line2 = data.output.split("\r\n");
                    var l_s = split_new_line.length;
                    var l_s2 = split_new_line2.length;
                    if  ( l_s !== l_s2 ) {
                        if (split_new_line.length > 2) {
                            for (var k = 0; k < l_s; k++) {
                                data.output = data.output.replace("\n", " ");
                            }
                        }
                    }
                    this.terminal.write('\r\n'+data.output);
                }

            }
            
            
            
            if ( data.finish_output === "true" ) {
                this.prompt(this.terminal, this.workdir);
                this.terminal.focus();
                
            }
        }
        
        
       
        
    }
    
    sendCommand(command) {
        var self = this;
        var action = "input-terminal";
        command = command.replace("\r", "");
        if (this.current.action === "run-inside-container" || Config.terminal.workdir !== "") {
            action = "input-inside-container";
        }
        var data = JSON.stringify({
            'uid': Config.env,
            "action" : action,
            "output" : [],
            "input" : command,
            "output_errors" : [],
            "workdir" : Config.terminal.workdir,
            "finish_output" : "true",
            "context" : self.context
        });
        this.socket.send(data);
    }
    
    runTerminal(display) {
        var self = this;
        var terminal_container = dom.get("#container-terminal");
        //if ( terminal_container )
        var term = new Terminal();
        this.terminal = term;
        var dom_terminal = dom.get("#terminal");
        term.resize(150, 18);
        term.open(dom_terminal);
        
        
        this.prompt(term, this.workdir);
        var command = "";
        term.onKey(function(e, d) {
            
            if ( dom_terminal.hasClass("edition-manuel") === false ) {
                term.focus();
                if (  e.domEvent.keyCode !== 8) {
                    command += e.key;
                }

                var directory_start = self.workdir;
                 const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey && !e.domEvent.ctrlKey && !e.domEvent.metaKey;
                if (e.domEvent.keyCode === 13) {
                    term.write('\r\n ');
                    term.blur();
                    if (command === "clear" || command === "cls") {
                        term.clear();
                        term.write(directory_start);
                    }
                    else {
                        if ( command.length > 0 && command !== "" && command !== " " ) {
                            self.sendCommand(command);
                        }
                        if( command.length === 0 || command === "" || command === " "  ) {
                            self.prompt(term, directory_start);
                        }
                    }

                    command = "";
                } 
                else if (e.domEvent.keyCode === 8) {
                    // Do not delete the prompt
                    if (term._core.buffer.x > (self.workdir.length-(command.length-1))  ) {
                        if (command.length > 2) {
                            command = command.substring(0, command.length-2);
                        }

                        term.write('\b \b');  
                    }
                } 
                else if (printable) {
                    term.write(e.key);
                }
                
            }
            else {
                term.blur();
            }
            
            
            
        });
    }
    
    resetTerminal(directory_start) {
        if (directory_start === "" || directory_start === " ") {
            directory_start = Config.name_project+"/"+Config.name_env+'/ $ ';
        }
        this.terminal.clear();
        this.prompt(this.terminal, directory_start);
    }
    
    prompt(term, directory) {
      term.write('\r\n'+directory);
    }
    
    runSocket(action, uid) {
        var self = this;
        var data = JSON.stringify({
            'uid': Config.env,
            "action" : action,
            "output" : [],
            "input" : "",
            "output_errors" : [],
            "workdir" : "",
            "finish_output" : "true",
            extra_data : {},
            "start_directory" : "",
            "context" : self.context
        });
        
        if (action === "run-container") {
            var data = JSON.stringify({
                'uid': Config.env,
                "action" : action,
                "output" : [],
                "input" : "",
                "output_errors" : [],
                "workdir" : "",
                "finish_output" : "true",
                "start_directory" : "",
                "context" : self.context
            });
        }
        console.log(data);
        
        
        this.socket.send(data);
        
        
        
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
    
    
}


invock.export("Workspace", Workspace);

invock.mountInStore({ parent : "body", root : "{% Workspace %}" }, "commands,data");

//invock.mount({ parent : "body", root : "{% Base %}" });