from fastapi import APIRouter, Depends

from src.dependencies.access_control import access_control, RoleOptions, super_user_access

router = APIRouter()


@router.get('/health')
async def health_check():
    return {'status': 'ok'}


@router.get('/health_auth')
async def health_check_auth(
        _=Depends(super_user_access)
):
    return {'status': 'ok', 'auth': 'authenticated'}
