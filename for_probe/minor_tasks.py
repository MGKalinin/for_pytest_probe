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

