
class Formatter:

    
    def order_object(self, order_list):
        for order in order_list:
            order = order['order']
            order.pop('accounted_tax')
            order.pop('affiliate_system')
            order.pop('billing_address1')
            order.pop('billing_address2')
            order.pop('billing_postcode')
            order.pop('billing_region')
            order.pop('business_vat_number')
            order.pop('buyer_email')
            order.pop('buyer_ip_address')
            order.pop('can_market_to_buyer')
            order.pop('dispatched_at')
            order.pop('download_attempts')
            order.pop('eu_resolved_country')
            order.pop('gateway')
            order.pop('gateway_transaction_ids')
            order.pop('gift_deliver_at')
            order.pop('giftee_email')
            order.pop('giftee_name')
            order.pop('order_custom_checkout_fields')
            order.pop('payment_method')
            order.pop('paypal_email')
            order.pop('settled_affiliate_fee')
            order.pop('settled_handling')
            order.pop('settled_shipping')
            order.pop('shipping_address1')
            order.pop('shipping_address2')
            order.pop('shipping_city')
            order.pop('shipping_country')
            order.pop('shipping_postcode')
            order.pop('shipping_region')


