def coroutine():
    try:
        while True:
            name = (yield)
            print(name)
    except GeneratorExit:
        print("coroutine closed!")

