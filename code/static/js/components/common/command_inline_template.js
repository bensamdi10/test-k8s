import invock, {Component} from "invock-js";

class CommandInlineTemplate extends Component {
    
    
    constructor(params) {
        super(params);
        this.events = {
            "click .remove-inline-command-item" : "removeItem"
        }
    }
    
    
    removeItem(evt, self) {
        var parent = this.closests(".inline-command-inline-item");
        if ( parent !== null ) {
            parent.animate(0.5, { "opacity" : 0, onComplete : function() {parent.remove(); } });
        }
    }
    
    render() {
        return `<div class="relative inline-command-inline-item inline-command_{{props.type_command}}">
            <p>
                <span class="block absolute remove-item remove-inline-command-item pointer fade-hover" data-element="default"></span>
                <label>Command {{props.count}}</label>
                <input type="text" name="command_sc_{{props.count}}" data-rule="string" placeholder="example : docker push" value="{{props.command_sc|default:}}" />
            </p>
        </div>`;
    }
}

invock.export("CommandInlineTemplate", CommandInlineTemplate);