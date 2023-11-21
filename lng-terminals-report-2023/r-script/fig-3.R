#install.packages("devtools")
library(devtools)
load_all('/Users/Baird/Dropbox/_git_ALL/_github-repos-gem/gemplot/')

# The first step here is to load the packages that we will need to work with the data and create the visualisations
library(tidyverse) # loads in tidyverse packages
library(readxl) # used to load in excel files
library(googlesheets4) # used to load data directly from Google sheets
library(gemplot) # used to draw plots in GEM style
library(ggimage) # used to add flags using geom_image functions from ggimage\
library(grid) # used to draw extra text grobs for tweaking charts
library(cowplot) # used to combine plots together
library(ggalt) # used for dumbell charts
library(treemapify) # used for drawing treemaps in ggplot
library(reactable) # used for displaying tables
# library(reactablefmtr) # added styling options for reactable tables
library(ggmosaic)
library(ggtext)

options(scipen = 999)
`%!in%` <- Negate(`%in%`)

#install.packages("extrafont")
library(extrafont)

#install.packages("gfonts")
library(gfonts)

#install.packages("ggtext")
#install.packages("tidyverse")
#install.packages("readxl")
##install.packages("gemplot")
#install.packages("ggimage")
##install.packages("grid")
#install.packages("cowplot")
#install.packages("ggalt")
#install.packages("treemapify")
#install.packages("reactable")
#install.packages("ggmosaic")




lng_capex_by_region <-
  googlesheets4::read_sheet("https://spreadsheets/d/1vdwrxwR0k8kwDrwneRsNchDNQ96U5D3cO8BLZaAb15o/edit#gid=2130887971",
                            sheet = "Figure 3 - total reg capex for imp and exp",
                            skip = 0)#,
                            #col_names=TRUE )

lng_capex_by_region
lng_capex_by_region$RegionSubregion

lng_terminals_by_continent <-
  lng_capex_by_region |>
  filter(`RegionSubregion` %in% c("Africa", "Americas", "Asia", "Europe", "Oceania"))

lng_terminals_by_continent

lng_terminals_by_subregion <-
  lng_capex_by_region |>
  filter(`RegionSubregion` %!in% c("Africa", "Americas", "Asia", "Europe", "Oceania", "Total"))

lng_terminals_by_subregion

# trying this out with continental subgroups
# data needs formatting to do that first
#
lng_capex_by_continent_with_region <-
  lng_terminals_by_subregion |>
  mutate(Continent = case_when(
    `RegionSubregion` == "Northern Africa" | `RegionSubregion` == "Sub-Saharan Africa" ~ "Africa",
    `RegionSubregion` == "Latin America and the Caribbean" | `RegionSubregion` == "Northern America" ~ "Americas",
    `RegionSubregion` == "Central Asia" | `RegionSubregion` == "Eastern Asia" | `RegionSubregion` == "South-eastern Asia" | `RegionSubregion` == "Southern Asia" | `RegionSubregion` == "Western Asia" ~ "Asia",
    `RegionSubregion` == "Eastern Europe" | `RegionSubregion` == "Northern Europe" | `RegionSubregion` == "Southern Europe" | `RegionSubregion` == "Western Europe" ~ "Europe",
    `RegionSubregion` == "Australia and New Zealand" | `RegionSubregion` == "Melanesia" ~ "Oceania",
    TRUE ~ "Other"
  )
  )


lng_capex_by_continent_with_region
lng_capex_by_continent_with_region <-
lng_capex_by_continent_with_region |> dplyr::mutate(RegionSubregion = factor(RegionSubregion, levels = c(
  "Eastern Asia",
  "Western Asia",
  "South-eastern Asia",
  "Southern Asia",
  "Central Asia",
  "Eastern Europe",
  "Northern Europe",
  "Southern Europe",
  "Western Europe",
  "Latin America and the Caribbean",
  "Northern America",
  "Northern Africa",
  "Sub-Saharan Africa",
  "Australia and New Zealand",
  "Melanesia")))

lng_capex_by_continent_with_region

#

lng_terminal_capex_by_continent_and_subgroup_plot <-
  ggplot(lng_capex_by_continent_with_region |>
           dplyr::select(RegionSubregion,Continent,InDev),
         aes(area = InDev,
             fill = RegionSubregion,
             subgroup = Continent,
             subgroup2 = RegionSubregion)) +
  geom_treemap(colour = "white",
               start = "topleft") +
  geom_treemap_subgroup_border(start = "topleft",
                               colour = "white",
                               size = 4) +
  geom_treemap_subgroup2_border(start = "topleft",
                                colour = "white",
                                size = 0.5) +
  geom_treemap_text(aes(label = paste0(`RegionSubregion`, "\n", round(`InDev`, digits=1), " mtpa")),
                    size = 14,
                    reflow = TRUE,
                    #min.size = 12,
                    min.size=9,
                    colour = "white",
                    family = "Open Sans",
                    fontface = "bold",
                    start = "topleft",
                    lineheight = 1,
                    padding.x = grid::unit(5, "mm"),
                    padding.y = grid::unit(5, "mm")) +

  scale_fill_manual(values =
                      lng_capex_by_continent_with_region$Colors

  gem_style() +
  geom_segment(x = 0.55, y = -0.025,
               xend = 0.55, yend = -0.1,
               lineend='round',
               colour = "white",
               size = 1.2) +
  geom_segment(x = 0.55, y = -0.025,
               xend = 0.55, yend = -0.065,
               lineend='round',
               size = 0.4) +
  ggtext::geom_richtext(x = 0.45, y = -0.07,
                        label = "Western Asia<br>8.1 mtpa",
                        hjust = 0,
                        vjust = 1,
                        size =4.5,
                        family = "Open Sans",
                        label.size = NA,
                        fill = "white") +
  # # eastern europe
  # geom_segment(x = 0.75, y = -0.015,
  #              xend = 0.75, yend = -0.1,
  #              lineend='round',
  #              colour = "white",
  #              size = 1.2) +
  # geom_segment(x = 0.75, y = -0.015,
  #              xend = 0.75, yend = -0.065,
  #              lineend='round',
  #              size = 0.4) +
  # ggtext::geom_richtext(x = 0.65, y = -0.07,
  #                       label = "Eastern Europe<br>10.4 mtpa",
  #                       hjust = 0,
  #                       vjust = 1,
  #                       size =4.5,
  #                       family = "Open Sans",
  #                       label.size = NA,
  #                       fill = "white") +
  geom_segment(x = .995, y = -0.015,
               xend = .995, yend = -0.1,
               lineend='round',
               colour = "white",
               size = 1.2) +
  geom_segment(x = .995, y = -0.015,
               xend = .995, yend = -0.065,
               lineend='round',
               size = 0.4) +
  ggtext::geom_richtext(x = 0.92, y = -0.07,
                        label = "Australia and<br>New Zealand<br>5.2 mtpa",
                        hjust = 0,
                        vjust = 1,
                        size = 4.5,
                        family = "Open Sans",
                        label.size = NA,
                        fill = "white") +
  geom_segment(x = 1.01, y = 0.11,
               xend = 1.07, yend = 0.11,
               lineend='round',
               colour = "white",
               size = 1.2) +
  geom_segment(x = 1.01, y = 0.11,
               xend = 1.06, yend = 0.11,
               lineend='round',
               size = 0.4) +
  ggtext::geom_richtext(x = 1.06, y = 0.14,
                        label = "Northern Africa<br>5.2 mtpa",
                        hjust = 0,
                        vjust = 1,
                        size = 4.5,
                        family = "Open Sans",
                        label.size = NA,
                        fill = "white") +

  geom_segment(x = 1.01, y = 0.24,
               xend = 1.07, yend = 0.24,
               lineend='round',
               colour = "white",
               size = 1.2) +
  geom_segment(x = 1.01, y = 0.24,
               xend = 1.06, yend = 0.24,
               lineend='round',
               size = 0.4) +
  ggtext::geom_richtext(x = 1.06, y = 0.28,
                        label = "Sub-Saharan<br>Africa<br>8.6 mtpa",
                        hjust = 0,
                        vjust = 1,
                        size = 4.5,
                        family = "Open Sans",
                        label.size = NA,
                        fill = "white") +

  geom_segment(x = 1.01, y = 0.45,
               xend = 1.07, yend = 0.45,
               lineend='round',
               colour = "white",
               size = 1.2) +
  geom_segment(x = 1.01, y = 0.45,
               xend = 1.06, yend = 0.45,
               lineend='round',
               size = 0.4) +
  ggtext::geom_richtext(x = 1.06, y = 0.5,
                        label = "Eastern Europe<br>10.4 mtpa",
                        hjust = 0,
                        vjust = 1,
                        size = 4.5,
                        family = "Open Sans",
                        label.size = NA,
                        fill = "white") +


  theme(legend.position = "none",
        plot.margin = margin(5, 115, 50, 5),
        axis.line.x = element_blank()) +
  labs(title = "Where are LNG terminals in development?",
       size=14,
       subtitle = "Capacity of planned LNG import terminals by continent\nand region, in million tonnes per annum (mtpa)") +
    coord_cartesian(clip="off")


  lng_terminal_capex_by_continent_and_subgroup_plot
warnings()

add_gem_footer(lng_terminal_capex_by_continent_and_subgroup_plot,
               height_pixels = 660,
               source_name = "Source: Global Gas Infrastructure Tracker") |>

gemplot::save_gem_plot(save_filepath = "/Users/baird/Dropbox/_git_ALL/_github-repos-gem/GOIT-GGIT-research/lng-terminals-report-2023/r-script/Fig3-lng-terminal-capex-estimates.png",
                         height_pixels = 660, width_pixels=660)


