import os
import shutil

import requests
from PIL import Image
from typing import List
from datetime import datetime

from fastapi import APIRouter, UploadFile, Depends, Cookie
from fastapi.responses import FileResponse, JSONResponse

from sqlalchemy import select, desc, insert, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from API.files.database import get_async_session
from API.files.functions import reformate_photo, check_auth
from API.files.models import file, favourites
from API.files.schemas import FileCreate, FavouritesCreate, FileUpdate

router = APIRouter(
    prefix="/file",
    tags=["Files"]
)

# templates = Jinja2Templates(directory="preprocessing/src/templates")


# @router.get("/work")
# def get_template(request: Request):
#     return templates.TemplateResponse("work.html", {"request": request})

@router.get("/aaaaa")
async def get_aaa(fastapiusersauth: str = Cookie(None)):
    response = requests.get("http://localhost:8001/api/user/get_user_info", cookies={"fastapiusersauth": fastapiusersauth})
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.get("/dabliat")
async def read_items(fastapiusersauth: str = Cookie(None)):
    return {"fastapiusersauth": fastapiusersauth}


@router.post("/improve_file")
async def improve_file(uploaded_file: UploadFile, prompt: str, anti_prompt: str, coordinates: List[str], session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
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
    created_at = datetime.now()
    # row_count = file.query(func.count(file.id)).scalar()
    # query = file.select().with_only_columns([file.c.id]).count()
    # row_count = session.execute(query).scalar()
    img_info = {'path': final_destination, 'author': 'me', 'public': False, 'created_at': created_at, 'likes': 0}
    await session.execute(img_info)
    await session.commit()
    return FileResponse(final_destination)


@router.get("/images")
async def get_all(filter_by: str = 'cr_time acs', author: str = '', skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    if author:
        query = select(file).where(file.c.author == author)
    else:
        query = select(file)

    if filter_by == 'cr_time acs':
        query = query.order_by(file.c.created_at)
    elif filter_by == 'cr_time desc':
        query = query.order_by(desc(file.c.created_at))
    elif filter_by == 'likes acs':
        query = query.order_by(file.c.likes)
    elif filter_by == 'likes desc':
        query = query.order_by(desc(file.c.likes))

    result = await session.execute(query)

    return result.mappings().all()


@router.get("/image/{image_id}")
async def get_image(image_id: int, session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).where(file.c.id == image_id)

    result = await session.execute(query)

    return result.mappings().all()


@router.patch("/image/add_like/{image_id}")
async def add_like_image(image_id: int, session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).where(file.c.id == image_id)
    result = await session.execute(query)
    stored_item_data = result.mappings().one()

    stmt = (update(file).where(file.c.id == image_id).values(likes=stored_item_data['likes']+1))
    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}


@router.patch("/image/change_status/{image_id}")
async def change_status_image(image_id: int, session: AsyncSession = Depends(get_async_session), fastapiusersauth: str = Cookie(None)):
    status_code, data = check_auth(fastapiusersauth)
    if status_code == 401:
        return JSONResponse(status_code=status_code, content=data)

    query = select(file).where(file.c.id == image_id)
    result = await session.execute(query)
    stored_item_data = result.mappings().one()
    if data['nickname'] != stored_item_data['nickname']:
        return JSONResponse(status_code=403, content={"detail": "It's not your image."})

    stmt = (update(file).where(file.c.id == image_id).values(public=not(stored_item_data['public'])))
    await session.execute(stmt)
    await session.commit()

    return JSONResponse(status_code=204)


@router.post("/image")
async def add_file(new_file: FileCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(file).values(**new_file.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}




