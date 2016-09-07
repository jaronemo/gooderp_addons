# -*- coding: utf-8 -*-

from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class partner(models.Model):
    _inherit = 'partner'
    _description = u'查看业务伙伴对账单'

    @api.multi
    def _set_receivable_init(self):
        if self.receivable_init:
            # 创建源单
            categ = self.env.ref('money.core_category_sale')
            source_id = self.env['money.invoice'].create({
            'name': "期初应收余额",
            'partner_id': self.id,
            'category_id': categ.id,
            'date': self.env.user.company_id.start_date,
            'amount': self.receivable_init,
            'reconciled': 0,
            'to_reconcile': self.receivable_init,
            'date_due': self.env.user.company_id.start_date,
            'state': 'draft',
             })

    @api.multi
    def _set_payable_init(self):
        if self.payable_init:
            # 创建源单
            categ = self.env.ref('money.core_category_purchase')
            source_id = self.env['money.invoice'].create({
            'name': "期初应付余额",
            'partner_id': self.id,
            'category_id': categ.id,
            'date': self.env.user.company_id.start_date,
            'amount': self.payable_init,
            'reconciled': 0,
            'to_reconcile': self.payable_init,
            'date_due': self.env.user.company_id.start_date,
            'state': 'draft',
             })

    receivable_init = fields.Float(u'应收期初', 
                                   digits=dp.get_precision('Amount'),
                                   inverse=_set_receivable_init)
    payable_init = fields.Float(u'应付期初', 
                           digits=dp.get_precision('Amount'),
                           inverse=_set_payable_init)


    @api.multi
    def partner_statements(self):
        self.ensure_one()
        view = self.env.ref('money.partner_statements_report_wizard_form')
        ctx = {'default_partner_id': self.id}
        if self.c_category_id.type == 'customer':
            ctx.update({'default_customer': True})
        else:
            ctx.update({'default_supplier': True})

        return {
            'name': u'业务伙伴对账单向导',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'views': [(view.id, 'form')],
            'res_model': 'partner.statements.report.wizard',
            'type': 'ir.actions.act_window',
            'context': ctx,
            'target': 'new',
        }


class bank_account(models.Model):
    _inherit = 'bank.account'
    _description = u'查看账户对账单'

    @api.multi
    def bank_statements(self):
        self.ensure_one()
        view = self.env.ref('money.bank_statements_report_wizard_form')

        return {
            'name': u'账户对账单向导',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'views': [(view.id, 'form')],
            'res_model': 'bank.statements.report.wizard',
            'type': 'ir.actions.act_window',
            'context': {'default_bank_id': self.id},
            'target': 'new',
        }
