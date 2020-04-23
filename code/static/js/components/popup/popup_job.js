export default function PopupJob() {
    return `
            <div class="overlay overlay-popup"></div>
            <div class="container-popup">
                <div class="popup relative center-auto border shadow">
                    <div class="bleu-violet box15 uppercase relative">
                        <h3 class="bold">Create New Job</h3>
                       <div class="close-popup absolute pointer fade-hover action-popup" data-action="close"></div>
                    </div>
                    <div class="content-popup">
                        <div class="tabs-ui bleu-violet-tabs uppercase none" id="container-pagination"></div>
                        <div class="clr"></div>

                        <div class="" id="container-form">
                            <form class="form-popup relative">
                                <div class="relative hidden">
                                    <div class="relative slider-form-container">
                                        <div class="slide-form left">
                                            <div class="inputs box30">
                                                <div class="container-inputs">
                                                    <p>
                                                        <label>Name of Job <span class="asterix">*</span></label>
                                                        <input type="text" name="name" placeholder="Example : example.com" class="required" data-rule="string" value="{{props.data.name|default:}}" />
                                                    </p>

                                                    <p>
                                                        <label>type of Job <span class="asterix">*</span></label>
                                                        <select id="select-type-job" name="type" class="requried" data-rule="string" data-value="{{props.data.type|default:}}">
                                                            <option value="">Select The Type of Job</option>
                                                            <option value="cron">Cron</option>
                                                            <option value="job">Job</option>
                                                            <option value="deamon">Deamon</option>
                                                        </select>
                                                    </p>

                                                    <p class="cron-param none">
                                                        <label>schedule of Job </label>
                                                        <input type="text" name="schedule" placeholder="Example : /* *2 * * *" class="mandatory-input" data-rule="string" value="{{props.data.schedule|default:}}" />
                                                    </p>




                                                    <p>
                                                        <label>Restart Policy of Job <span class="asterix">*</span></label>
                                                        <select name="restart_policy" class="requried" data-rule="string" data-value="{{props.data.restart_policy|default:}}">
                                                            <option value="">Select The Restart Policy of Job</option>
                                                            <option value="OnFailure">On Failure</option>
                                                            <option value="Never">Never</option>
                                                            <option value="always">Always</option>
                                                        </select>
                                                    </p>

                                                    <p class='none'>
                                                        <label>Back Off Limit of Job </label>
                                                        <input type="text" name="back_off_limit" placeholder="Example : 5" class="mandatory-input" data-rule="number" value="{{props.data.back_off_limit|default:5}}" />
                                                    </p>

                                                    <p>
                                                        <label>Container Image of Job </label>
                                                        <input type="text" name="container_image" placeholder="Example : DOCKER_ID/IMAGE_NAME" class="" data-rule="string" value="{{props.data.container_image|default:}}" />
                                                    </p>

                                                    <p>
                                                        <label>Container </label>
                                                        <select name="container" data-rule="string" data-value="{{props.data.container|default:}}">
                                                            <option value="">Select Container</option>
                                                            {% for sub_container in props.data.containers %}
                                                                <option value="{{sub_container.uid}}">{{sub_container.name}}</option>
                                                            {% endfor %}

                                                        </select>
                                                    </p>



                                                    <p>
                                                        <label>Command of Job </label>
                                                        <input type="text" name="command" placeholder="Example : apt-get install git" class="" data-rule="string" value="{{props.data.command|default:}}" />
                                                    </p>

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