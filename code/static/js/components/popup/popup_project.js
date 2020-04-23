export default function PopupProject() {
    return `
        <div class="overlay overlay-popup"></div>
        <div class="container-popup">
            <div class="popup relative center-auto border shadow">
                <div class="bleu-violet box15 uppercase relative">
                    <h3 class="bold">Create New Project</h3>
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
                                                    <label>Name of Project <span class="asterix">*</span></label>
                                                    <input type="text" name="name" placeholder="Example : Project Startup" class="required" data-rule="string" value="{{props.element.name|default:}}" />
                                                </p>

                                                <p>
                                                    <label>Description of project <span class="asterix">*</span></label>
                                                    <textarea name="description" placeholder="Example : Lorem ipsum" class="required" data-rule="string">{{props.element.description|default:}}</textarea>
                                                </p>

                                                <p>
                                                    <label>NameSpace of Project <span class="asterix">*</span></label>
                                                    <input type="text" name="name_space" placeholder="Example : com.project.statup" class="required" data-rule="string" value="{{props.project.name_space|default:}}" />
                                                </p>

                                                <p>
                                                    <label>Cloud Provider <span class="asterix">*</span></label>
                                                    <select name="provider" class="requried" data-rule="string" data-value="{{props.element.provider|default:}}">
                                                        <option value="">Select the Cloud Provider</option>
                                                        <option value="Google_cloud">Google Cloud</option>
                                                        <option value="aws">AWS</option>
                                                        <option value="heroku">Heroku</option>
                                                        <option value="digital_ocean">Digital Ocean</option>
                                                        <option value="minikube">Minikube</option>
                                                    </select>
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