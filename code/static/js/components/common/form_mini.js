import invock, {Component} from "invock-js";
import Plugins from "../../plugins/plugins";

class FormMini extends Component {
    constructor(params) {
        super(params);
        this.slides_length = 0;
        this.alias = "FormCommon";
        this.slides = [];
        this.slides_side = [];
        this.slider = null;
        this.slider_side = null;
        this.form = null;
        this.step = 0;
        this.step_side = 0;
        this.type_slide = "h";
        this.type_slide_side = "h";
        this.index = 0;
        this.state = { title : "", theme : ""  };
        this.events = { "click .finish-slide" : "finsishSlide"};
        this.observerChanges = null;
        this.type_submit = 'normal';
        this.url_ajax = "";
        this.data_ajax = null;
        this.observerAjax = null;
        this.observerBeforeAjax = null;
        this.send = true;
        this.slider_form = false;
    }
    
    init() {
        this.parent_form = this.parent.find("#left-form");
        this.form = this.parent.find("form");
        this.preFill();
    }
    
    preFill() {
        
        var selects = this.parent_form.findAll("select");
        var l_selects = selects.length;
        for (var i = 0; i < l_selects; i++) {
            var select = selects.eq(i);
            var value = select.attr("value");
            var option_target = select.find("option[value='"+value+"']");
            if (option_target !== null) {
                option_target.setAttr("selected", "selected");
            }
        }
    }
    
    finsishSlide(evt, self) {
        var index = self.index = parseInt(this.data("index"));
        var slide_parent = self.parent_form;
        self.validateForm(slide_parent, function() {
            if (self.type_submit === "normal") {
                self.form.submit();
            }
            else {
                if (self.observerBeforeAjax !== null && typeof self.observerBeforeAjax === "function") {
                    self.observerBeforeAjax.call(self);
                }
                if (self.send) {
                    self.http.url = self.url_ajax;
                    self.http.post(self.data_ajax, function(response) {
                        if (self.observerAjax !== null && typeof self.observerAjax === "function") {
                            self.observerAjax.call(self, response);
                        }
                    }, function(http, xhr, error) {
                        if (typeof self.errorCallback !== "undefined" && self.errorCallback !== null) {
                            self.errorCallback.call(self, xhr, error, http);
                        }
                        
                        
                    } );
                }
                
            }
            
        }, evt);
    }
    
    validateForm(form, callback, evt) {
        var self = this;
        form.runPlugin("validator", {
            parent : form,
            valid : function(response) {
                if (response) {
                    if (typeof callback === "function" && callback !== null) {
                        callback.call(self, this);
                    }
                }
            },
            error : function() {
                evt.preventDefault();
                return false;
            }
        });
    }
    
    
    getChanges() {
        return { parent : this, index : this.index };
    }
    
}


invock.export("FormMini", FormMini);

invock.mount({ parent : "#container-form", root : "{% FormMini parent_name='#container-form' %}" });