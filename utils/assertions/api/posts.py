from models.posts import DefaultPost, PostDict , UpdatePost 
from utils.assertions.base.expect import expect


def assert_post(
    expected_post: PostDict,
    actual_post: DefaultPost | UpdatePost
):
    if isinstance(actual_post, DefaultPost):
        expect(expected_post['id']) \
            .set_description('Post "id"')\
            .to_be_equal(actual_post.id)

    expect(expected_post['user_id']) \
        .set_description('Post "user_id"') \
        .to_be_equal(actual_post.user_id)

    expect(expected_post['title']) \
        .set_description('Post "title"') \
        .to_be_equal(actual_post.title)
    
    expect(expected_post['body']) \
        .set_description('Post "body"') \
        .to_be_equal(actual_post.body)
    