"""
Module with all sql queries as immutable maps (MappingProxyType)
"""
from types import MappingProxyType

INSERT = MappingProxyType(
    {
        "json_array": """
INSERT INTO {schema}.{table}
SELECT *
FROM json_populate_recordset(null::{schema}.{table},
                             {json})
ON CONFLICT DO NOTHING
"""
    }
)

FETCH = MappingProxyType(
    {
        "rooms_with_number_of_students": """
SELECT {rooms_table}.id,
       {rooms_table}.name,
       count({students_table}) AS students_count
FROM {schema}.{rooms_table}
LEFT JOIN {schema}.{students_table} ON {rooms_table}.id = {students_table}.room
GROUP BY {rooms_table}.id,
         {rooms_table}.name
""",
        "rooms_with_five_min_avg_students_ages": """
SELECT {rooms_table}.id,
       {rooms_table}.name,
       round(avg(extract(YEAR FROM current_date) - extract(YEAR FROM {students_table}.birthday))) AS avg_age
FROM {schema}.{rooms_table}
INNER JOIN {schema}.{students_table} ON {rooms_table}.id = {students_table}.room
GROUP BY {rooms_table}.id,
         {rooms_table}.name
ORDER BY avg_age
LIMIT 5
""",
        "rooms_with_five_max_students_age_diff": """
SELECT {rooms_table}.id,
       {rooms_table}.name,
       max(extract(YEAR FROM current_date) - extract(YEAR FROM {students_table}.birthday)) -
       min(extract(YEAR FROM current_date) - extract(YEAR FROM {students_table}.birthday)) AS age_diff
FROM {schema}.{rooms_table}
INNER JOIN {schema}.{students_table} ON {rooms_table}.id = {students_table}.room
GROUP BY {rooms_table}.id,
         {rooms_table}.name
HAVING count({students_table}) > 1
ORDER BY age_diff DESC 
LIMIT 5
""",
        "rooms_with_different_students_gender": """
SELECT {rooms_table}.id,
       {rooms_table}.name,
       count({students_table}) FILTER (WHERE {students_table}.sex = 'M') AS m_count,
       count({students_table}) FILTER (WHERE {students_table}.sex = 'F') AS f_count
FROM {schema}.{rooms_table}
INNER JOIN {schema}.{students_table} ON {rooms_table}.id = {students_table}.room
GROUP BY {rooms_table}.id,
         {rooms_table}.name
HAVING count(DISTINCT {students_table}.sex) > 1
""",
    }
)
