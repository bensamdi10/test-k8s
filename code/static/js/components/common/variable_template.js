import invock, {Component} from "invock-js";

class VariableTemplate extends Component {
    
    
    constructor(params) {
        super(params);
        this.events = {
            "click .remove-item-variable" : "removeItem",
            "click .switcher" : "changeSwitcher",
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
    
    
    
    removeItem(evt, self) {
        var parent = this.closests(".inline-variable-item");
        if ( parent !== null ) {
            parent.animate(0.5, { "opacity" : 0, onComplete : function() {parent.remove(); } });
        }
    }
    
    render() {
        return `<div class="div-p half-p inline-variable-item">
            <span class="block absolute remove-item remove-item-variable pointer fade-hover"></span>
            <p>
                <label>ENV variable Name</label>
                <input type="text" name="name_var_{{props.count}}" placeholder="Example : HOST_NAME" class="required" data-rule="string" />
            </p>
            <p>
                <label>ENV variable Value</label>
                <input type="text" name="value_var_{{props.count}}" placeholder="Example : Cluster_ip" class="required" data-rule="string" />
            </p>
            <input type="hidden" value="" name="uid_var_{{props.count}}" />
            <div class="clr"></div>
            

            <div class="relative inline-item-center top20 center-auto">
                <label class="left">Secret Variable : </label>
                <div class="switcher {{props.secret_active|default:}} right" data-value="secret" data-yes="Yes" data-no="No">
                       <div class="handler animate"></div>
                       <div class="text-handler animate">{{props.secret_label|default:No}}</div>
                       <input type="hidden" name="secret_var_{{props.count}}" value="{{props.secret|default:}}" />
                </div>
                <div class="clr"></div>
            </div>

        </div>`;
    }
}

invock.export("VariableTemplate", VariableTemplate);