from abc import ABC, abstractmethod
from types import TracebackType
from typing import IO, Optional, Type, Iterator, Iterable, Dict, List
import xml.etree.ElementTree as ET
import pathlib


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
    def __init__(self, filename: str, read: bool, element_name: str, root_element_name: str):
        self._readable = read
        self._element_name = element_name
        self._filename = filename
        self._path = pathlib.Path(self._filename)

        if self._path.exists() and self._path.is_file():
            self._root = ET.parse(filename).getroot()
        else:
            self._root = ET.Element(root_element_name)

    def readable(self) -> bool:
        return self._readable

    def writable(self) -> bool:
        return not self._readable

    def close(self) -> None:
        self.flush()

    def flush(self) -> None:
        ET.ElementTree(self._root).write(self._filename)

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
        ET.SubElement(self._root, self._element_name, attrib=s)

    def writelines(self, lines: Iterable[Dict]) -> None:
        for s in lines:
            self.write(s)

    def __next__(self) -> Dict:
        pass

    def __iter__(self) -> Iterator[Dict]:
        pass

    def __enter__(self) -> IO[Dict]:
        pass

    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        pass


def open(name: str, options: str, root_element_name: str, element_name: str) -> FormattedFileLike:
    xml_file = XMLFormattedFileLike(name, True if options == "r" else False, element_name, root_element_name)
    return xml_file


if __name__ == "__main__":
    xml_file = open("/tmp/1.xml", "w", "Test", "Task")
    new_dict = {"a": 1, "b": 2}
    xml_file.write(new_dict)
    xml_file.close()

