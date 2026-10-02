def check_purchases(purchases, budget):
    total_spent = 0

    for purchase in purchases:
        total_spent += purchase
        if total_spent > budget:
            print(f"This {purchase} is over budget!")
            break
        else:
            print(f"This {purchase} is within budget.")