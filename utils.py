def inp(min_value, max_value, msg, err_msg):
    value = input(msg)
    while not value.isdigit() or not(min_value <= int(value) < max_value):
        value = input(err_msg)
    return int(value)
