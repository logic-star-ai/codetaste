# Consolidate DAG scheduling parameters into single `schedule` argument

Consolidate `schedule_interval`, `timetable`, and `schedule_on` parameters into a unified `schedule` parameter that accepts cron expressions, timedelta objects, Timetable instances, or Dataset lists.