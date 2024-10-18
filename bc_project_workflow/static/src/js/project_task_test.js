/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TaskTest = publicWidget.Widget.extend({ 

    selector : '.testing',

    events: {
        'click .accepted_test': '_onAccepted',
        'click .refused_test': '_onRefused',
        'click .description_form' : '_onDescription',
        'submit .refused_partner_assign_form': '_onSubmitRefusal',
    },


    init() {
        console.log("Init démarer");
        this._super(...arguments);
        this.orm = this.bindService("orm");
    },

    /**
     * @private
     * @param {jQuery} $btn
     * @param {function} callback
     * @returns {Promise}
     */
    _buttonExec: function ($btn, callback) {
        $btn.prop('disabled', true);
        return callback.call(this).catch(function (e) {
            $btn.prop('disabled', false);
            if (e instanceof Error) {
                return Promise.reject(e);
            }
        });
    },

    /**
     * @private
     * @returns {Promise}
     */
    _accepted: function (taskTestId) {
        console.log("_accepted démarer " + taskTestId);
        return this.orm.call("project.task.test", "accepted", [[taskTestId]]);
    },

    /**
     * @private
     * @returns {Promise}
     */
    _refused: function (taskTestId, justify) {
        console.log("_refused démarer " + taskTestId);
        return this.orm.call("project.task.test", "refused", [[taskTestId],justify]);
    },

    /**
     * @private
     * @param {Event} ev
     */
    _onDescription: function (ev) {
        console.log("_onDescription");
        ev.preventDefault();
        ev.stopPropagation();
        
        const $link = $(ev.currentTarget); 
        const testId = $link.data('test-id'); 

        const $modal = $link.closest('.description').find('.modal_test_description');

        $modal.find('textarea[name="description"]').val(testId);
        $modal.modal('show');
    },

    /**
     * @private
     * @param {Event} ev
     */
    _onAccepted: function (ev) {
        console.log("_onAccepted");
        ev.preventDefault();
        ev.stopPropagation();
        const taskTestId = $(ev.currentTarget).closest('.testing').data('test-id');
        this._buttonExec($(ev.currentTarget), () => this._accepted(taskTestId));
    },
    

    /**
     * @private
     * @param {Event} ev
     */
    _onRefused: function (ev) {
        console.log("_onRefused");
        ev.preventDefault();
        ev.stopPropagation();
        const $modal = $(ev.currentTarget).closest('.testing').find('.modal_test_justify_refused');
        $modal.modal('show');
    },

    /**
     * @private
     * @param {Event} ev
     */
    _onSubmitRefusal: function (ev) {
        console.log("_onSubmitRefusal");
        ev.preventDefault();  
        const $form = $(ev.currentTarget);
        const taskTestId = $form.closest('.testing').data('test-id');
        const justify = $form.find('#comment_refused').val(); 

        console.log("Task ID:", taskTestId, "Justification:", justify); 
        if (!justify) {
            console.log("La justification est obligatoire");
            alert("La justification est obligatoire. Veuillez entrer une raison.");
            ev.stopPropagation();
            $form.find('#comment_refused').focus();
            return;
        }
        if (justify) {
            this._buttonExec($form.find('button[type="submit"]'), () => {
                return this._refused(taskTestId, justify).then(() => {
                    $form.closest('.modal').modal('hide');
                    console.log("Justification soumise et modal fermée.");
                });
            });
        }
    },
})