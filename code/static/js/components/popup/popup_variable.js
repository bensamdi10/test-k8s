export default function PopupVariable() {
    return `
        <div class="overlay overlay-popup"></div>
        <div class="container-popup">
            <div class="popup relative center-auto border shadow">
                <div class="bleu-violet box15 uppercase relative">
                    <h3 class="bold">Create ENV Variables</h3>
                    <div class="close-popup absolute pointer fade-hover action-popup" data-action="close"></div>
                </div>
                <div class="content-popup">
                    <div class="tabs-ui bleu-violet-tabs uppercase none" id="container-pagination"></div>
                    <div class="clr"></div>
                    <div class="" id="container-form">
                        <form class="form-popup relative">
                            <div class="container-slider-environnement relative hidden">
                                <div class="relative slider-form-container">

                                   <div class="slide-form left">
                                        <div class="inputs box30">
                                            <div class="container-inputs">
                                                <h3 class="bleu-violet-color bottom30 bold">ENV Variables : </h3>

                                                <div id="env-variables-items" class='inline-parent-container relative'>

                                                    <div id="" class="relative subs-container">
                                                        {% for variable in props.data.env_variables %}
                                                            <div class="div-p half-p relative inline-variable-item inline-block-item">
                                                                <span class="block absolute remove-item pointer fade-hover" data-state="remove" data-uid="{{variable.uid}}" data-element="variable"></span>
                                                                <p>

                                                                    <label>ENV variable Name</label>
                                                                    <input type="text" name="name_var_{{variable.loop_counter|default:}}" placeholder="Example : HOST_NAME" class="required" data-rule="string" value="{{variable.name|default:}}" />
                                                                </p>

                                                                <p>
                                                                    <label>ENV variable Value</label>
                                                                    <input type="text" name="value_var_{{variable.loop_counter|default:}}" placeholder="Example : Cluster_ip" class="required" data-rule="string" value="{{variable.value}}" />
                                                                </p>
                                                                <input type="hidden" value="{{variable.uid}}" name="uid_var_{{variable.loop_counter|default:}}" />

                                                                <div class="clr"></div>
                                                                
                                                                <div class="relative inline-item-center top20 center-auto">
                                                                    <label class="left">Secret Variable : </label>
                                                                    <div class="switcher {{variable.secret_active|default:}} right" data-value="secret" data-yes="Yes" data-no="No">
                                                                           <div class="handler animate"></div>
                                                                           <div class="text-handler animate">{{variable.secret_label|default:No}}</div>
                                                                           <input type="hidden" name="secret_var_{{variable.loop_counter}}" value="{{variable.secret|default:}}" />
                                                                    </div>
                                                                    <div class="clr"></div>
                                                                </div>

                                                            </div>
                                                        {% endfor %}
                                                    </div>


                                                    <div class="align-center top30">
                                                        <input type="button" value="Add New Variable" data-action="add_variable" class="bleu-web bleu-web-shadow action-popup" />
                                                    </div>
                                                </div>

                                                <p>
                                                    <span class="asterix">*</span> <span>: Mandatory Field</span>
                                                </p>
                                            </div>

                                            <div class="align-center top30 bottom15">
                                                <input type="button" value="Close" class="fonce action-popup" data-action="close" />
                                                <input type="button" value="Validate" class="green green-shadow finish-slide" data-index="1" />

                                            </div>
                                        </div>

                                    </div>

                                    <div class="clr"></div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `;
}