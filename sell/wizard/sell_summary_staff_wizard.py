# -*- coding: utf-8 -*-

from datetime import date
from openerp import models, fields, api
from openerp.exceptions import except_orm


class sell_summary_staff_wizard(models.TransientModel):
    _name = 'sell.summary.staff.wizard'
    _description = u'销售汇总表（按销售人员）向导'

    @api.model
    def _default_date_start(self):
        return self.env.user.company_id.start_date

    @api.model
    def _default_date_end(self):
        return date.today()

    date_start = fields.Date(u'开始日期', default=_default_date_start)
    date_end = fields.Date(u'结束日期', default=_default_date_end)
    staff_id = fields.Many2one('staff', u'销售人员')
    goods_id = fields.Many2one('goods', u'商品')
    goods_categ_id = fields.Many2one('core.category', u'商品类别',
                                     domain=[('type', '=', 'goods')],
                                     context={'type': 'goods'})
    warehouse_id = fields.Many2one('warehouse', u'仓库')

    @api.multi
    def button_ok(self):
        if self.date_end < self.date_start:
            raise except_orm(u'错误', u'开始日期不能大于结束日期！')
        read_fields = ['date_start', 'date_end', 'staff_id',
                       'goods_id', 'goods_categ_id', 'warehouse_id']
        return {
            'name': u'销售汇总表（按销售人员）',
            'view_mode': 'tree',
            'res_model': 'sell.summary.staff',
            'type': 'ir.actions.act_window',
            'context': self.read(read_fields)[0],
        }
