odoo.define('pwc_tasks/static/src/js/message.js', function (require) {
    'use strict';
    const {
        registerClassPatchModel,
        registerFieldPatchModel,
    } = require('mail/static/src/model/model_core.js');
    const { attr } = require('mail/static/src/model/model_field.js');

    registerClassPatchModel('mail.message', 'pwc_tasks/static/src/js/message.js', {

        convertData(data) {
            const data2 = this._super(data);
            if ('email_cc_ids' in data) {
                data2.email_cc_ids = data.email_cc_ids;
            }
            return data2;
        },
    });
    registerFieldPatchModel('mail.message', 'pwc_tasks/static/src/js/message.js', {
        email_cc_ids: attr({
            default: false,
        }),
    });
});