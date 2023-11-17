from pydantic import BaseModel, Field


class Demo(BaseModel):
    name: str = Field(default="hello word", description="你好")
