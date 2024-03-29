import pytest
from flask_login import login_user

from app.models import db, User, Post, Category, Tag


@pytest.fixture
def user(client):
    response = client.post('/register', data=dict(
        username='testuser',
        email='test@example.com',
        password='TestPassword',
        submit='Register'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful. You can now log in.' in response.data
    return user


@pytest.fixture
def category():
    category = Category(name='Test Category')
    db.session.add(category)
    db.session.commit()
    return category


@pytest.fixture
def tag():
    tag = Tag(name='Test Tag')
    db.session.add(tag)
    db.session.commit()
    return tag


def test_add_post(client, user, category, tag):
    login_user(user)
    response = client.post('/add_post', data=dict(
        title='Test Post',
        text='This is a test post.',
        type='News',
        category=category.id,
        tags=[tag.id]
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Post created successfully!' in response.data


def test_edit_post(client, user, category, tag):
    login_user(user)
    post = Post(title='Test Post',
                text='This is a test post.',
                type='News',
                category_id=category.id,
                user_id=user.id)
    db.session.add(post)
    db.session.commit()

    response = client.post(f'/edit_post/{post.id}', data=dict(
        title='Updated Test Post',
        text='This is an updated test post.',
        type='Other',
        category=category.id,
        tags=[tag.id]
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Post updated successfully!' in response.data


def test_delete_post(client, user, category, tag):
    login_user(user)
    post = Post(title='Test Post',
                text='This is a test post.',
                type='News',
                category_id=category.id,
                user_id=user.id)
    db.session.add(post)
    db.session.commit()

    response = client.post(f'/delete_post/{post.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Post deleted successfully!' in response.data

    deleted_post = Post.query.get(post.id)
    assert deleted_post is None


def test_view_user_posts(client, user, category, tag):
    login_user(user)
    post = Post(title='Test Post',
                text='This is a test post.',
                type='News',
                category_id=category.id,
                user_id=user.id)
    db.session.add(post)
    db.session.commit()

    response = client.get('/my_posts', follow_redirects=True)
    assert response.status_code == 200
    assert b'My Posts' in response.data
    assert b'Test Post' in response.data


def test_view_all_posts(client, user, category, tag):
    login_user(user)
    post = Post(title='Test All Post',
                text='This is a test post.',
                type='News',
                category_id=category.id,
                user_id=user.id)
    db.session.add(post)
    db.session.commit()

    response = client.get('/posts', follow_redirects=True)
    assert response.status_code == 200
    assert b'Posts' in response.data
    assert b'Test All Post' in response.data
