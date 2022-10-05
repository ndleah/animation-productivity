library(arrow)
library(dplyr)

timesheets <- read_parquet("./data/timesheets/timesheet_data.parquet")

unique(timesheets$task)

timesheets$overhead <- timesheets$task %in% c("td", "meeting", "prod", "training", "supervision", NA)

test <- timesheets %>% 
  select(task, dept, overhead, days_logged) %>% 
  mutate(days_logged = as.double(days_logged)) %>% 
  group_by(dept, overhead) %>% 
  summarize(OverheadDays = sum(ifelse(overhead, days_logged, 0)), )


