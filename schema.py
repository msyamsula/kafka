key_schema_avg_str = """
{
    "name": "average_key",
    "type": "int"
}
"""

key_schema_rank_str = """
{
    "name": "rank_key",
    "type": "int"
}
"""

value_schema_avg_str = """
{
    "name": "average_value",
    "type": "record",
    "fields": [
        {"name": "student_id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "average", "type": "int"}
    ]
}
"""

value_schema_rank_str = """
{
    "name": "rank_value",
    "type": "record",
    "fields": [
        {"name": "student_id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "average", "type": "int"},
        {"name": "ranking", "type": "int"}
    ]
}
"""