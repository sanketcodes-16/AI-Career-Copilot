from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents import (
    resume_agent,
    career_agent,
    interview_agent,
    skill_gap_agent
)

# Graph State
class AgentState(TypedDict):
    user_input: str
    response: str


# Supervisor Router
def supervisor(state: AgentState):

    user_input = state["user_input"].lower()

    if "resume" in user_input:
        return "resume"

    elif "interview" in user_input or "question" in user_input:
        return "interview"

    elif "skill" in user_input or "missing" in user_input:
        return "skill_gap"

    else:
        return "career"


# Resume Node
def resume_node(state: AgentState):

    result = resume_agent(state["user_input"])

    return {
        "response": result
    }


# Career Node
def career_node(state: AgentState):

    result = career_agent(state["user_input"])

    return {
        "response": result
    }


# Interview Node
def interview_node(state: AgentState):

    result = interview_agent(state["user_input"])

    return {
        "response": result
    }


# Skill Gap Node
def skill_gap_node(state: AgentState):

    result = skill_gap_agent(state["user_input"])

    return {
        "response": result
    }


# Build Graph
graph = StateGraph(AgentState)

# Add Nodes
graph.add_node("resume", resume_node)
graph.add_node("career", career_node)
graph.add_node("interview", interview_node)
graph.add_node("skill_gap", skill_gap_node)

# Conditional Routing
graph.set_conditional_entry_point(
    supervisor,
    {
        "resume": "resume",
        "career": "career",
        "interview": "interview",
        "skill_gap": "skill_gap",
    }
)

# End Connections
graph.add_edge("resume", END)
graph.add_edge("career", END)
graph.add_edge("interview", END)
graph.add_edge("skill_gap", END)

# Compile Graph
app_graph = graph.compile()