from fastapi import APIRouter, Query
from sqlalchemy import text

from base.dababase import get_session_2
from base.sql_model import WorkBenches

router = APIRouter(
    prefix="/work",
    tags=["工作台"],
)


@router.get("/list", summary="工作台列表")
async def work_list():
    """
    工作台列表 \n
    return:
    """

    my_session = get_session_2().__next__()
    results = my_session.execute(
        text("SELECT w.id,w.video_id,w.`status`,v.`name`,w.`type_flag`,w.`crop_name` from work_benches as w "
             "LEFT JOIN video as v on w.video_id=v.id WHERE w.status_flag=0 ORDER BY w.create_time desc"))
    task_list = []
    for result in results:
        task_list.append(result._asdict())
    return {"data": task_list}


@router.get("/delete", summary="工作台删除")
async def work_delete(work_id: int = Query(..., description="工作台id", example=1, gt=0)):
    """
    工作台记录逻辑删除 \n
    """
    try:
        my_session = get_session_2().__next__()
        my_session.query(WorkBenches).filter(WorkBenches.id == work_id).update({"status_flag": 1})
        my_session.commit()
        return {"msg": "删除成功"}
    except Exception as e:
        print(f"更新失败：{e}")
        return {"code": 500, "msg": f"删除失败:{e}"}
