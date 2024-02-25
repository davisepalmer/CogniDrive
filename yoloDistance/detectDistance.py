import detect
def detectDistance(imgsource):
    return detect.run(source = imgsource)

def main():
    print(detect.run(source='test2.jpg'))

main()