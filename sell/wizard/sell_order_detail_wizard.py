# -*- coding: utf-8 -*-

from datetime import date
from openerp import models, fields, api
from openerp.exceptions import except_orm


class sell_order_detail_wizard(models.TransientModel):
    _name = 'sell.order.detail.wizard'
    _description = u'销售明细表向导'

    @api.model
    def _default_date_start(self):
        return self.env.user.company_id.start_date

    @api.model
    def _default_date_end(self):
        return date.today()

    date_start = fields.Date(u'开始日期', default=_default_date_start)
    date_end = fields.Date(u'结束日期', default=_default_date_end)
    partner_id = fields.Many2one('partner', u'客户')
    goods_id = fields.Many2one('goods', u'产品')
    staff_id = fields.Many2one('staff', u'销售员')
    warehouse_id = fields.Many2one('warehouse', u'仓库')

    @api.multi
    def button_ok(self):
        '''向导上的确定按钮'''
        if self.date_end < self.date_start:
            raise except_orm(u'错误', u'开始日期不能大于结束日期！')

        domain = [('date', '>=', self.date_start),
                  ('date', '<=', self.date_end),
                  ]

        if self.goods_id:
            domain.append(('goods_id', '=', self.goods_id.id))
        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))
        if self.staff_id:
            domain.append(('staff_id', '=', self.staff_id.id))
        if self.warehouse_id:
            domain.append(('warehouse_id', '=', self.warehouse_id.id))

        view = self.env.ref('sell.sell_order_detail_tree')
        graph_view = self.env.ref('sell.sell_order_detail_graph')
        return {
            'name': u'销售明细表',
            'view_type': 'form',
            'view_mode': 'tree,graph',
            'view_id': False,
            'views': [(view.id, 'tree'),(graph_view.id,'graph')],
            'res_model': 'sell.order.detail',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'limit': 300,
        }
