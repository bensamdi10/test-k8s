import invock, {Component} from "invock-js";

class ContainerTemplate extends Component {
    
    
    constructor(params) {
        super(params);
        this.events = {
            "click .remove-item-container" : "removeItem"
        }
    }
    
    
    removeItem(evt, self) {
        var parent = this.closests(".inline-container-item");
        if ( parent !== null ) {
            parent.animate(0.5, { "opacity" : 0, onComplete : function() {parent.remove(); } });
        }
    }
    
    render() {
        return `<div class="div-p third-p top20 inline-container-item relative">
                <span class="block absolute remove-item pointer fade-hover"></span>
                <p>
                    <label>Container </label>
                    <select name="container_name_{{props.count}}" data-rule="string" data-value="">
                        <option value="">Select Container</option>
                        {% for sub_container in props.list %}
                            <option value="{{sub_container.uid}}">{{sub_container.name}}</option>
                        {% endfor %}
                    </select>
                </p>

                <p>
                    <label>Path</label>
                    <input type="text" name="container_path_{{props.count}}" placeholder="Example : /home?(.*)" class="" data-rule="string" />
                </p>

                <p>
                    <label>Port </label>
                    <input type="text" name="container_port_{{props.count}}" placeholder="Example : 3000" class="" data-rule="number" />
                </p>

                <div class="clr"></div>

            </div>`;
    }
}

invock.export("ContainerTemplate", ContainerTemplate);