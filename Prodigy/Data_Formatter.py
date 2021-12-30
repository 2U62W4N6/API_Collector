
import pandas as pd

class Formatter:

    
    def order_object(self, order_list):
        orders = pd.DataFrame(order_list)
        orders = orders['order'].apply(pd.Series)
        orders = orders.drop(columns=[
            'accounted_tax',
            'affiliate_system',
            'billing_address1',
            'billing_address2',
            'billing_postcode',
            'billing_region',
            'business_vat_number',
            'buyer_email',
            'buyer_ip_address',
            'can_market_to_buyer',
            'dispatched_at',
            'download_attempts',
            'eu_resolved_country',
            'gateway',
            'gateway_transaction_ids',
            'gift_deliver_at',
            'giftee_email',
            'giftee_name',
            'order_custom_checkout_fields',
            'payment_method',
            'paypal_email',
            'settled_affiliate_fee',
            'settled_handling',
            'settled_shipping',
            'shipping_address1',
            'shipping_address2',
            'shipping_city',
            'shipping_country',
            'shipping_postcode',
            'shipping_region',
        ])
        carts = pd.concat([orders[['id']], orders['cart'].apply(pd.Series)], axis=1)
        carts = carts.explode('cart_items')
        carts = pd.concat([carts, carts['cart_item'].apply(pd.Series)], axis=1)
        carts = carts.drop(columns=['cart_items', 'cart_items'])
        return orders, carts
