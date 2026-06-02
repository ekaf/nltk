import os
from importlib import import_module

import pytest

from nltk import pathsec
from nltk.corpus.reader.util import (
    StreamBackedCorpusView,
    find_corpus_fileids,
    read_line_block,
)
from nltk.data import FileSystemPathPointer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

reader_util = import_module("nltk.corpus.reader.util")


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="requires os.symlink")
def test_corpusreader_open_blocks_symlink_escape(tmp_path):
    # Arrange: a corpus root in tempdir
    corpus_root = tmp_path / "corpus"
    corpus_root.mkdir()

    # Arrange: a second directory also in tempdir (so pathsec allowed-roots won't object)
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()

    # Secret file outside the corpus root
    secret = outside_dir / "secret.txt"
    secret.write_text("should not be readable via corpus_root", encoding="utf-8")

    # Create a symlink inside corpus_root that points outside corpus_root
    link = corpus_root / "outside_link"
    os.symlink(str(outside_dir), str(link))

    reader = PlaintextCorpusReader(str(corpus_root), r".*")

    # Act + Assert: opening via the symlinked path must be blocked by corpus-root sandboxing
    with pytest.raises((ValueError, PermissionError, OSError)):
        reader.open("outside_link/secret.txt").read()


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="requires os.symlink")
def test_find_corpus_fileids_prunes_symlink_escape(tmp_path, monkeypatch):
    corpus_root = tmp_path / "corpus"
    corpus_root.mkdir()
    (corpus_root / "inside.txt").write_text("inside", encoding="utf-8")

    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    (outside_dir / "secret.txt").write_text("secret", encoding="utf-8")

    link = corpus_root / "outside_link"
    try:
        os.symlink(str(outside_dir), str(link))
    except OSError:
        pytest.skip("symlink creation not available")

    original_walk = os.walk
    monkeypatch.setattr(
        reader_util.os, "walk", lambda path: original_walk(path, followlinks=True)
    )

    fileids = find_corpus_fileids(FileSystemPathPointer(str(corpus_root)), r".*\.txt")

    assert "inside.txt" in fileids
    assert "outside_link/secret.txt" not in fileids


def test_streambackedcorpusview_string_fileid_uses_pathsec(tmp_path, monkeypatch):
    sample = tmp_path / "sample.txt"
    sample.write_text("first line\n", encoding="utf-8")

    monkeypatch.setattr(pathsec, "ENFORCE", True)
    monkeypatch.setattr(pathsec, "_get_allowed_roots", lambda: set())

    view = StreamBackedCorpusView(str(sample), read_line_block)
    with pytest.raises(PermissionError):
        view[0]
