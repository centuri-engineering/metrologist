"""
# sql
SELECT cv_table_sd, cv_table_average, cv_table_nb_pixels, cv_table_cv_value FROM Cv

# sqlalchemy
colnames_list = ["cv_table_sd", "cv_table_average", "cv_table_nb_pixels", "cv_table_cv_value"]
sqlalchemy.select(Cv).where(user_table.c.name == colnames_list)
print(stmt)

# pandas
pandas.read_sql_table(Cv, DB_URL, colunms = colnames_list)
"""

import logging

log = logging.getLogger(__name__)
