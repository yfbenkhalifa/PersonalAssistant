from fastapi import FastAPI
from global_settings import global_settings
from langgraph.prebuilt import create_react_agent


app = FastAPI(
    title=global_settings.API_TITLE,
    description=global_settings.API_DESCRIPTION,
    version=global_settings.API_VERSION
)

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt="You are a helpful assistant"
)

@app.get("/api/v1/invoke")
async def invoke(query: str):
    agent = 




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=global_settings.HOST, port=global_settings.PORT)