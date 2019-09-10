from typing import Generator, Coroutine
from assessment_estimation.subjects import Model


class FileStorage:
    @staticmethod
    def persist(filename, converter) -> Coroutine[Model, None, None]:
        with open(filename, "w") as f:
            try:
                while True:
                    element = (yield)
                    element_text = converter(element)
                    f.write(element_text)
            except GeneratorExit:
                pass

    @staticmethod
    def restore(view_iterator, decoder) -> Generator[Model, None, None]:
        for cur_view in view_iterator:
            cur_element = decoder(cur_view)
            yield cur_element
