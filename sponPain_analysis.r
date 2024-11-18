# Basis for Spontaneous Pain analysis of behavioural data
# Isabel Ellerbrock, October 2019

rm(list = ls(all = TRUE))
library(utils)
library(ggplot2)
library(tidyverse)
library(readr)

# read in data
pth <- "C:/Users/Isabel/Documents/POADOS/logfiles/logfiles_MR/SponPain"
file.names <- dir(pth, pattern = "sponPain")
out.file <- vector()

for (j in 1:length(file.names)) {
  file <- read.table(file.path(pth, file.names[j]), header = TRUE, sep = "\t")
  kk <- strsplit(file.names[j], "\\_")[[1]]
  id <- rep(kk[2], nrow(file)) # extract name from file name and add to data
  file <- cbind(id, file) # attach id to data frame in first column

  out.file <- rbind(out.file, file) # concatenate data and create df of original data for all participants

  if (tail(file$Time, n = 1) < 600) { # make sure there are values until 600 frames, right-pad last rating
    paddedtailtime <- round(tail(file$Time, n = 1), digits = 0):600
    paddedtailscore <- rep(tail(file$Rating, n = 1), length(paddedtailtime))
    paddedid <- rep(id[1], length(paddedtailtime))
    tailfile <- data.frame(paddedid, paddedtailtime, paddedtailscore)
    colnames(tailfile) <- c("id", "Time", "Rating")
    afile <- dplyr::bind_rows(file, tailfile)
  } else {
    afile <- file
  }

  if (head(file$Time, n = 1) > 1) {
    paddedheadtime <- 1:trunc(head(file$Time, n = 1), digits = 0)
    paddedheadscore <- rep(0, length(paddedheadtime))
    paddedid <- rep(id[1], length(paddedheadtime))
    headfile <- data.frame(paddedid, paddedheadtime, paddedheadscore)
    colnames(headfile) <- c("id", "Time", "Rating")

    if (exists("afile")) {
      afile <- dplyr::bind_rows(headfile, afile)
    } else {
      afile <- file
    }
  }

  # plot data
  if (id[1] < 4000) {
    print(ggplot(data = afile, aes(x = Time, y = Rating, ymin = 0, ymax = 50, xmin = 0, xmax = 600)) +
      geom_line(size = 2) +
      theme_minimal() +
      xlab("Time") +
      ylab("Rating") +
      ggtitle(paste("spontaneous pain ratings: ", kk[2])))
  } else {
    print(ggplot(data = afile, aes(x = Time, y = Rating, ymin = 0, ymax = 50, xmin = 0, xmax = 600)) +
      geom_line(size = 2) +
      theme_minimal() +
      xlab("Time") +
      ylab("Rating") +
      ggtitle(paste("spontaneous unpleasantness ratings: ", kk[2])))
  }

  #  Sys.sleep(3) # pause for 3 sec to look at the plot
}

inx <- out.file %>%
  group_by(id) %>%
  summarise_at(vars(Rating), list(mean = mean, sd = sd, med = median, max = max))
