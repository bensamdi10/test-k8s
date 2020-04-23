import invock, {Component} from "invock-js";

class EnvVariableTemplate extends Component {
    
    
    constructor(params) {
        super(params);
        this.events = {
            "click .remove-item-env-variable" : "removeItem"
        }
    }
    
    
    removeItem(evt, self) {
        var parent = this.closests(".inline-env-variable-item");
        if ( parent !== null ) {
            parent.animate(0.5, { "opacity" : 0, onComplete : function() {
                parent.remove();    
            } });
        }
        
        
    }
    render() {
        console.log(this.props);
        return `<div class="div-p half-p inline-env-variable-item" data-uid="{{props.uid}}">
            <span class="block absolute remove-item remove-item-env-variable pointer fade-hover"></span>
            <span>{{props.name}}</span>
            <div class="clr"></div>
        </div>`;
    }
}

invock.export("EnvVariableTemplate", EnvVariableTemplate);