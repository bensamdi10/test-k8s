import invock, {dom, utils} from "invock-js";

dom.addPlugin("dropdown", function(params) {
	var element = this;
	var open = false;
	params = params || {};
	this.value = "sum";
    
    if ( params.hasOwnProperty("multiple") === false ) {
        params.multiple = false;
    }
    
    var type = params.type || "";
    var class_no_option = params.class_no_option || "no-option";
	var class_option = params.class_option || ".operation-option";
	var class_option_pur = class_option.substring(1, class_option.length);
	element.on("click", function(evt) {
		var target = evt.target;
		var text = target.text();
        var prev_value = this.data("value");
        var value = target.attr("data-value");
        
        if ( target.hasClass("validate-multiple") === false ) {
        
            if (target.getParent().hasClass(class_no_option)) {
            params.callback_no_option.call(this, value, target);
        }
            else {
            if (type === "layout" && !target.getParent().hasClass("value-dropdown") && value !== null) {
                if (!target.hasClass("layout-option")) {
                    text = target.getParent().find(".name-option").text();
                }
                element.find("."+class_option_pur).find('.text-option').text(text);
                var option_target = element.find(".value-dropdown .icon-layout-bleu");
                option_target.setAttr('class', '');
                option_target.addClass('icon-layout-bleu left '+value);
                element.setAttr("data-value", value);
                var name_element = element.data("name");
                element.find("input[name='"+name_element+"']").val(value);
                if (typeof params.callback === "function" && params.callback !== null) {
                    params.callback.call(this, value);
                }
            }
            if (!target.getParent().hasClass("value-dropdown") && type !== "layout") {
                if (target.hasClass(class_option_pur) || target.closests("."+class_option_pur) !== null && params.multiple === false) {
                    if (value === null && target.closests("."+class_option_pur) !== null) {
                        value = target.closests("."+class_option_pur).attr("data-value");
                    }
                    if (element.find(".value-dropdown").find(".operation-option") !== null) {
                        element.find(".value-dropdown").find(".operation-option").html("<div class='"+class_option_pur+" "+value+"'></div>");
                    }
                    else {
                        element.find(".value-dropdown").html("<div class='"+class_option_pur+" "+value+"'></div>");
                    }
                    
                    element.setAttr("data-value", value);

                    if (typeof params.after === "function" && params.after !== null) {
                        params.after.call(this, value, prev_value, text);
                        if (element.find(".active-view-default") !== null) {
                            element.find(".active-view-default").removeClass("active-view-default");
                        }
                        
                        target.addClass("active-view-default");
                    }
                    if (text !== "" && type !== "layout") {
                        element.find(".value-dropdown").find(class_option).text(text);
                    }
                }
            }
            if(open && element.find(".open-dropdown") && params.multiple === false ) {
                element.find(".list-dropdown").hide();
                element.removeClass("active");
                element.find(".list-dropdown").removeClass("open-dropdown");
                open = false;
            }
            else {
                element.find(".list-dropdown").show();
                element.addClass("active");
                element.find(".list-dropdown").addClass("open-dropdown");
                open = true;
            }
        }        
        }
	});
    
    var btn_validate = element.findAll(".validate-multiple");
    if ( btn_validate !== null )  {
        btn_validate.on("click", function(evt) {
           var checks = element.findAll("input[type='checkbox']");
           var l_checks = checks.length;
           var ids = [];
           for ( var i = 0; i < l_checks; i++ ) {
               var check_box = checks.eq(i);
               if ( check_box.checked === true ) {
                   ids.push(check_box.attr("name"))
               }
           }
            element.find(".list-dropdown").hide();
            element.removeClass("active");
            element.find(".list-dropdown").removeClass("open-dropdown");
            open = false;
            
            var type = this.data("type");
            
            if ( type !== null && type === "validate" ) {
                if ( typeof params.after === "function" && params.after !== null ) {
                    params.after.call(this, ids);
                }
            }
            
            
           
            
            
            
            
        });
    }
    
    
	
	return this;
}); 