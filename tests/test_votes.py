def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1}
    )
    assert response.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert response.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert response.status_code == 404


def test_vote_post_not_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": 99999, "dir": 1})
    assert response.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert response.status_code == 401
