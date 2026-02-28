import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.environ["DATABASE_URL"])

query = """
WITH team_rosters AS (
  SELECT
    p.match_id,
    m.patch,
    m.queue_id,
    p.team_id,
    bool_or(p.win) AS win,
    array_agg(p.champion_id ORDER BY p.champion_id) AS champs,
    count(*) AS n_players
  FROM participants p
  JOIN matches m ON m.match_id = p.match_id
  GROUP BY p.match_id, m.patch, m.queue_id, p.team_id
),
team_tags AS (
  SELECT
    p.match_id,
    p.team_id,
    ct.tag,
    count(*)::int AS tag_count
  FROM participants p
  JOIN champion_tag ct ON ct.champion_id = p.champion_id
  GROUP BY p.match_id, p.team_id, ct.tag
)
SELECT
  tr.match_id,
  tr.patch,
  tr.queue_id,
  tr.team_id,
  tr.win,
  tr.champs,
  jsonb_object_agg(tt.tag, tt.tag_count ORDER BY tt.tag) AS tag_counts
FROM team_rosters tr
LEFT JOIN team_tags tt
  ON tt.match_id = tr.match_id AND tt.team_id = tr.team_id
WHERE tr.n_players = 5
GROUP BY tr.match_id, tr.patch, tr.queue_id, tr.team_id, tr.win, tr.champs
"""

df = pd.read_sql(query, conn)
df.to_csv("aram_team_dataset.csv", index=False)