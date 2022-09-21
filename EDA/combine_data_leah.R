# Load libraries
library(here)
library(tidyverse)
library(dplyr)                                    # Load dplyr package
library(readr)                                    # Load readr package
library(data.table)

#####################
# Timesheet data
#####################
setwd(here("data/timesheets"))

timesheet_df <- 
  # Identify all CSV files
  list.files(
    pattern = "*.csv", 
    full.names = TRUE) %>% 
  # Read all files and store as a list
  lapply(read_csv) %>% 
  # append rows to combine all datasets as 1
  rbindlist(use.names = TRUE, idcol = TRUE)

# save the df as csv file
write.csv(timesheet_df, here("data/timesheets_all.csv"), row.names = FALSE)


########################
# CPU version data
########################
setwd(here("data/versions"))

version_df <- 
  # Identify all CSV files
  list.files(
    pattern = "*.csv", 
    full.names = TRUE) %>% 
  # Read all files and store as a list
  lapply(read_csv) %>% 
  # append rows to combine all datasets as 1
  rbindlist(use.names = TRUE, idcol = TRUE)

# save the df as csv file
write.csv(version_df, here("data/versions_all.csv"), row.names = FALSE)

