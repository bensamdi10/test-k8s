import invock, {Component} from "invock-js";

class CommandTemplate extends Component {
    
    
    constructor(params) {
        super(params);
        this.events = {
            "click .remove-item-command" : "removeItem"
        }
    }
    
    
    removeItem(evt, self) {
        var parent = this.closests(".inline-command-item");
        if ( parent !== null ) {
            parent.animate(0.5, { "opacity" : 0, onComplete : function() {parent.remove(); } });
        }
    }
    
    render() {
        return `<div class="div-p half-p top20 inline-command-item relative">
            <span class="block absolute remove-item remove-item-command pointer fade-hover"></span>
            <p class="relative">
                 
                <label>Instruction Type </label>
                <select name="command_type_{{props.count}}" data-rule="string" data-value="{{props.command_type|default:}}">
                    <option value="">Select Instruction Type</option>
                    <option value="FROM">FROM Command</option>
                    <option value="RUN">RUN Command</option>
                    <option value="WORKDIR">WORKDIR Command</option>
                    <option value="COPY">COPY Command</option>
                    <option value="EXPOSE">EXPOSE Command</option>
                    <option value="ENV">ENV Command</option>
                    <option value="ADD">ADD Command</option>
                    <option value="VOLUME">VOLUME Command</option>
                    <option value="USER">USER Command</option>
                    <option value="ARG">ARG Command</option>
                    <option value="CMD">Entrypoint Command</option>
                    <option value="ONBUILD">ONBUILD Command</option>
                    <option value="STOPSIGNAL">STOPSIGNAL Command</option>
                    <option value="HEALTHCHECK">HEALTHCHECK Command</option>
                    <option value="SHELL">SHELL Command</option>
                </select>
            </p>

            <p>
                <label>Value of Instruction </label>
                <input type="text" name="command_value_{{props.count}}" placeholder="Example : Cluster_ip" class="" data-rule="string" value="{{props.command_value|default:}}" />
            </p>

            <div class="clr"></div>

        </div>`;
    }
}

invock.export("CommandTemplate", CommandTemplate);