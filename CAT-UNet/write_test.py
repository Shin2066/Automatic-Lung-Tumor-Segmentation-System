def test():
    path = 'D:/UI/CAT-UNet/output.txt'
    f = open(path, 'w')
    print('Hello World', file=f)
    print('123', file=f)
    print('456', file=f)
    print('789', file=f)
    f.close()

if __name__ == "__main__":
    test()