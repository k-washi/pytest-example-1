from _pytest.monkeypatch import monkeypatch
import pytest
import pdb
from tests.conftest import assert_list_match
from unittest.mock import patch
import os
from pathlib import Path

def f(n = 0):
    a = 5
    #pdb.set_trace() # debugモードに入り、変数の確認ができる
    return 3

def test_f():
    assert f() == 3

def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_match():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        raise ValueError("Exception 123 raised")

def test_excinfo():
    with pytest.raises(RuntimeError) as excinfo:
        raise RuntimeError("ERROR")
    assert str(excinfo.value) == "ERROR"

@pytest.fixture
def smtp():
    return 3


def test_foo(smtp):
    print(smtp)


@pytest.fixture
def before_and_after():
    print('BEFORE')
    yield "aaaaaaaaaaaaaaa"
    print('AFTER')

def test_foo(before_and_after):
    print(before_and_after)

def test_foo2(assert_list_match):
    assert_list_match([1,2,3], [3,1,2])


class Example1:
    def example_method(self, n):
        return n * 2

def test_monkeypatch(monkeypatch):
    e = Example1()

    def mockreturn(self, n):
        # n*2 => n*3
        return n * 3
    
    monkeypatch.setattr(Example1, "example_method", mockreturn)

    assert e.example_method(3) == 9

def test_patch_func():
    e = Example1()
    assert e.example_method(0) == 0
    with patch.object(Example1, 'example_method', return_value=42) as m:
        assert e.example_method(0) == 42

        e.example_method(1)
        e.example_method(2)
        e.example_method(3)
    #m.assert_any_call(3)
    assert m.call_count == 4

## 環境変数
## monkeypatch の例
def test_env1(monkeypatch):
    monkeypatch.setenv('NEW_KEY', 'newvalue')
    assert os.environ['NEW_KEY'] == 'newvalue'


## unittest.mock の例
def test_env2():
    with patch.dict('os.environ', {'NEW_KEY': 'newvalue'}):
        assert os.environ['NEW_KEY'] == 'newvalue'

# 1時ファイルの作成
def create_file_in_cwd():
    with open('foo.txt', 'w') as f:
        print('hello', file=f)

def test_create_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path) # カレントディレクトリを tmp_path に一時的に変更
    create_file_in_cwd()
    assert Path('foo.txt').exists()

# mymoduleの読み込み
def test_package():
    from mypkg.sample import kk
    assert kk() == 5

# テストデータの読み込み
def test_read_global(shared_datadir):
    #dataからデータを読み込み
    contents = (shared_datadir / 'hello.txt').read_text()
    assert contents == 'Hello World!\n'
def test_read_module(datadir):
    # sample1 (ファイル名のディレクトリ)からデータを読み込む
    contents = (datadir / 'spam.txt').read_text()
    assert contents == 'eggs\n'
