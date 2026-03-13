def segment_customers(store_id: str):
    return [
        {'segment_name': 'VIP', 'customer_count': 50, 'avg_ticket': 425.50, 'avg_frequency': 8.5},
        {'segment_name': 'Regulares', 'customer_count': 100, 'avg_ticket': 140.00, 'avg_frequency': 6.0},
        {'segment_name': 'Ocasionales', 'customer_count': 150, 'avg_ticket': 65.00, 'avg_frequency': 2.0}
    ]