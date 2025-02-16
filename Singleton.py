class MemoryItem:
    def __init__(self):
        self.data = [0] * 1024

    def reset(self):
        for i in range(len(self.data)):
            self.data[i] = 0


class RAM:
    MAX_COUNT = 100
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.objects = [
            MemoryItem() for _ in range(RAM.MAX_COUNT)
        ]

    def get(self) -> MemoryItem:
        return self.objects.pop()

    def release(self, reusable: MemoryItem):
        reusable.reset()
        self.objects.append(reusable)

def main():
    r1 = RAM()
    r2 = RAM()
    print(r1)
    print(r2)

if __name__ == '__main__':
    main()