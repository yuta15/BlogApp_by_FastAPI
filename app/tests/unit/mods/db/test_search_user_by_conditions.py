from app.mods.db.search_user_by_conditions import search_user_by_conditions
from app.models.User import User

def test_search_user_by_conditions_and(db_session, select_user_fixture):
    """search_user_by_conditionsのand検索用テスト用関数"""
    session = db_session
    users = select_user_fixture(session)
    for user in users:
        user_stmt = [
            User.username == user.username, 
            User.uuid == user.uuid,
            User.email == user.email
            ]
        assert [user] == search_user_by_conditions(session=session, method=True, conditions=user_stmt)


# def test_search_user_by_conditions_time_over(db_session, select_user_fixture):
#     """search_user_by_conditionsのand検索用テスト用関数"""
#     session = db_session
#     users = select_user_fixture(session)
#     for user in users:
#         user_stmt = [
#             User.create_at == user.username, 
#             User.uuid == user.uuid,
#             User.email == user.email
#             ]
#         assert [user] == search_user_by_conditions(session=session, method=True, conditions=user_stmt)



# def test_search_user_by_conditions_or(db_session, select_data_fixture):
#     """search_user_by_conditionsのor検索用テスト用関数"""
#     session = db_session
#     users = select_data_fixture(session)
    
#     for user in users:
        