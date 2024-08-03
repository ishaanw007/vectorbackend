from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def check_is_dag(nodes, edges):
    graph = {node.id: set() for node in nodes}
    for edge in edges:
        graph[edge.source].add(edge.target)
    
    def has_cycle(node, path):
        if node in path:
            return True
        path.add(node)
        for neighbor in graph[node]:
            if has_cycle(neighbor, path):
                return True
        path.remove(node)
        return False

    for node in graph:
        if has_cycle(node, set()):
            return False
    return True

@app.post('/pipelines/parse')
async def parse_pipeline(pipeline: Pipeline = Body(...)):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    is_dag = check_is_dag(pipeline.nodes, pipeline.edges)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag
    }