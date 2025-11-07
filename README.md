## @functools.wraps   
```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Apply functools.wraps here
    def wrapper(*args, **kwargs):
        print("Something before the function call")
        result = func(*args, **kwargs)
        print("Something after the function call")
        return result
    return wrapper

@my_decorator
def greet(name):
    """This function greets a person."""
    return f"Hello, {name}!"

print(greet.__name__)
print(greet.__doc__)   

# greet
# This function greets a person.


```   

## Параметризированный декоратор (декоратор для логирования с таймингом и уровнем детализации)   
```python
import logging
import time
from functools import wraps
logging.basicConfig(level=logging.INFO)

def log_execution(log_args: bool = True):
    """Декоратор с параметрами"""
    def decorator(func):
        @wraps(func)
        def wrapper (*args,**kwargs):
            start_time = time.time()
            try:
                result = func(*args,**kwargs)
                end_time = (time.time() - start_time)*1000
                if log_args:
                    logging.info( f'Calling {func.__name__} with args={args},'
                                              f' kwargs={kwargs} → returned: {result} {end_time:.2f}ms')
                else:
                    logging.info( f'Executed {func.__name__} {end_time:.2f}ms')
            except Exception as e:
                end_time = (time.time() - start_time)*1000
                if log_args:
                    logging.info( f'Calling {func.__name__} with args={args},'
                                              f' kwargs={kwargs} → failed  {type(e).__name__}: {e} {end_time:.2f}ms')
                else:
                    logging.info( f'Executed {func.__name__} failed {end_time:.2f}ms')
                raise
            return result
        return wrapper
    return decorator


@log_execution()
def slow_add(a, b):
    import time
    time.sleep(0.1)
    return a + b

result = slow_add(2, 3)

@log_execution(log_args=False)
def ping():
    return "pong"

ping()


```
## Контекстный менеджер через @contextmanager (принимает описание, замеряет время выполнения блока with, логирует)
```python
from contextlib import contextmanager
import logging
import time
logging.basicConfig(level=logging.INFO)

@contextmanager
def timed_block(name: str):
    start = time.time()
    exc = None
    try:
        # то, что до yield — это __enter__
        yield
        # то, что после yield — это __exit__ (успех)
    except Exception as e:
        exc = e
        raise
    finally:
        end = (time.time() - start) * 1000
        if exc is None:
            logging.info(f"Block '{name}' completed in {end:.2f} ms")
        else:
            logging.info(f"Block '{name}' FAILED: {type(exc).__name__}: {exc} ({end:.2f} ms)")

with timed_block("ok"):
    time.sleep(0.01)

with timed_block("fail"):
    raise RuntimeError("boom")

```

## Пример замокать get запрос   
```python
import requests
import pytest

# pip install pytest - mock

def get_post_title(post_id: int) -> str:
    """Возвращает заголовок поста по его ID."""
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    response.raise_for_status()
    return response.json()["title"]


def test_get_post_title(mocker):
    # Подготовка фейкового ответа (один объект, не список!)
    mock_response_data = {
        "userId": 1,
        "id": 42,
        "title": "My custom mocked title",
        "body": "..."
    }

    # Мокаем requests.get
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response_data

    # Вызываем функцию
    result = get_post_title(42)

    # Проверки
    assert result == "My custom mocked title"
    mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/posts/42")

```
