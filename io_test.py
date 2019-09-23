from abc import ABC, abstractmethod
from types import TracebackType
from typing import IO, Optional, Type, Iterator, Iterable, Dict, List


class FormattedFileLike(IO[Dict], ABC):
    @abstractmethod
    def close(self) -> None:
        pass

    def fileno(self) -> int:
        return 0

    @abstractmethod
    def flush(self) -> None:
        pass

    def isatty(self) -> bool:
        return False

    @abstractmethod
    def read(self, n: int = ...) -> Dict:
        pass

    @abstractmethod
    def readable(self) -> bool:
        pass

    @abstractmethod
    def readline(self, limit: int = ...) -> Dict:
        pass

    @abstractmethod
    def readlines(self, hint: int = ...) -> List[Dict]:
        pass

    def seek(self, offset: int, whence: int = ...) -> int:
        raise NotImplementedError("The file is not seekable")

    def seekable(self) -> bool:
        return False

    @abstractmethod
    def tell(self) -> int:
        pass

    @abstractmethod
    def truncate(self, size: Optional[int] = ...) -> int:
        pass

    @abstractmethod
    def writable(self) -> bool:
        pass

    @abstractmethod
    def write(self, s: Dict) -> int:
        pass

    @abstractmethod
    def writelines(self, lines: Iterable[Dict]) -> None:
        pass

    @abstractmethod
    def __next__(self) -> Dict:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Dict]:
        pass

    @abstractmethod
    def __enter__(self) -> IO[Dict]:
        pass

    @abstractmethod
    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        pass


class XMLFormattedFileLike(FormattedFileLike):
    def __init__(self, filename: str, read: bool):
        self._readable = read
        self._filename = filename

    def readable(self) -> bool:
        return self._readable

    def writable(self) -> bool:
        return not self._readable

    def close(self) -> None:
        pass

    def flush(self) -> None:
        pass

    def read(self, n: int = ...) -> Dict:
        pass

    def readline(self, limit: int = ...) -> Dict:
        pass

    def readlines(self, hint: int = ...) -> List[Dict]:
        pass

    def seek(self, offset: int, whence: int = ...) -> int:
        pass

    def tell(self) -> int:
        pass

    def truncate(self, size: Optional[int] = ...) -> int:
        pass

    def write(self, s: Dict) -> int:
        pass

    def writelines(self, lines: Iterable[Dict]) -> None:
        pass

    def __next__(self) -> Dict:
        pass

    def __iter__(self) -> Iterator[Dict]:
        pass

    def __enter__(self) -> IO[Dict]:
        pass

    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        pass


def open(name: str, options: str) -> FormattedFileLike:
    return XMLFormattedFileLike(name, True if options == "r" else False)


if __name__ == "__main__":
    with open("/tmp/1.xml", "w") as xml_file:
        new_dict = {"a": 1, "b": 2}
        xml_file.write(new_dict)
