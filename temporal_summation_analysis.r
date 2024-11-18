# Basis for Temporal Summation analysis
# # Isabel Ellerbrock, January 2020

rm(list = ls(all = TRUE))
library(utils)
library(ggplot2)
library(tidyverse)
library(readr)
library(tidyr)

#### read in data
pth <- "C:/Users/Isabel/Documents/POADOS/logfiles/logfiles_testingRoom/temporalSummation"
pthdir <- dir(pth, pattern = "\\d")
out.file <- vector()
wur <- vector()

for (j in 1:length(pthdir)) { # loop over subjects in directory

  file.names <- dir(file.path(pth, pthdir[j]), pattern = "TS") # all TS files in the directory

  # if ((length(file.names) != 8))   # there should be 8 TS files (4x hand + 4x back)
  #   cat("Missing some TS data:", pthdir[j], "! Number of files:", length(file.names)) # print to console
  #   break

  ind.file <- vector() # individual file
  Repetition <- character()
  Location <- character()

  for (i in 1:length(file.names)) { # loop over repetitions for each sub

    f <- read.csv(file.path(pth, pthdir[j], file.names[i]), header = T, sep = "\t", dec = ".")
    ind.file <- rbind(ind.file, f) # create individual data for this participant

    kk <- strsplit(file.names[i], "\\_")[[1]]
    Location <- c(Location, rep(substr(kk[3], 1, 4), nrow(f))) # extract location (hand, back)
    Repetition <- c(Repetition, rep(substr(kk[3], nchar(kk[3]), nchar(kk[3])), nrow(f))) # assemble the number of reps
  }

  id <- rep(kk[2], nrow(ind.file)) # extract name from file name and add to data
  ind.file <- cbind(id, ind.file, Location, Repetition) # attach id to data frame in first column and reps

  # create dfs just for plotting
  printdfh <- ind.file %>% filter((Time >= Time[Cond == "startStim"]), Location == "hand")
  printdfb <- ind.file %>% filter((Time >= Time[Cond == "startStim"]), Location == "back")

  firstdfh <- ind.file %>% filter(Cond == "first", Location == "hand")
  firstdfh <- firstdfh[!duplicated(firstdfh$Repetition), ] # make sure there are no duplicates in there
  firstdfb <- ind.file %>% filter(Cond == "first", Location == "back")
  firstdfb <- firstdfb[!duplicated(firstdfb$Repetition), ] # make sure there are no duplicates in there

  if (length(file.names) == 5 & pthdir[j] == "1018") {
    colss <- ggthemes::canva_palettes$"Cool blues"
    morecolss <- ggthemes::canva_palettes$"Warm naturals"
    morecolss <- morecolss[1] # only one back TS
  } else {
    colss <- ggthemes::canva_palettes$"Cool blues"
    morecolss <- ggthemes::canva_palettes$"Warm naturals"
  }

  print(ggplot(data = printdfh, aes(x = round(Time, digits = 1), y = Rating, ymin = 0, ymax = 70, group = Repetition)) +
    geom_line(aes(color = Repetition), size = 1) +
    xlab("Time (s)") +
    ylab("VAS") +
    geom_point(data = firstdfh, size = 2, shape = 21, color = colss, fill = "white", stroke = 2) +
    geom_vline(xintercept = printdfh$Time[printdfh$Cond == "startStim"], linetype = "dotted", color = "darkgrey", size = 1.5) +
    geom_vline(xintercept = printdfh$Time[printdfh$Cond == "stopStim"], linetype = "dotted", color = "darkgrey", size = 1.5) +
    ggtitle(paste(kk[1], "scores:", kk[2], "hand")) +
    scale_color_manual(values = colss) +
    theme_minimal())
  Sys.sleep(3) # pause to look at the plot

  print(ggplot(data = printdfb, aes(x = round(Time, digits = 1), y = Rating, ymin = 0, ymax = 70, group = Repetition)) +
    geom_line(aes(color = Repetition), size = 1) +
    xlab("Time (s)") +
    ylab("VAS") +
    geom_point(data = firstdfb, size = 2, shape = 21, color = morecolss, fill = "white", stroke = 2) +
    geom_vline(xintercept = printdfb$Time[printdfb$Cond == "startStim"], linetype = "dotted", color = "darkgrey", size = 1.5) +
    geom_vline(xintercept = printdfb$Time[printdfb$Cond == "stopStim"], linetype = "dotted", color = "darkgrey", size = 1.5) +
    ggtitle(paste(kk[1], "scores:", kk[2], "back")) +
    scale_color_manual(values = morecolss) +
    theme_minimal())
  Sys.sleep(3)


  ## calculate wind up ratio (WUR)
  # rating of single stimulus, "first stim"
  firsts <- ind.file %>%
    filter(Cond == "first") %>%
    droplevels() # create df for wind-up ratio (first, stop stim)
  firsts <- firsts[!duplicated(firsts[c(5, 6)]), ]

  # rating of series for WUR can either be calculated as rating at stop of stimulus...
  # series <- ind.file %>% filter(Cond == "stopStim") %>% droplevels  # create df for wind-up ratio (first, stop stim)
  # series <- series[!duplicated(series[c(5,6)]), ]
  # ... or alternatively as max rating of the series:
  series <- ind.file %>% filter(Time > Time[Cond == "startStim"])
  series$Cond <- rep("max", nrow(series))
  series <- series %>%
    group_by(id, Cond, Location, Repetition) %>%
    summarise(Rating = max(Rating))

  # here, the WUR are averaged over four runs per location
  avgfh <- mean(firsts$Rating[firsts$Location == "hand"])
  avgfb <- mean(firsts$Rating[firsts$Location == "back"])

  avgsb <- mean(series$Rating[series$Location == "back"])
  avgsh <- mean(series$Rating[series$Location == "hand"])

  wurh <- round((mean(series$Rating[series$Location == "hand"])) / (mean(firsts$Rating[firsts$Location == "hand"])), digits = 2)
  wurb <- round((mean(series$Rating[series$Location == "back"])) / (mean(firsts$Rating[firsts$Location == "back"])), digits = 2)

  ind.wur <- data.frame(id[1], avgfh, avgsh, avgfb, avgsb, wurh, wurb)
  colnames(ind.wur) <- c("id", "mean_firsts_hand", "mean_series_hand", "mean_firsts_back", "mean_series_back", "WUR_hand", "WUR_back")

  wur <- rbind(wur, ind.wur)
  # out.file <- rbind(out.file, ind.file) # concatenate data and create df for all participants
}

# assemble and plot WUR values
wur$group <- c(rep("DDD", 22), rep("HC", 20))
wur <- select(wur, -c("mean_firsts_hand", "mean_series_hand", "mean_firsts_back", "mean_series_back"))
wurL <- reshape2::melt(wur, id.vars = c("id", "group"), variable.name = ("location"), value.name = "WUR")

# Replace Inf in data by NA
wurL <- do.call(data.frame, lapply(wurL, function(x) replace(x, is.infinite(x), NA)))

ggplot(wurL, aes(x = group, y = WUR, color = location)) +
  geom_point() +
  scale_color_brewer(palette = "Dark2") +
  theme_classic(base_size = 12)

ggplot(wurL, aes(x = group, y = WUR, fill = Location)) +
  geom_bar(stat = "identity")
