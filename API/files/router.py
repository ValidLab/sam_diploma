import os
import shutil

from PIL import Image
from typing import List
from datetime import datetime

from fastapi import APIRouter, UploadFile, Depends, Cookie
from fastapi.responses import FileResponse, JSONResponse

from sqlalchemy import select, desc, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from API.files.database import get_async_session
from API.files.functions import reformate_photo, check_auth
from API.files.models import file, favourites
from API.files.schemas import FileCreate

router = APIRouter(
    prefix="/file",
    tags=["Files"]
)


@router.post("/improve_file/post")
async def post_file(filename: str, public: bool, session: AsyncSession = Depends(get_async_session),
                    fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    created_at = datetime.now()
    # img_info = {'path': filename, 'author': data['nickname'], 'public': public, 'created_at': created_at, 'likes': 0}
    # await session.execute(img_info)
    # await session.commit()

    stmt = insert(file).values(path=filename, author=data['nickname'], public=public, created_at=created_at, likes=0)
    await session.execute(stmt)
    await session.commit()


@router.post("/improve_file")
async def improve_file(uploaded_file: UploadFile, prompt: str, anti_prompt: str, coordinates: List[str],
                       fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    destination = f"media/{uploaded_file.filename}"
    if not os.path.exists('media'):
        os.makedirs('media')
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    finally:
        uploaded_file.file.close()

    img = reformate_photo(destination, coordinates, prompt, anti_prompt)

    img = Image.fromarray(img)
    final_destination = ''.join(destination.split('.')[:-1]) + '_updated.jpg'
    img.save(final_destination)

    return FileResponse(final_destination, filename=final_destination)


@router.get("/images/favourite/")
async def get_favourite(session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).select_from(favourites).where(favourites.c.user_id == data['id']).join(file)

    result = await session.execute(query)

    return result.mappings().all()


@router.get("/images/private/")
async def get_private(session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).select_from(file).where((file.c.author == data['nickname']) & (file.c.public == False))

    result = await session.execute(query)

    return result.mappings().all()


@router.get("/images")
async def get_public(filter_by: str = 'latest', author: str = '', skip: int = 0, limit: int = 10,
                  session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    if author:
        query = select(file).where((file.c.author == author) & (file.c.public == True))
    else:
        query = select(file).where(file.c.public == True)

    if filter_by == 'earliest':
        query = query.order_by(file.c.created_at)
    elif filter_by == 'latest':
        query = query.order_by(desc(file.c.created_at))
    elif filter_by == 'likes':
        query = query.order_by(desc(file.c.likes))

    result = await session.execute(query)

    return result.mappings().all()


@router.get("/image/{image_id}")
async def get_image(image_id: int, session: AsyncSession = Depends(get_async_session),
                    fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).where(file.c.id == image_id)

    result = await session.execute(query)
    return result.mappings().one()


@router.patch("/image/add_like/{image_id}")
async def add_like_image(image_id: int, session: AsyncSession = Depends(get_async_session),
                         fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).where(file.c.id == image_id)
    result = await session.execute(query)
    stored_item_data = result.mappings().one()

    stmt = (update(file).where(file.c.id == image_id).values(likes=stored_item_data['likes']+1))
    await session.execute(stmt)
    await session.commit()

    return JSONResponse(status_code=204, content=None)


@router.patch("/image/change_status/{image_id}")
async def change_status_image(image_id: int, session: AsyncSession = Depends(get_async_session),
                              fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).where(file.c.id == image_id)
    result = await session.execute(query)
    stored_item_data = result.mappings().one()
    if data['nickname'] != stored_item_data['author']:
        return JSONResponse(status_code=403, content={"detail": "It's not your image."})

    stmt = (update(file).where(file.c.id == image_id).values(public=not(stored_item_data['public'])))
    await session.execute(stmt)
    await session.commit()

    return JSONResponse(status_code=204, content=None)


@router.post("/image/add_favourite/{image_id}")
async def add_favourite(image_id: int, session: AsyncSession = Depends(get_async_session),
                              fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    stmt = insert(favourites).values(user_id=data['id'], id_file=image_id)
    await session.execute(stmt)
    await session.commit()

    return JSONResponse(status_code=204, content=None)


# @router.post("/image")
# async def add_file(new_file: FileCreate, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(file).values(**new_file.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return JSONResponse(status_code=201, content=new_file.dict())


@router.post("/random")
async def improve_file():
    final_destination = 'media/Pyramid_updated.jpg'

    return FileResponse(final_destination, filename=final_destination)


@router.get("/get_image_file/{image_id}")
async def get_file(image_id: int, session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).where(file.c.id == image_id)

    result = await session.execute(query)
    result = result.mappings().one().get('path')

    return FileResponse(result)
