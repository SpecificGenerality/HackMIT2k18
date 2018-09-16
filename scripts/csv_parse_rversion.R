setwd("/Users/dfan/Dropbox (Personal)/Programming/Projects/HackMIT2k18")
df <- read.csv("data/DisasterDeclarationsSummaries.csv")
columns <- c("state", "fyDeclared", "incidentType", "declaredCountyArea")
df <- df[which(df$fyDeclared >= 1990), columns]
df$declaredCountyArea <- gsub('* \\(County\\)', '', df$declaredCountyArea)

fips <- read.csv("https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt",
                  col.names = c("state.abb", "statefp", "countyfp", "county.name", "classfp"),
                  colClasses = rep("character", 5))
df$FIPS <- apply(df, 1, function(vec) {
  temp_fips <- fips[which(fips$state.abb == vec['state']), ]
  index <- grep(vec['declaredCountyArea'], temp_fips$county.name)[1]
  paste(temp_fips[index, 'statefp'], temp_fips[index, 'countyfp'], sep="")
})

disaster_types = c("Tornado", "Fire", "Flood", "Snow", "Hurricane", "Earthquake")
result = data.frame()
for (year in unique(df$fyDeclared)) {
  temp_df <- df[which(df$fyDeclared == year), ]
  temp_append_df <- data.frame()
  temp_append_df$FIPS <- temp_df$FIPS
  for (disaster in disaster_types) {
    temp_temp_df <- temp_df[which(temp_df$incidentType == disaster)]
    temp_append_df$disaster <- sapply(temp_append_df$FIPS, function(x) {
      length(which(temp_temp_df$FIPS == x))
    })
  }
  result <- rbind(result, temp_append_df)
}

