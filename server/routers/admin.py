from fastapi import APIRouter, HTTPException
from common.responses import SC, HTTPBadRequest, HTTPForbidden, HTTPNotFound, HTTPUnauthorized
from data.models.category import Category
from routers.topics import switch_topic_locking_helper
from services import categories_services, users_services
from common.oauth import AdminAuthDep

admin_router = APIRouter(prefix='/admin', tags=['admin'])


# ============================== Categories ==============================

@admin_router.post('/categories', status_code=201)
def create_category(category: Category, current_admin: AdminAuthDep):
    """
    - Admin can create a Category
    - Category names must be unique
    """
    result = categories_services.create(category)
    if isinstance(result, categories_services.IntegrityError):
        raise HTTPBadRequest(result.msg)

    return result


@admin_router.patch('/categories/{category_id}/privacy', status_code=202)
def switch_category_privacy(category_id: int, current_admin: AdminAuthDep):
    """
    - Admin can make a Category private or public, if it exists
    """
    category = categories_services.get_by_id(category_id)
    if not category:
        raise HTTPNotFound()

    categories_services.update_privacy(not category.is_private, category_id)
    return f'Category {category.name} is {'public' if category.is_private else 'private'} now'


@admin_router.patch('/categories/{category_id}/locking', status_code=202)
def switch_category_locking(category_id: int, current_admin: AdminAuthDep):
    """
    - Admin can lock or unlock a Category, if it exists
    - Locked Categories don't accept new Topics
    """
    category = categories_services.get_by_id(category_id)
    if not category:
        raise HTTPNotFound("No such category")

    categories_services.update_locking(not category.is_locked, category_id)
    return f'Category {category.name} is {'unlocked' if category.is_locked else 'locked'} now'


# ============================== Users ==============================

@admin_router.post('/users/{user_id}/categories/{category_id}')
def give_user_category_read_access(user_id: int, category_id: int, current_admin: AdminAuthDep):
    """
    - Admin can give a regular user read access to a private Category
    """
    if not users_services.get_by_id(user_id) or not categories_services.get_by_id(category_id):
        raise HTTPNotFound('No such user or category')

    if categories_services.is_user_in(user_id, category_id):
        raise HTTPBadRequest('User is already in the category')

    categories_services.add_user(user_id, category_id)
    return 'User successfully added to that category and he can read'


@admin_router.delete('/users/{user_id}/categories/{category_id}')
def revoke_user_category_read_access(user_id: int, category_id: int, current_admin: AdminAuthDep):
    """
    - Admin can revoke a regular user's read access to a private Category
    """
    if not users_services.get_by_id(user_id) or not categories_services.get_by_id(category_id):
        raise HTTPNotFound('No such user or category')

    categories_services.remove_user(user_id, category_id)
    return 'User is not in that category anymore'


@admin_router.patch('/users/{user_id}/categories/{category_id}/access')
def switch_user_category_write_access(user_id: int, category_id: int, current_admin: AdminAuthDep):
    """
    - Admin can give / revoke a regular user's write access to a private Category
    """
    if not users_services.get_by_id(user_id) or not categories_services.get_by_id(category_id):
        raise HTTPNotFound('No such user or category')

    access = categories_services.get_user_access_level(user_id, category_id)
    if access is None:
        return "User is not in that category"

    categories_services.update_user_access_level(
        user_id, category_id, not access)
    return f"User {'cannot' if access else 'can'} write"


@admin_router.get('/users/categories/{category_id}')
def view_privileged_users(category_id: int, current_admin: AdminAuthDep):
    """
    - Admin can view all regular users who have access to a private Category
    """
    category = categories_services.get_by_id(category_id)
    if not category:
        raise HTTPNotFound('No such category')
    elif not category.is_private:
        return f'This category is public'

    users = categories_services.get_privileged_users(category_id)
    if not users:
        return "No users in that category"

    dto = categories_services.response_obj_privileged_users(category, users)
    return dto


# ============================== Topics ==============================

@admin_router.patch('/topics/{topic_id}/locking')
def switch_topic_locking(topic_id: int, current_admin: AdminAuthDep):
    """
    - Admin can lock/unlock a Topic
    - A locked Topic no longer accepts Replies
    """
    return switch_topic_locking_helper(topic_id, current_admin)
