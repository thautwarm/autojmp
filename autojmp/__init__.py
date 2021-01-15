from pathlib import Path
from collections import Counter
from wisepy2 import wise
import os
import sys

root = Path(os.environ.get('AUTOJMP_DIR', '~/.autojmp')).expanduser()

class AutoJump:
    max_cache = max(1, int(os.environ.get("AUTOJMP_MAX_CACHE", 999)))
    word_analyze_len = max(1, int(os.environ.get("AUTOJMP_WORD_ANA_LEN", 3)))

class FileIO:

    def __init__(self, file_path: Path, cache_size_getter):
        self.file_path = file_path
        self._max_cache_getter = cache_size_getter
        self._histories = None
        if not file_path.exists():
            file_path.parent.mkdir(mode=0o777, parents=True, exist_ok=True)
            with file_path.open('w'):
                pass

    @property
    def histories(self) -> list:
        self._load_history()
        return self._histories

    def _load_history(self):
        if self._histories is None:
            with self.file_path.open('r') as fr:
                self._histories = list(map(str.rstrip, fr))

    def __getitem__(self, item):
        return self.histories[item]

    def __len__(self):
        return len(self.histories)

    def __iter__(self):
        yield from self.histories

    def writeline(self, text):
        with self.file_path.open('a+') as fw:
            fw.write(text)
            fw.write('\n')
        self.histories.append(text)
        n = self._max_cache_getter()

        if len(self.histories) > n:
            with self.file_path.open('r') as fr:
                contents = list(fr)
            with self.file_path.open('w') as fw:
                for each in contents[-n:]:
                    fw.write(each)



class _HistVectorGatherIO:

    def __init__(self, file_io: FileIO):
        self._file_io = file_io
        self._vectors = list(map(to_vec, file_io))

    def __len__(self):
        return len(self._vectors)


    def writeline(self, line: str):
        self._file_io.writeline(line)
        self._vectors.append(to_vec(line))

    def corr_with(self, line: str):
        line_vec = to_vec(line)

        ret = {}
        for key, vec in zip(self._file_io, self._vectors):
            if key not in ret:
                ret[key] = corr(vec, line_vec)

        return ret

    def index_vec(self, idx):
        return self._vectors[idx]

    def index_line(self, idx):
        return self._file_io[idx]



def _analyzer(text, ngram):
    tokens = text
    for k in range(1, ngram + 1):
        n = len(tokens) - k
        for i in range(n):
            yield tokens[i: i + k]


def to_vec(s: str):
    return Counter(_analyzer(s, AutoJump.word_analyze_len))


def corr(a: Counter, b: Counter):
    na = len(a)
    nb = len(b)

    def get_score(l, r):
        weights = 0
        score = 0
        for lk, lv in l.items():
            v = r.get(lk)
            weight = len(lk)
            weights += weight
            if v is None:
                continue

            if v > lv:
                v, lv = lv, v
            score += weight * v / lv

        if weights == 0:
            return 0

        return score / weights

    return (get_score(a, b) * na + get_score(b, a) * nb) / (na + nb)

rtpy_history_cached_file = _HistVectorGatherIO(FileIO(root / ('wd_history'), lambda: AutoJump.max_cache))

@wise
def cli(subcommand, *args):
    if subcommand == "update":
        [pwd] = args
        path_str = str(Path(pwd).absolute())
        rtpy_history_cached_file.writeline(path_str)
        return
    elif subcommand == "complete":
        text = ' '.join(args)
        correlation_asoc_lst = tuple(rtpy_history_cached_file.corr_with(text).items())
        try:
            p, stat = min(correlation_asoc_lst, key=lambda _: -_[1])
            sys.stdout.write(p)
        except ValueError:
            sys.stdout.write('.')
    else:
        raise ValueError
