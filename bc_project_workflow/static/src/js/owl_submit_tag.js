/** @odoo-module **/

import { Component, onWillStart, useState, onWillDestroy } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';

export class SubmitModal extends Component {

    static template = 'submit_modal.SubmitModal';

    static props = { test_id:Number};

    setup() {
        this.orm = useService('orm');
        this.tags = [];
        this.state = useState({
            isButtonVisible: true,
            isModalVisible: false,
            justify: '',
            selectedTags: [],
            isInvalidJustify: false,
            isInvalidTag: false,
            file: null,
            file_name:'',
        });

        onWillStart(() => this.tagCollector());
        
    }

    handleFileChange(ev) {
        const file = ev.target.files[0];
        this.state.file_name = file.name;
        if (file) {
            const reader = new FileReader(); 

            reader.onloadend = () => {
                const fileAsBase64 = reader.result.split(',')[1]; 
                
                this.state.file = fileAsBase64;
            };

            reader.readAsDataURL(file);
        }
    }

    hideButton(){
        this.state.isButtonVisible = false;
    }

    showModal() {
        this.state.isModalVisible = true;
    }

    closeModal() {
        this.state.isModalVisible = false;
    }

    async tagCollector() {
        this.tags = await this.orm.call('test.tag', 'search_read', [], {
            fields: ['id' , 'name'],
        });
    }

    async accepted(){
        return this.orm.call("project.task.test", "accepted", [this.props.test_id]).then(() => {
            this.closeModal();
            this.hideButton();
        });
    }
    
    async submitForm() {
        const tag_id = this.state.selectedTags;
        const justify = this.state.justify;
        const test_id = this.props.test_id;
        const file_name = this.state.file_name;
        if (justify && tag_id) {
            return this.orm.call("project.task.test", "refused", [test_id,justify,tag_id,this.state.file,file_name]).then(() => {
                this.closeModal();
                this.hideButton();
            });
        }
        if (!justify || tag_id == '') {

            if (!justify){
                this.state.isInvalidJustify = true;
            }
            if (tag_id == ''){
                this.state.isInvalidTag = true;
            }
        }
    }

    get getTags() {
        return this.tags
    }
}
registry.category("public_components").add("submit_modal.SubmitModal", SubmitModal);