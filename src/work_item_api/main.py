from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from work_item_api.database import get_session
from work_item_api.models import WorkItem
from work_item_api.schemas import WorkItemCreate, WorkItemRead, WorkItemUpdate

app = FastAPI(title="Work Item API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/work-items", response_model=WorkItemRead, status_code=status.HTTP_201_CREATED)
def create_work_item(payload: WorkItemCreate, session: Session = Depends(get_session)) -> WorkItem:
    item = WorkItem(title=payload.title, description=payload.description)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/work-items", response_model=list[WorkItemRead])
def list_work_items(session: Session = Depends(get_session)) -> list[WorkItem]:
    return list(session.scalars(select(WorkItem).order_by(WorkItem.id)))


@app.get("/work-items/{item_id}", response_model=WorkItemRead)
def get_work_item(item_id: int, session: Session = Depends(get_session)) -> WorkItem:
    item = session.get(WorkItem, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work item not found")
    return item


@app.patch("/work-items/{item_id}", response_model=WorkItemRead)
def update_work_item(
    item_id: int, payload: WorkItemUpdate, session: Session = Depends(get_session)
) -> WorkItem:
    item = session.get(WorkItem, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work item not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    session.commit()
    session.refresh(item)
    return item


@app.delete("/work-items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_item(item_id: int, session: Session = Depends(get_session)) -> Response:
    item = session.get(WorkItem, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work item not found")

    session.delete(item)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
