
CREATE TABLE IF NOT EXISTS draw_results (
    issue_number TEXT PRIMARY KEY,
    draw_date TEXT NOT NULL,
    red_ball_1 INTEGER NOT NULL,
    red_ball_2 INTEGER NOT NULL,
    red_ball_3 INTEGER NOT NULL,
    red_ball_4 INTEGER NOT NULL,
    red_ball_5 INTEGER NOT NULL,
    blue_ball_1 INTEGER NOT NULL,
    blue_ball_2 INTEGER NOT NULL
);

