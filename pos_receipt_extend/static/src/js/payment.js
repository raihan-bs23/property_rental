odoo.define('pos_receipt_extend.PaymentScreen', function (require) {
   'use strict';
   var rpc = require('web.rpc')
   const PaymentScreen = require('point_of_sale.PaymentScreen');
   const Registries = require('point_of_sale.Registries');
   const { onMounted } = owl;

   const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
      setup() {
         super.setup();
      }
      async validateOrder(isForceValidate) {

         var orders = this.env.pos.selectedOrder
         const receipt_order = await super.validateOrder(...arguments);
         const odoo_pos_porder_id = this.env.pos.validated_orders_name_server_id_map[orders.name]
         var self = this;

         self.env.pos.order_name = null;

         this.env.services.rpc({
            model: 'pos.order',
            method: 'get_custom_data',
            args: [odoo_pos_porder_id]
         }).then(function (result) {
            self.env.pos.order_name = result.order_name;

         }).catch(function (error) {
            console.log('Failed to get order id at its offline ');
            throw error;
         });
         return receipt_order
      }
   }
   Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);
   return PaymentScreen;
});

