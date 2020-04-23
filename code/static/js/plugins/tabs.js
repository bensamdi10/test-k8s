import invock, {dom, utils} from "invock-js";

dom.addPlugin("tabs", function(params) {
	var element = this;
	var parent = this.getParent();
    
    var init_tab = params.init_tab || 0;
    
    
	params = params || {};
    if ( typeof params.current_language === "undefined" ) {
        params.current_language = "en";
    }
    var name_space = params.name_space || "";
    var slider_tabs = dom.get(".slider-tabs-"+name_space);
    var width_tab = dom.get(".container-tabs-"+name_space).width();
    slider_tabs.findAll(".tab-"+name_space).css({ "width" : width_tab+"px" });
    var length_tabs = slider_tabs.findAll(".tab-"+name_space).length;
    var width_slider = (length_tabs*width_tab)+100;
    slider_tabs.css({ "width" : width_slider+"px" });
    if (element.findAll("li").length > 0) {
        element.findAll("li").eq(0).addClass("active");
    }
	element.findAll("ul.parent-ul > li:not(.no-tab)").on("click", function(evt) {
        var class_no_tab = this.hasClass("no-tab");
        if (!class_no_tab) {
            var index = this.index("li");
            element.find("li.active").removeClass("active");
            this.addClass("active");
            if ( current_language === "ar" ) {
                slider_tabs.animate(0.5, { left : width_tab*index, ease : "easeOutExpo" });
            }
            else {
               slider_tabs.animate(0.5, { left : -width_tab*index, ease : "easeOutExpo" });
            }
            
            
            if (typeof params.callback === "function") {
                params.callback.call(this, index, slider_tabs);
            }
        }
        
		evt.preventDefault();
	}, true);
    
    
    Element.prototype.goTab = function(index, name_space) {
        var slider_tabs = dom.get(".slider-tabs-"+name_space);
        var width_tab = dom.get(".container-tabs-"+name_space).width();
        this.find("li.active").removeClass("active");
        this.findAll("ul.parent-ul > li").eq(index).addClass('active');
        if ( params.current_language === "ar" ) {
            slider_tabs.animate(0.5, { left : width_tab*index, ease : "easeOutExpo" });
        }
        else {
           slider_tabs.animate(0.5, { left : -width_tab*index, ease : "easeOutExpo" }); 
        }
        
      
    };
    
    if ( init_tab < length_tabs) {
        element.goTab(init_tab, name_space);
    }
    
    
}); 