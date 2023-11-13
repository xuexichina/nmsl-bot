import random
from dataclasses import dataclass, field
from typing import List

from httpx import AsyncClient, NetworkError, HTTPError
from httpcore import TimeoutException


class UpdateException(Exception):
    pass


@dataclass
class Corpus:
    common: List[str] = field(default_factory=list)
    refuse: List[str] = field(default_factory=list)
    trigger: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.http = AsyncClient()

    async def update(self):
        try:
            file=open('nmsl.txt', encoding="utf8")
            content = file.read()
            #content = [x.strip() for x in content] 
            self.common = content.strip().split("\n")
            self.refuse = content.strip().split("\n")
            self.trigger = content.strip().split("\n")
        except (NetworkError, HTTPError, TimeoutException) as e:
            raise UpdateException from e

    def get_rnd_common(self):
        return self.common[random.randint(0, len(self.common) - 1)]

    def get_rnd_refuse(self):
        return self.refuse[random.randint(0, len(self.refuse) - 1)]
