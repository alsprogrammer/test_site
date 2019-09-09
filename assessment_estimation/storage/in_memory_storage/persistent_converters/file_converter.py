from typing import Generator, Coroutine


class FileStorage:
    @staticmethod
    def persist(filename, converter) -> Coroutine:
        with open(filename, "w") as f:
            try:
                while True:
                    element = (yield)
                    element_text = converter(element)
                    f.write(element_text)
            except GeneratorExit:
                print("Closing coroutine!!")

    @staticmethod
    def get_elements(self) -> Generator:
        pass
