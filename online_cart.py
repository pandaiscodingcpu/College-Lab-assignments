def compute_cart_total(*costs):
    subtotal = 0  # summing up all product costs
    for price in costs:
        subtotal += price
    print(f"Subtotal for items: Rs. {subtotal}")
    return subtotal


def finalize_order(initial_total):
    # discount for orders above Rs. 250 is 8%
    order_discount = 0
    if initial_total > 250:
        order_discount = initial_total * 0.08
        initial_total -= order_discount
        print("Congrats! 8% discount applied for orders above Rs. 250.")

    payment_type = input("Choose payment method (card/cash): ").strip().lower()
    shipping_fee = 0

    if payment_type == "card":
        print("Card payment selected: Free shipping unlocked!")
    else:
        shipping_fee = 40  # Rs. 40 shipping for cash orders 
        print("Cash payment selected: Shipping fee Rs. 40 added.")

    bill_amount = initial_total + shipping_fee

    # Promo codes
    valid_codes = {"flash10": 0.10, "djsoffer": 0.15, "save5": 0.05}
    promo_entered = input("Enter promo code or 'none' to skip: ").strip().lower()

    promo_discount = 0
    if promo_entered != "none":
        if promo_entered in valid_codes:
            promo_discount = bill_amount * valid_codes[promo_entered]
            print(f"Promo '{promo_entered}' applied! Discount: Rs. {promo_discount:.2f}")
        else:
            print("Promo code not recognized!")

    bill_amount -= promo_discount

    # Membership plan: Rs. 120 for 6 months
    member_choice = input("Subscribe to premium membership for Rs. 120/6 months? (y/n): ").strip().lower()
    membership_fee = 0
    if member_choice == 'y':
        membership_fee = 120
        bill_amount += membership_fee

    # Display final summary
    print("\n" + "="*42)
    print("FINAL BILL SUMMARY")
    print("="*42)
    print(f"Subtotal:\t\t\tRs. {initial_total + order_discount:.2f}")
    if order_discount > 0:
        print(f"Order discount:\t\t\t-Rs. {order_discount:.2f}")
    print(f"Shipping fee:\t\t\tRs. {shipping_fee:.2f}")
    if promo_discount > 0:
        print(f"Promo discount:\t\t\t-Rs. {promo_discount:.2f}")
    if membership_fee > 0:
        print(f"Membership fee:\t\t\tRs. {membership_fee:.2f}")
    print("-" * 42)
    print(f"TOTAL PAYABLE:\t\tRs. {bill_amount:.2f}")
    print("="*42)


# Taking user inputs
num_products = int(input("How many products in your cart? "))
prices_list = []

for i in range(num_products):
    cost = float(input(f"Enter price of product {i+1}: Rs. "))
    prices_list.append(cost)

initial_total = compute_cart_total(*prices_list)
finalize_order(initial_total)
