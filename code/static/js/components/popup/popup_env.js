export default function PopupEnvironnement() {
    return `
            <div class="overlay overlay-popup"></div>
            <div class="container-popup">
                <div class="popup relative center-auto border shadow">
                    <div class="bleu-violet box15 uppercase relative">
                        <h3 class="bold">Create New Environnement</h3>
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
                                                        <label>Name of Environnement <span class="asterix">*</span></label>
                                                        <input type="text" name="name" placeholder="Example : Project Startup" class="required" data-rule="string" value="{{props.element.name|default:}}" />
                                                    </p>
                                                    <p>
                                                        <label>Type of Environnement <span class="asterix">*</span></label>
                                                        <select name="type" class="required" data-rule="string" data-value="{{props.element.type|default:}}">
                                                            <option value="">Select the Type of Environnement</option>
                                                            <option value="developpement">Developpement</option>
                                                            <option value="test">Test</option>
                                                            <option value="production">Production</option>
                                                            <option value="others">Others</option>
                                                        </select>
                                                    </p>

                                                    <p>
                                                        <span class="asterix">*</span> <span>: Mandatory Field</span>
                                                    </p>
                                                </div>
                                                <div class="align-center top30 bottom15">
                                                    <input type="button" value="Close" class="fonce action-popup" data-action="close" />
                                                    <input type="button" value="Save" class="green green-shadow finish-slide" data-index="1" />

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