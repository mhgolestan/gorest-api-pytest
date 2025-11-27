from models.users import DefaultUser, UserDict , UpdateUser 
from utils.assertions.base.expect import expect


def assert_user(
    expected_user: UserDict,
    actual_user: DefaultUser | UpdateUser
):
    if isinstance(actual_user, DefaultUser):
        expect(expected_user['id']) \
            .set_description('User "id"')\
            .to_be_equal(actual_user.id)

    expect(expected_user['name']) \
        .set_description('User "name"') \
        .to_be_equal(actual_user.name)

    expect(expected_user['email']) \
        .set_description('User "email"') \
        .to_be_equal(actual_user.email)

    expect(expected_user['gender']) \
        .set_description('User "gender"') \
        .to_be_equal(actual_user.gender)
    
    expect(expected_user['status']) \
        .set_description('User "status"') \
        .to_be_equal(actual_user.status)