import {Http} from "invock-js";
dom.addPlugin("slider", function(params) {
    var element = this;
    var name_space = params.name_space || "";
    var action_apply = params.actions_apply || true;
    var step = 0;
    var index = 0;
    var count = 0;
    var http = new Http();
    
    var container = dom.get(".container-slider-"+name_space);
    var slider = null;
    var overlay = null;
    if ( container !== null ) {
        overlay = container.closests(".overlay");
        show(overlay);
        slider = container.find(".slider-"+name_space);
        if (  slider !== null ) {
            count = slider.findAll(".slide-"+name_space).length;
            createSlider(container, slider);
        }
    }
    
    function createSlider(container, slider) {
        step = container.width();
        slider.width(step*count);
        slider.findAll(".slide-"+name_space).css({ "width" : step });
        
        applyActions(slider);
    }
    
    
    function applyActions(slider) {
        var next = dom.get(".action-"+name_space+"[data-action='next']");
        var prev = dom.get(".action-"+name_space+"[data-action='prev']");
        var close = dom.get(".action-"+name_space+"[data-action='close']");
        
        if (next !== null) {
            next.on("click", function() {
                if ( index < (count - 1) ) {
                    index = index+1;
                    go(index, slider);
                }
                else {
                    disableTour();
                    closeTour();
                }
            });
        }
        if (prev !== null) {
            prev.on("click", function() {
                if ( index > 0 ) {
                    index = index - 1;
                    go(index, slider);
                }
            });
        }
        
        if (close !== null) {
            close.on("click", function() {
                disableTour();
                closeTour();
            });
        }
    }
    
    function closeTour() {
        if ( overlay !== null ) {
            overlay.remove();
        }
    }
    
    function show(overlay) {
        if ( overlay !== null ) {
            overlay.fadeIn();
        }
    }
    
    function go(index, slider) {
        if ( params.lang === "ar" ) {
            slider.animate(0.5, { left : step*index, ease : "easeOutExpo" });
            //slider.animate(0.5, { right : -(index*step), ease : "easeOutExpo"  });
        }
        else {
            slider.animate(0.5, { left : -(index*step), ease : "easeOutExpo"  });
        }
        
    }
    
    function disableTour() {
        var url = params.url || "/api/account/disable-tour-site/";
        http.url = url;
        http.fetch(function(response) {
            if ( response.status === "success" ) {
                closeTour();
            }
        });
    }
    
    
});