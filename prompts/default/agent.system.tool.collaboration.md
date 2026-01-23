### collaboration_tool

Interact with the real-time collaborative document space.
Allows reading, writing (overwrite), and appending to shared documents.
Use this to collaborate with human users or other agents.
Default doc_id is "default".

usage:

1. Read document
~~~json
{
    "thoughts": [
        "Checking what is in the shared document..."
    ],
    "tool_name": "collaboration_tool",
    "tool_args": {
        "action": "read",
        "doc_id": "default"
    }
}
~~~

2. Append to document
~~~json
{
    "thoughts": [
        "Adding my analysis to the shared doc..."
    ],
    "tool_name": "collaboration_tool",
    "tool_args": {
        "action": "append",
        "content": "Here is the summary of the data...",
        "doc_id": "default"
    }
}
~~~

3. Overwrite document
~~~json
{
    "thoughts": [
        "Clearing the doc and starting fresh..."
    ],
    "tool_name": "collaboration_tool",
    "tool_args": {
        "action": "write",
        "content": "Meeting Agenda:\n1. Intro...",
        "doc_id": "default"
    }
}
~~~
