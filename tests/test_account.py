import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    User.objects.create_user('test', 'test@mail.com', 'test')
    count = User.objects.all().count()
    print(count)
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_follow_user():
    user_1 = User.objects.create_user('test1', 'test1@mail.com', 'test')
    user_2 = User.objects.create_user('test2', 'test2@mail.com', 'test')
    print(user_1)
    print(user_2)
    user_1_profile = user_1.profile
    user_2_profile = user_2.profile

    # user_1 follow user_2
    user_2_profile.followers.add(user_1)
    print('user_1 follow user_2')
    
    # user_1 の フォロワー数
    user_1_follower_count = user_1_profile.followers.count()
    # user_1 の フォロー数
    user_1_following_count = user_1.following.count()
    # user_2 の フォロワー数
    user_2_follower_count = user_2_profile.followers.count()
    # user_2 の フォロー数
    user_2_following_count = user_2.following.count()

    assert user_1_follower_count == 0
    assert user_1_following_count == 1
    assert user_2_follower_count == 1
    assert user_2_following_count == 0


@pytest.mark.django_db
def test_unfollow_user():
    user_1 = User.objects.create_user('test1', 'test1@mail.com', 'test')
    user_2 = User.objects.create_user('test2', 'test2@mail.com', 'test')
    print(user_1)
    print(user_2)
    user_1_profile = user_1.profile
    user_2_profile = user_2.profile

    # user_1 follow user_2
    user_2_profile.followers.add(user_1)
    print('user_1 follow user_2')

    # user_1 unfollow user_2
    user_2_profile.followers.remove(user_1)
    print('user_1 unfollow user_2')
    
    # user_1 の フォロワー数
    user_1_follower_count = user_1_profile.followers.count()
    # user_1 の フォロー数
    user_1_following_count = user_1.following.count()
    # user_2 の フォロワー数
    user_2_follower_count = user_2_profile.followers.count()
    # user_2 の フォロー数
    user_2_following_count = user_2.following.count()

    assert user_1_follower_count == 0
    assert user_1_following_count == 0
    assert user_2_follower_count == 0
    assert user_2_following_count == 0
