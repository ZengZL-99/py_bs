def props_with(obj):
    print("www", type(obj))
    pr = {
        "id", obj.id,
        "name", obj.name
    }
    return pr