def get_image_number(score):
    if score <= 0:
        return 0
    
    if score >= 100:
        return 100
    
    return round(score, -1)
    
print(get_image_number(-10))
print(get_image_number(10))
print(get_image_number(11))
print(get_image_number(16))
print(get_image_number(21))
print(get_image_number(121))