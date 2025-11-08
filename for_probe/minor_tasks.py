import requests

base_url="https://jsonplaceholder.typicode.com/posts"
def get_post_titles_by_user_id(url:str,user_id: int) -> list[str]:
    response = requests.get(url)
    response.raise_for_status()
    response_json=response.json()
    answer=[]
    for post in response_json:
        if post["userId"] == user_id:
            answer.append(post["title"])
    return answer
# print(get_post_titles_by_user_id(base_url,1))


def test_get_post_titles_by_user_id(mocker):
    mock_response_data = [
        {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit..."
        },
        {
            "userId": 1,
            "id": 2,
            "title": "qui est esse",
            "body": "est rerum tempore..."
        },
        {
            "userId": 2,  # пост другого пользователя - должен быть отфильтрован
            "id": 3,
            "title": "other user post",
            "body": "..."
        }
    ]
    mock_get=mocker.patch("requests.get")
    mock_get.return_value.status_code=200
    mock_get.return_value.json.return_value = mock_response_data

    result=get_post_titles_by_user_id(base_url,1)
    expected_titles = [
        "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "qui est esse"
    ]
    assert result == expected_titles

