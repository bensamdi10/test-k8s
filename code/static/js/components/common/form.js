import invock, {Component} from "invock-js";

class FormCommon extends Component {
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
        
        this.observerChanges = null;
        this.type_submit = 'normal';
        this.url_ajax = "";
        this.data_ajax = null;
        this.observerAjax = null;
        this.observerBeforeAjax = null;
        this.send = true;
        this.slider_form = false;
        this.stepBeforeFinish = null;
    }
    
    init() {
        this.parent_form = this.parent
        
        this.parent_pagination = dom.get("#container-pagination");
        this.slides_length = this.parent.findAll(".slide-form").length;
        
        console.log(this.slides_length);
        this.type_slide = this.parent.data("type") || null;
        this.createSlider();
        this.adjustRightSide();
        this.events = { "click .next-slide" : "nextSlide", "click .finish-slide" : "finsishSlide", "click .back-slide": "backSlide"};
        this.runEvents(true);
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
    
    adjustRightSide() {
        if (this.parent_compliment !== null && typeof this.parent_compliment !== "undefined" && this.slider_form === true) {
            this.type_slide_side = this.parent_compliment.data("type") || null;
            var height_form = this.parent_form.height();
            this.parent_compliment.height(height_form);
            var diff_height = 0;
            for (var s = 0; s < this.slides_length; s++) {
                var slide_side = this.slides_side.eq(s);
                var height_slide = slide_side.height();
                diff_height = height_form - height_slide;
                slide_side.css({ "margin-top" : diff_height / 2 });
            }
            this.slides_side.css({"height" : height_form - (diff_height / 2)});
        }
        
    }
    
    createSlider() {
        var form = this.form = this.parent.find("form");
        
        var form_width = this.step = form.width();
        this.form.css({"width" : form_width});
        this.slides = form.findAll(".slide-form");
        this.slider = form.find(".slider-form-container");
        this.slides.css({ "width" : form_width });
        var inputs = this.slider.findAll(".inputs");
        var width_slider = (this.slides_length*form_width)+10;
        this.slider.width(width_slider);
        if (this.type_slide === "v"  ) {
            var form_height = this.step = form.height()+80;
            var height_slider = (this.slides_length*form_height)+10;
            inputs.css({ "height" :  form_height-260});
            this.slider.height(height_slider);
            this.slides.css({ "height" : form_height });
            this.parent_form.css({ "height" : form_height });
            this.slides.addClass("none-left");
        }
        if (this.type_slide === "h") {
            var form_height = form.height()+80;
            var height_slider = (this.slides_length*form_height)+10;
            inputs.css({ "min-height" :  form_height-260});
        }
        
        var container_inputs = form.findAll(".container-inputs");
        if ( container_inputs.length > 0 ) {
            var popup_height = dom.get(".popup").height()-300;
            container_inputs.css({ "min-height" :  popup_height});
        }
        
        this.createPagination();
        
        if (this.parent_compliment !== null && typeof this.parent_compliment !== "undefined" && this.slider_form === true) {
            // adjust slider right side
            this.step_side = this.parent_compliment.width();
            this.slides_side = this.parent_compliment.findAll(".slide-side");
            this.slider_side = this.parent_compliment.find("#slider-right-side");
            var width_slider_side = (this.slides_length*this.step_side)+10;
            this.slider_side.width(width_slider_side);
            this.slides_side.css({ "width" : this.step_side });
            if (this.type_slide_side === "v"  ) {
                this.step_side = this.parent_compliment.height()+30;
                var height_slider_side = (this.slides_length*this.step_side)+10;
                this.slider_side.height(height_slider_side);
                this.slides_side.css({ "height" : this.step_side });
                this.slides_side.addClass("none-left");
            }
        }
        
    }
    
    correctSliderDrag() {
        var container_draggable_element = dom.get("#container-elements");
        var height_container = container_draggable_element.height();
        if (height_container > 150) {
            var form = this.form;
            var inputs = this.slider.findAll(".inputs");
            var form_height = form.find('.slide-form').height();
            var new_height = form_height+height_container;
            inputs.eq(1).css({ "height" : new_height-220 });
            this.parent_form.css({ "height" : new_height });
            this.slides.eq(1).css({ "height" : new_height });
            
        }
        
    }
    
    createPagination() {
        if (this.parent_pagination !== null) {
            var ul = "<ul class='inline-block horizontal'></ul>";
            ul = this.parent_pagination.appendTo(ul);
            for (var i = 0; i < this.slides_length; i++) {
                var j = i+1;
                var li = "<li class='fade-hover'>Step "+j+"</li>";
                ul.appendTo(li);
            }
            ul.findAll("li").eq(0).addClass("active");
            this.parent_pagination.appendTo("<div class='clr'></div>");
        }
        if (this.slides_length === 2) {
            if (this.observerChanges !== null && typeof this.observerChanges === "function") {
                this.observerChanges.call(this, 0, this.slides);
            }    
        }
    }
    
    nextSlide(evt, self) {
        var index = self.index = parseInt(this.data("index"));
        var slide_parent = self.slides.eq(index-1);
        self.validateForm(slide_parent, function() {
            self.go(index, true, false);
        }, evt);
    }
    backSlide(evt, self) {
        self.index = self.index-1;
        var data_index = this.data("index");
        if (typeof data_index !== "undefined" && data_index !== null) {
            self.index = parseInt(data_index);
            var grand_parent = self.parent.getParent();
            if (grand_parent.hasClass("theme-success") || grand_parent.hasClass("theme-error")) {
                grand_parent.removeClass("theme-success");
                grand_parent.removeClass("theme-error");
                grand_parent.addClass("theme-bleu-clair");
            }
        }
        self.go(self.index, true, true);
    }
    
    finsishSlide(evt, self) {
        var index = self.index = parseInt(this.data("index"));
        var slide_parent = self.slides.eq(index-1);;
        
        self.validateForm(slide_parent, function() {
            if (self.type_submit === "normal") {
                self.form.submit();
            }
            else {   
                if (self.stepBeforeFinish !== null && typeof self.stepBeforeFinish === "function") { 
                    self.stepBeforeFinish.call(self);
                }
                else {
                    if (self.observerChanges !== null && typeof self.observerChanges === "function") {
                        self.observerChanges.call(this, index, self.slides.length);
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
                
                
            }
            
        }, evt);
    }
    
    send() {
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
    
    go(index, go_right, back) {
        if (back) {
            this.slider.find(".slide-form").eq(index-1).animate(0.9, { "opacity" : 1, ease : "easeOutExpo" });
            if (this.slider_form === true && this.slider_side !== null) {
                this.slider_side.find(".slide-side").eq(index-1).animate(0.9, { "opacity" : 1, ease : "easeOutExpo" });
            }
            
        }
        else {
            this.slider.find(".slide-form").eq(index-1).animate(0.9, { "opacity" : 0.3, ease : "easeOutExpo" });
            if (this.slider_form === true && this.slider_side !== null) {
                this.slider_side.find(".slide-side").eq(index-1).animate(0.9, { "opacity" : 0.3, ease : "easeOutExpo" });
            }
            
        }
        
        if (this.type_slide === "v" ) {
            
            this.slider.animate(0.9, { "top" : -this.step*index, ease : "easeOutExpo" });
        }
        else {
            this.slider.animate(0.9, { "left" : -this.step*index, ease : "easeOutExpo" });
        }
        
        var navigation_form = dom.get("#navigation-services");
        if (navigation_form !== null) {
            var items_navigation = navigation_form.findAll(".icon-service-block");
            var next_item = items_navigation.eq(index);
            var prev_item = items_navigation.eq(index-1);
            
            var max = items_navigation.length;
            for (var t = max-1; t > index; t--) {
                var sub_item = items_navigation.eq(t);
                var sub_sub_item = items_navigation.eq(t-1);
                if (sub_item !== null) {
                    sub_item.find(".icon-service").removeClass("active");
                    if (sub_sub_item !== null) {
                        sub_sub_item.find(".line-separ-service").removeClass("active");
                    }

                }
            }
            
            if (next_item !== null) {
                if (index > 0 &&  prev_item !== null) {
                    prev_item.find(".line-separ-service").addClass("active");
                }
                next_item.find(".icon-service").addClass("active");
            }
            
            
        }
        
        var li_pagination = this.parent_pagination.findAll("li");
        this.parent_pagination.find(".active").removeClass("active");
        li_pagination.eq(index).addClass("active");
        /*if (go_right) {
            this.slider_side.animate(0.6, { "left" : -this.step_side*index, ease : "easeOutSine" });
        }*/
            if (this.type_slide_side === "v" && go_right && this.slider_form === true) {
                this.slider_side.animate(0.9, { "top" : -this.step_side*index, ease : "easeOutExpo" });
            }
            if (this.type_slide_side !== "v" && go_right && this.slider_form === true) {
                this.slider_side.animate(0.9, { "left" : -this.step_side*index, ease : "easeOutExpo" });
            }
            if (this.observerChanges !== null && typeof this.observerChanges === "function") {
                this.observerChanges.call(this, index, this.slides.length);
            }
        
        
    }
    
    getChanges() {
        return { parent : this, index : this.index };
    }
    
    
    afterRender() {
        //this.init();
    }
    
}


invock.export("FormCommon", FormCommon);