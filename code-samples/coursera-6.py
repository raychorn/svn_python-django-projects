wardrobe = {"shirt":["red","blue","white"], "jeans":["blue","black"]}
for k,v in wardrobe.items():
    for item in v:
        print("{} {}".format(k,item))