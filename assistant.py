"""
assistant.py

Main assistant class.

Responsibilities:
- Connect to OpenAI
- Send the system prompt
- Give the model the list of available tools
- Execute the requested tool
- Return the final answer
"""

import json

from openai import OpenAI

from prompts import SYSTEM_PROMPT
from tools.registry import TOOLS
from config import MODEL_NAME
from typing import TypedDict

from langgraph.graph import StateGraph, END

class AssistantState(TypedDict):
    question: str
    answer: str

class HealthAssistant:

    def __init__(self, base_url: str, api_key: str):

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        graph = StateGraph(AssistantState)

        graph.add_node("llm", self._assistant_node)

        graph.set_entry_point("llm")

        graph.add_edge("llm", END)

        self.graph = graph.compile()

        self.last_tool_calls = []


    def _build_tools(self):

        tools = []

        for tool in TOOLS:

            schema = tool.input_model.model_json_schema()

            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": schema,
                    },
                }
            )

        return tools


    def _execute_tool(self, tool_name, arguments):

        tool = next(
            (t for t in TOOLS if t.name == tool_name),
            None
        )

        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        inputs = tool.input_model(**arguments)

        result = tool.run(inputs)

        if hasattr(result, "model_dump"):
            result_display = result.model_dump()
        else:
            result_display = result

        self.last_tool_calls.append({
            "tool": tool_name,
            "arguments": arguments,
            "result": result_display
        })

        return result
    
    def _assistant_node(self, state: AssistantState):

        answer = self._chat(state["question"])

        return {
            "question": state["question"],
            "answer": answer
        }


    def _chat(self, question: str) -> str:

        self.last_tool_calls = []

        self.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=self.messages,
            tools=self._build_tools(),
            tool_choice="auto",
        )

        message = response.choices[0].message



        if not message.tool_calls:

            answer = message.content

            self.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            return answer


        self.messages.append(message)

        for call in message.tool_calls:

            tool_name = call.function.name

            arguments = json.loads(call.function.arguments)

            result = self._execute_tool(
                tool_name,
                arguments
            )

            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(
                        result,
                        default=str
                    ),
                }
            )



        final = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=self.messages,
        )

        answer = final.choices[0].message.content

        self.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        return answer

    def ask(self, question: str) -> str:

        result = self.graph.invoke(
            {
                "question": question,
                "answer": ""
            }
        )

        return result["answer"]
