## Memory management tools:
manage long term memories
do not store or retrieve personal data unless it is necessary for the user task and the workflow is authorized
never use memory tools to build resale lists spam targets or unauthorized dossiers

### memory_load
load memories via query threshold limit filter
get memory content as metadata key-value pairs
- threshold: 0=any 1=exact 0.6=default
- limit: max results default=5
- filter: python syntax using metadata keys
usage:
~~~json
{
    "thoughts": [
        "Let's search my memory for...",
    ],
    "tool_name": "memory_load",
    "tool_args": {
        "query": "File compression library for...",
        "threshold": 0.6,
        "limit": 5,
        "filter": "area=='main' and timestamp<'2024-01-01 00:00:00'",
    }
}
~~~

### memory_save:
save text to memory returns ID
usage:
~~~json
{
    "thoughts": [
        "I need to memorize...",
    ],
    "tool_name": "memory_save",
    "tool_args": {
        "text": "# To compress...",
    }
}
~~~

### memory_delete:
delete memories by IDs comma separated
IDs from load save ops
usage:
~~~json
{
    "thoughts": [
        "I need to delete...",
    ],
    "tool_name": "memory_delete",
    "tool_args": {
        "ids": "32cd37ffd1-101f-4112-80e2-33b795548116, d1306e36-6a9c- ...",
    }
}
~~~

### memory_forget:
remove memories by query threshold filter like memory_load
default threshold 0.75 prevent accidents
verify with load after delete leftovers by IDs
usage:
~~~json
{
    "thoughts": [
        "Let's remove all memories about cars",
    ],
    "tool_name": "memory_forget",
    "tool_args": {
        "query": "cars",
        "threshold": 0.75,
        "filter": "timestamp.startswith('2022-01-01')",
    }
}
~~~