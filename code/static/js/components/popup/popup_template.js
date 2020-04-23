export default function PopupTemplate() {
    return `
            <div class="overlay overlay-popup"></div>
            <div class="container-popup">
                <div class="popup relative center-auto border shadow">
                    <div class="bleu-violet box15 uppercase relative">
                        <h3 class="bold">Create New Template</h3>
                        <div class="close-popup absolute pointer fade-hover action-popup" data-action="close"></div>
                    </div>
                    <div class="content-popup">
                        <div class="tabs-ui bleu-violet-tabs uppercase none" id="container-pagination"></div>
                        <div class="clr"></div>
                        <div class="" id="container-form">
                            <form class="form-popup relative">

                                <div class="container-slider-environnement relative hidden">
                                    <div class="slider-environnement relative slider-form-container">
                                        
                                        <div class="slide-environnement slide-form left">
                                            <div class="inputs box30">
                                                <div class="container-inputs">
                                                    <p>
                                                        <label>Name of Template <span class="asterix">*</span></label>
                                                        <input type="text" name="name" placeholder="Example : example.com" class="required" data-rule="string" value="{{props.data.name|default:}}" />
                                                    </p>

                                                    <p>
                                                        <label>Description of Template </label>
                                                        <textarea name="description" placeholder="Example : example.com" class="" data-rule="string">{{props.data.description|default:}}</textarea>

                                                    </p>

                                                    <p class="none">
                                                        <input type="hidden" name="uid" value="{{props.data.uid}}" />
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