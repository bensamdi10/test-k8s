export default function PopupContainer() {
    return `
    <div class="overlay overlay-popup"></div>
    <div class="container-popup">
        <div class="popup relative center-auto border shadow">
            <div class="bleu-violet box15 uppercase relative">
                <h3 class="bold">Create New Container</h3>
                <div class="close-popup absolute pointer fade-hover action-popup" data-action="close"></div>
            </div>
            <div class="content-popup">
                <div class="tabs-ui bleu-violet-tabs uppercase" id="container-pagination"></div>
                <div class="clr"></div>
                <div class="" id="container-form">
                    <form class="form-popup relative">
                        <div class=" relative hidden">
                            <div class="relative slider-form-container">
                                <div class="slide-form left">
                                    <div class="inputs box30">
                                        <div class="container-inputs">
                                            <p>
                                                <label>Name of Container <span class="asterix">*</span></label>
                                                <input type="text" name="name" placeholder="Example : Container Name" class="required" data-rule="string" value="{{props.data.name|default:}}" />
                                            </p>
                                            <p>
                                                <label>Base Image <span class="asterix">*</span></label>
                                                <input type="text" name="base_image" placeholder="Example : Project Startup" class="required" data-rule="string" value="{{props.data.base_image|default:}}" />
                                            </p>
                                            <p>
                                                <label>Type of Container <span class="asterix">*</span></label>
                                                <select name="type" class="required" data-rule="string" data-value="{{props.data.type|default:}}">
                                                    <option value="">Select the Type of Container</option>
                                                    <option value="code_base">Code Base</option>
                                                    <option value="software">Software</option>
                                                    <option value="plugin">Add-ons / Plugin</option>
                                                    <option value="cron">Cron Job</option>
                                                    <option value="others">Others</option>
                                                </select>
                                            </p>
                                            <p>
                                                <label>Source Code Clone</label>
                                                <input type="text" name="source" placeholder="Example : https://github.com/ID/APP" class="mandatory-input" data-rule="string" value="{{props.data.source|default:}}" />
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
                                            <p>
                                                <label>Port of Container <span class="asterix">*</span></label>
                                                <input type="text" name="port" placeholder="Example : 8010" class="required" data-rule="number" value="{{props.data.port|default:}}" />
                                            </p>
                                            <p>
                                                <label>Path of Volume</label>
                                                <input type="text" name="volume_path" placeholder="Example : temp/data" class="" data-rule="string"  value="{{props.data.volume_path|default:}}" />
                                            </p>
                                            <p>
                                                <label>CMD</label>
                                                <input type="text" name="cmd" placeholder="Example : python manage.py runserver" data-rule="string" value="{{props.data.cmd|default:}}" />
                                            </p>
                                            <p>
                                                <label>Name of Image in Docker Hub <span class="asterix">*</span></label>
                                                <input type="text" name="image_name" placeholder="Example : LOGIN/NAME_IMAGE" class="required" data-rule="string"  value="{{props.data.image_name|default:}}" />
                                            </p>
                                            <p>
                                                <span class="asterix">*</span> <span>: Mandatory Field</span>
                                            </p>
                                        </div>
                                        <div class="align-center top30 bottom15">
                                            <input type="button" value="Back" class="fonce back-slide"/>
                                            <input type="button" value="Next" class="bleu-violet bleu-violet-shadow next-slide" data-index="2" />
                                        </div>
                                    </div>
                                </div>

                                <div class="slide-form left">
                                    <div class="inputs box30">
                                        <div class="container-inputs">
                                             <h3 class="bleu-violet-color bottom30 bold">Container Template: </h3>
                                            <p>
                                                <label>Container Template </label>
                                                <select name="template" class="" data-rule="string" class="select-template">
                                                    <option value="">Select Container Template</option>
                                                    {% for temp in props.data.templates %}
                                                        <option value="{{temp.uid}}">{{temp.name}}</option>
                                                    {% endfor %}
                                                    <option value="blank">New Blank Template</option>
                                                </select>
                                            </p>
                                            <div id="commands-items">
                                                 <div id="" class="relative subs-container">
                                                    {% for command in props.data.commands %}
                                                        <div class="div-p half-p top20 inline-command-item relative inline-block-item">
                                                            <span class="block absolute remove-item remove-item-command pointer fade-hover"></span>
                                                            <p>
                                                                <label>Instruction Type </label>
                                                                <select name="command_type_{{command.loop_counter|default:}}" data-rule="string" data-value="{{command.command_type|default:}}">
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
                                                                <input type="text" name="command_value_{{command.loop_counter|default:}}" placeholder="Example : Cluster_ip" class="" data-rule="string" value="{{command.command_value|default:}}" />
                                                            </p>
                                                            <div class="clr"></div>
                                                        </div>
                                                    {% endfor %}
                                                </div>
                                                <div class="align-center top30">
                                                    <input type="button" value="Add New Command" data-action="add_command" class="bleu-web bleu-web-shadow action-popup" />
                                                </div>
                                            </div>
                                            <p>
                                                <span class="asterix">*</span> <span>: Mandatory Field</span>
                                            </p>
                                        </div>

                                        <div class="align-center top30 bottom15">
                                            <input type="button" value="Back" class="fonce back-slide" />
                                            <input type="button" value="Next" class="bleu-violet bleu-violet-shadow next-slide" data-index="3" />
                                        </div>
                                    </div>
                                </div>

                                 <div class="slide-form left">
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

                                            <div id="env-variables-items" class='inline-parent-container relative top20'>
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
                                            <input type="button" value="Validate" class="green green-shadow finish-slide" data-index="4" />
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