import nest_asyncio
nest_asyncio.apply()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel

import traceback
from langchain_core.runnables.graph import MermaidDrawMethod

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()
        # Draw mermaid diagram using local rendering
        png_graph = react_app.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.PYPPETEER  # Use local Pyppeteer instead of Mermaid.ink API
        )
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        # Prepare messages for the LLM
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        # Get the final output
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)

        return {"answer": final_output}
    except Exception as e:
        # Print full traceback for better debugging
        print("Exception occurred:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
