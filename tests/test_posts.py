from typing import List

import pytest

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200

    posts_list = response.json()
    assert len(posts_list) == len(test_posts)

    posts_list = sorted(posts_list, key=lambda x: x["Post"]["id"])
    test_posts = sorted(test_posts, key=lambda x: x.id)

    for post, test_post in zip(posts_list, test_posts):
        validated_post = schemas.PostOut(**post)
        assert validated_post.Post.id == test_post.id
        assert validated_post.Post.title == test_post.title
        assert validated_post.Post.content == test_post.content
        assert validated_post.Post.owner_id == test_post.owner_id


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_post_by_id(client, test_posts):
    for test_post in test_posts:
        response = client.get(f"/posts/{test_post.id}")
        assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/posts/99999")
    assert response.status_code == 404


def test_authorized_user_get_post_by_id(authorized_client, test_posts):
    for test_post in test_posts:
        response = authorized_client.get(f"/posts/{test_post.id}")
        assert response.status_code == 200

        post_data = response.json()

        try:
            validated_post = schemas.PostOut(**post_data)
        except Exception as e:
            pytest.fail(
                f"Response does not match schema for post ID {test_post.id}: {e}"
            )

        assert (
            validated_post.Post.id == test_post.id
        ), f"Post ID mismatch: expected {test_post.id}, got {validated_post.Post.id}"
        assert (
            validated_post.Post.title == test_post.title
        ), f"Post title mismatch: expected '{test_post.title}', got '{validated_post.Post.title}'"
        assert (
            validated_post.Post.content == test_post.content
        ), f"Post content mismatch: expected '{test_post.content}', got '{validated_post.Post.content}'"
        assert (
            validated_post.Post.owner_id == test_post.owner_id
        ), f"Post owner_id mismatch: expected {test_post.owner_id}, got {validated_post.Post.owner_id}"


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("first title", "first content", True),
        ("second title", "second content", False),
        ("third title", "third content", False),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    response = authorized_client.post(
        "posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post(
        "posts/", json={"title": "first title", "content": "first content"}
    )

    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "first title"
    assert created_post.content == "first content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    response = client.post(
        "/posts/", json={"title": "first title", "content": "first content"}
    )
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_authorized_user_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/99999")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    response = authorized_client.put(f"/posts/99999", json=data)
    assert response.status_code == 404
