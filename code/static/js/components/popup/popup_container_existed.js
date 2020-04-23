export default function PopupContainerExisted() {
    return `
            <div class="overlay overlay-popup"></div>
            <div class="container-popup">
                <div class="popup relative center-auto border shadow">
                    <div class="bleu-violet box15 uppercase relative">
                        <h3 class="bold">Add Container</h3>
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
                                                        <label>Container </label>
                                                        <select name="container" data-rule="string" data-value="{{props.data.container|default:}}">
                                                            <option value="">Select Container</option>
                                                            {% for sub_container in props.data.containers %}
                                                                <option value="{{sub_container.uid}}">{{sub_container.name}}</option>
                                                            {% endfor %}

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