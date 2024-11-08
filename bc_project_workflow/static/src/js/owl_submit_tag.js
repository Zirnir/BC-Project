/** @odoo-module **/

import { Component, onWillStart, useRef, useState } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';

export class SubmitModal extends Component {

    static template = 'submit_modal.SubmitModal';

    static props = { test_id:Number};

    setup() {
        console.log("ok", this.props.test_id);
        this.orm = useService('orm');
        this.tags = [];
        this.state = useState({
            isButtonVisible: true,
            isModalVisible: false,
            justify: '',
            selectedTags: []
        });


        onWillStart(() => this.tagCollector());
    }

    hideButton(){
        this.state.isButtonVisible = false;
    }

    showModal() {
        this.state.isModalVisible = true;
        console.log(this.state.isModalVisible);
    }

    closeModal() {
        this.state.isModalVisible = false;
    }

    async tagCollector() {
        this.tags = await this.orm.call('test.tag', 'search_read', [], {
            fields: ['id' , 'name'],
        });
        console.log(this.tags);
    }

    async accepted(){
        return this.orm.call("project.task.test", "accepted", [this.props.test_id]).then(() => {
            this.closeModal();
            this.hideButton();
            console.log("azerty");
        });
    }
    
    async submitForm() {
        const tag_id = this.state.selectedTags;
        const justify = this.state.justify;
        const test_id = this.props.test_id;
        if (justify && tag_id) {
            return this.orm.call("project.task.test", "refused", [test_id,justify,tag_id]).then(() => {
                this.closeModal();
                this.hideButton();
            });
        }
        if (!justify || !test_id) {
            alert("Select a tag and justify.");
        }
    }

    get getTags() {
        return this.tags
    }
}
registry.category("public_components").add("submit_modal.SubmitModal", SubmitModal);