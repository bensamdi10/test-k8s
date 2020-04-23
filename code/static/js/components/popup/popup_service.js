export default function PopupService() {
    return `
            <div class="overlay overlay-popup"></div>
            <div class="container-popup">
                <div class="popup relative center-auto border shadow">
                    <div class="bleu-violet box15 uppercase relative">
                        <h3 class="bold">Link Service CI / CD</h3>
                        <div class="close-popup absolute pointer fade-hover action-popup" data-action="close"></div>
                    </div>
                    <div class="content-popup">
                        <div class="tabs-ui bleu-violet-tabs uppercase" id="container-pagination"></div>
                        <div class="clr"></div>
                        <div class="" id="container-form">
                            <form class="form-popup relative">
                                <div class="relative hidden">
                                    <div class="relative slider-form-container">
                                        <div class="slide-form left">
                                            <div class="inputs box30">
                                                <div class="container-inputs">
                                                    <p>
                                                        <label>Name of Link <span class="asterix">*</span></label>
                                                        <input type="text" name="name" placeholder="Example : Project Startup" class="required" data-rule="string" value="{{props.data.name|default:}}" />
                                                    </p>

                                                    <p>
                                                        <label>Service CI  / CD <span class="asterix">*</span></label>
                                                        <select name="type" class="required" data-rule="string" data-value="{{props.data.type|default:}}">
                                                            <option value="">Select the Service CI / CD</option>
                                                            <option value="travis">Travic CI</option>
                                                            <option value="gitlab">Gitlab</option>

                                                        </select>
                                                    </p>

                                                    <p>
                                                        <label>On Branch <span class="asterix">*</span></label>
                                                        <input type="text" name="on_branch" placeholder="Example : master" class="required" data-rule="string" value="{{props.data.on_branch|default:}}" />
                                                    </p>

                                                    <p>
                                                        <span class="asterix">*</span> <span>: Mandatory Field</span>
                                                    </p>
                                                </div>

                                                <div class="align-center top30 bottom15">
                                                    <input type="button" value="Close" class="fonce action-popup" data-action="close" />
                                                    <input type="button" value="Next" class="bleu-violet bleu-violet-shadow next-slide" data-index="1" />

                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div class="slide-form left">
                                            <div class="inputs box30">
                                                <div class="container-inputs">
                                                    <div>
                                                            <p class='bottom20'>
                                                                <label>Select Template to Apply for Services</label>
                                                                <select name="template_services" data-rule="string" class="select-template">
                                                                    <option value="">Select The Template to Apply</option>
                                                                    {% for template in props.data.templates %}
                                                                        <option value="{{template.uid|default:}}">{{template.name|default:}}</option>
                                                                    {% endfor %}
                                                                </select>
                                                            </p>

                                                    </div>

                                                    <div class="accordeon-container relative">
                                                        <h3 class="uppercase bold accordeon-trigger">Before Install</h3>

                                                        <div id="before-install-inputs" class="relative container-commands-inputs">
                                                            <div class="parent-commands relative subs-container" data-type="before_install">
                                                                {% for before in props.data.before_install %}
                                                                     <div class="relative inline-command-inline-item inline-command_before_install inline-block-item">
                                                                        <span class="block absolute remove-item pointer fade-hover"></span>
                                                                        <p>
                                                                            <span class="block absolute remove-item pointer fade-hover" data-element="default"></span>
                                                                            <label>Command {{before.loop_counter}}</label>
                                                                            <input type="text" name="command_sc_{{before.loop_counter}}" data-rule="string" placeholder="example : docker push" value="{{before.command_sc|default:}}" />
                                                                        </p>
                                                                    </div>
                                                                {% endfor %}
                                                            </div>


                                                            <div class="align-center bottom20 top20">
                                                                <input type="button" class="bleu-web bleu-web-shadow action-popup" data-action="add_inline_command" value="Add New Command" />
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <div class="accordeon-container relative">
                                                        <h3 class="uppercase bold accordeon-trigger">Script</h3>

                                                        <div id="script-inputs" class="relative container-commands-inputs">
                                                            <div class="parent-commands relative subs-container" data-type="script">
                                                                {% for script in props.data.script %}
                                                                     <div class="relative inline-command-inline-item inline-command_script inline-block-item">
                                                                        <span class="block absolute remove-item pointer fade-hover"></span>
                                                                        <p>
                                                                            <span class="block absolute remove-item pointer fade-hover" data-element="default"></span>
                                                                            <label>Command {{script.loop_counter}}</label>
                                                                            <input type="text" name="command_sc_{{script.loop_counter}}" data-rule="string" placeholder="example : docker push" value="{{script.command_sc|default:}}" />
                                                                        </p>
                                                                    </div>
                                                                {% endfor %}
                                                            </div>
                                                            <div class="align-center bottom20 top20">
                                                                <input type="button" class="bleu-web bleu-web-shadow action-popup" data-action="add_inline_command" value="Add New Command" />
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <div class="accordeon-container relative">
                                                        <h3 class="uppercase bold accordeon-trigger">After success</h3>
                                                        <div id="after-success-inputs" class="relative container-commands-inputs">
                                                            <div class="parent-commands relative subs-container" data-type="after_success">
                                                                {% for after in props.data.after_success %}
                                                                     <div class="relative inline-command-inline-item inline-command_after_success inline-block-item">
                                                                        <span class="block absolute remove-item pointer fade-hover"></span>
                                                                        <p>
                                                                            <span class="block absolute remove-item pointer fade-hover" data-element="default"></span>
                                                                            <label>Command {{after.loop_counter}}</label>
                                                                            <input type="text" name="command_sc_{{after.loop_counter}}" data-rule="string" placeholder="example : docker push" value="{{after.command_sc|default:}}" />
                                                                        </p>
                                                                    </div>
                                                                {% endfor %}
                                                            </div>

                                                           <div class="align-center bottom20 top20">
                                                                <input type="button" class="bleu-web bleu-web-shadow action-popup" data-action="add_inline_command" value="Add New Command" />
                                                            </div>

                                                        </div>

                                                    </div>

                                                    <div class="accordeon-container relative">
                                                        <h3 class="uppercase bold accordeon-trigger">Deploy</h3>

                                                        <div id="deploy-inputs" class="relative container-commands-inputs">
                                                            <div class="parent-commands relative subs-container" data-type="deploy">
                                                                {% for deploy in props.data.deploy %}
                                                                     <div class="relative inline-command-inline-item inline-command_deploy inline-block-item">
                                                                        <span class="block absolute remove-item pointer fade-hover"></span>
                                                                        <p>
                                                                            <span class="block absolute remove-item pointer fade-hover" data-element="default"></span>
                                                                            <label>Command {{deploy.loop_counter}}</label>
                                                                            <input type="text" name="command_sc_{{deploy.loop_counter}}" data-rule="string" placeholder="example : docker push" value="{{deploy.command_sc|default:}}" />
                                                                        </p>
                                                                    </div>
                                                                {% endfor %}
                                                            </div>


                                                            <div class="align-center bottom20 top20">
                                                                <input type="button" class="bleu-web bleu-web-shadow action-popup" data-action="add_inline_command" value="Add New Command" />
                                                            </div>

                                                        </div>

                                                    </div>
                                                </div>
                                                
                                                <div class="align-center top30 bottom15">
                                                    <input type="button" value="Back" class="fonce back-slide" data-action="Back" />
                                                    <input type="button" value="Next" class="bleu-violet bleu-violet-shadow next-slide" data-index="2" />
                                                </div>

                                            </div>
                                        </div>

                                        <div class="slide-environnement slide-form left">
                                            <div class="inputs box30">
                                                <div class="container-inputs">
                                                    <h3 class="bleu-violet-color bottom30 bold">ENV Variables : </h3>
                                                    <div class="top20">
                                                        <select id="select-variales">
                                                            <option value="">Select The ENV Variables Already exist </option>
                                                            {% for varia in props.data.env_variables %}
                                                                <option value="{{varia.uid}}" data-name="{{varia.name}}">{{varia.name}}</option>
                                                            {% endfor %}
                                                        </select>
                                                        <div id="container-env-variables-items" class="relative top20"></div>
                                                    </div>

                                                    <div id="env-variables-items" class='inline-parent-container relative'>

                                                        <div id="" class="relative subs-container">
                                                            {% for variable in props.data.variables %}
                                                                <div class="div-p relative half-p inline-variable-item inline-block-item">
                                                                    <span class="block absolute remove-item pointer fade-hover" data-uid="{{variable.uid}}" data-element="variable"></span>
                                                                    <p>

                                                                        <label>ENV variable Name</label>
                                                                        <input type="text" name="name_var_{{variable.loop_counter|default:}}" placeholder="Example : HOST_NAME" class="required" data-rule="string" value="{{variable.name|default:}}" />
                                                                    </p>

                                                                    <p>
                                                                        <label>ENV variable Value</label>
                                                                        <input type="text" name="value_var_{{variable.loop_counter|default:}}" placeholder="Example : Cluster_ip" class="required" data-rule="string" value="{{variable.value}}" />
                                                                    </p>

                                                                    <div class="clr"></div>
                                                                    <div class="relative inline-item-center top20 center-auto">
                                                                        <label class="left">Secret Variable : </label>
                                                                        <div class="switcher {{variable.secret_active}} right" data-value="secret" data-yes="Yes" data-no="No">
                                                                               <div class="handler animate"></div>
                                                                               <div class="text-handler animate">{{variable.secret_label}}</div>
                                                                               <input type="hidden" name="secret_var_{{variable.loop_counter|default:}}" value="{{variable.secret}}" />
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
                                                    <input type="button" value="Back" class="fonce back-slide" />
                                                    <input type="button" value="Validate" class="green green-shadow finish-slide" data-index="3" />

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