import random

def random_menu():
    """This is a random menu app you want to choose you want
    If this matches what you want you have to go to eat it"""

    random_list = ["กะเพราหมู", "ไข่เจียวหมูสับ", "หมูทอดกระเทียม", "ก๋วยเตี๋ยว", "ผัดซีอิ๊ว"]
    menu_data = random.choice(random_list)

    print(menu_data)


random_menu()