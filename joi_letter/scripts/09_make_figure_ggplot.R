# JOI Letter figures.
#
# Figure 1: observed coverage, the screening-method incidence curve, and the
#           national-target reductions beside the age-structured diagnostic.
# Figure 2: published versus stack individual effectiveness, the seasonal
#           prior, and held-out folds on each series' own scale.

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(readr)
  library(scales)
  library(tidyr)
  library(patchwork)
  library(grid)
})

root <- if (dir.exists("manuscript/joi_letter")) "manuscript/joi_letter" else "."
source(file.path(root, "scripts/figure_style.R"))

out_dir <- file.path(root, "outputs/figures")
data_dir <- file.path(root, "data/derived")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(data_dir, recursive = TRUE, showWarnings = FALSE)

stop_if_missing <- function(path) {
  if (!file.exists(path)) stop("Required JOI Letter input is missing: ", path, call. = FALSE)
}

parse_month <- function(x) {
  x <- trimws(as.character(x))
  x <- gsub("_", " ", x, fixed = TRUE)
  out <- as.Date(sub(" 00:00:00$", "", x), format = "%Y-%m-%d")
  missing <- is.na(out)
  if (any(missing)) out[missing] <- as.Date(paste0("01 ", x[missing]), format = "%d %b %Y")
  out
}

fmt_pct <- function(x, digits = 1) paste0(number(x, accuracy = 10^-digits, trim = TRUE), "%")
fmt_num <- function(x) comma(round(x))
year_of <- function(x) as.integer(format(x, "%Y"))
month_of <- function(x) as.integer(format(x, "%m"))
month_lab <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

# Sequential coverage colours. Red is reserved for the threshold miss in the
# ICB panel, so the scenario lines do not look like an alert scale.
target_cols <- c(`75%` = "#5B93C7", `80%` = "#2A6EBB", `90%` = "#123A63")
series_cols <- c(Observed = pub_colours$text, Predicted = pub_colours$blue)
mechanism_cols <- c("Legacy mapping" = pub_colours$blue,
                    "Walker-anchored" = pub_colours$orange)

panel_theme <- theme_publication(
  base_size = 8.2,
  grid = "y",
  show_titles = FALSE,
  plot_margin = margin(8, 10, 4, 8)
) +
  theme(
    text = element_text(family = "Arial", colour = pub_colours$text),
    plot.title = element_blank(),
    plot.subtitle = element_blank(),
    plot.caption = element_blank(),
    plot.tag = element_text(family = "Arial", face = "bold", size = 11,
                            colour = pub_colours$text, hjust = 0, vjust = 1),
    axis.title = element_text(size = 8.2, face = "bold"),
    axis.text = element_text(size = 7.4),
    legend.title = element_blank(),
    legend.text = element_text(size = 7.4),
    legend.position = "bottom",
    legend.key.height = unit(3.2, "mm"),
    legend.key.width = unit(6, "mm"),
    strip.text = element_text(size = 8, face = "bold"),
    plot.margin = margin(8, 10, 4, 8)
  )

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
under3_path <- file.path(data_dir, "joi_infant_under3_summary.csv")
coverage_icb_path <- file.path(data_dir, "ukhsa_coverage_icb_long.csv")
national_path <- file.path(data_dir, "ukhsa_coverage_national_monthly.csv")
annual_path <- file.path(data_dir, "ukhsa_coverage_annual.csv")
scenario_path <- file.path(data_dir, "joi_scenario_timeseries.csv")
validation_path <- file.path(data_dir, "joi_validation_timeseries.csv")
for (p in c(under3_path, coverage_icb_path, national_path, annual_path,
            scenario_path, validation_path)) stop_if_missing(p)

under3 <- read_csv(under3_path, show_col_types = FALSE) %>%
  mutate(coverage_pct = as.numeric(coverage_pct))
if (nrow(under3) != 8L) stop("Observed-baseline summary must contain eight rows.", call. = FALSE)

coverage_icb <- read_csv(coverage_icb_path, show_col_types = FALSE) %>%
  mutate(month_date = parse_month(month))
coverage_national <- read_csv(national_path, show_col_types = FALSE) %>%
  mutate(month_date = parse_month(month))
coverage_annual <- read_csv(annual_path, show_col_types = FALSE) %>%
  mutate(coverage_percent = as.numeric(coverage_percent))
if (nrow(coverage_annual) != 3L) {
  stop("Annual coverage ledger must contain the three fiscal-year estimates.", call. = FALSE)
}
coverage_annual$annual_date <- as.Date(c("2024-03-31", "2025-03-31", "2026-03-31"))

latest_month <- max(coverage_icb$month_date, na.rm = TRUE)
coverage_latest <- coverage_icb %>%
  filter(month_date == latest_month) %>%
  mutate(
    icb_name = gsub(" and ", " & ", icb_name, fixed = TRUE),
    gap_fill = if_else(coverage_percent < 75, "Below 75%", "75% or higher")
  )
if (nrow(coverage_latest) < 30L) stop("The latest ICB extract contains too few regions.", call. = FALSE)

scenario_ts <- read_csv(scenario_path, show_col_types = FALSE) %>%
  mutate(calendar_date = as.Date(calendar_date))
validation_ts <- read_csv(validation_path, show_col_types = FALSE) %>%
  mutate(period_start = as.Date(period_start), period_end = as.Date(period_end))
if (!"structural_seasonal_phase_days" %in% names(validation_ts) ||
    any(abs(validation_ts$structural_seasonal_phase_days - 300) > 1e-6)) {
  stop("Validation ledger is not the UK structural seasonal contract (phase day 300).", call. = FALSE)
}

target_lines <- tibble(target = c(75, 80, 90), label = paste0(c(75, 80, 90), "%"))
target_lines$label <- factor(target_lines$label, levels = c("75%", "80%", "90%"))

# ---------------------------------------------------------------------------
# Figure 1
# ---------------------------------------------------------------------------
annual_labels <- coverage_annual %>%
  mutate(label_y = coverage_percent + c(-3.8, 3.6, 3.6))
p1a <- ggplot(coverage_national, aes(month_date, coverage_percent)) +
  geom_hline(yintercept = c(75, 80, 90), linetype = "dashed",
             linewidth = 0.3, colour = pub_colours$reference) +
  annotate("text", x = as.Date("2023-04-15"), y = c(76.6, 81.6, 92.2),
           label = c("75%", "80%", "90%"), hjust = 0, size = 2.5,
           colour = pub_colours$muted_text) +
  geom_line(colour = pub_colours$orange, linewidth = 0.8) +
  geom_point(data = coverage_annual, aes(annual_date, coverage_percent),
             inherit.aes = FALSE, shape = 21, fill = "white",
             colour = pub_colours$blue, size = 2.4, stroke = 0.7) +
  geom_text(data = annual_labels, aes(annual_date, label_y, label = fmt_pct(coverage_percent, 1)),
            inherit.aes = FALSE, size = 2.7, colour = pub_colours$blue) +
  geom_vline(xintercept = as.Date("2024-09-01"), linetype = "dotted",
             linewidth = 0.35, colour = pub_colours$muted_text) +
  annotate("text", x = as.Date("2024-09-01"), y = 96, label = "RAVs",
           hjust = -0.12, size = 2.6, colour = pub_colours$muted_text) +
  scale_y_continuous(limits = c(50, 100), breaks = c(50, 60, 70, 80, 100),
                     labels = function(x) paste0(x, "%")) +
  scale_x_date(date_breaks = "6 months", date_labels = "%b\n%Y",
               expand = expansion(mult = c(0.02, 0.06))) +
  labs(x = NULL, y = "Antenatal coverage") +
  panel_theme +
  theme(legend.position = "none")

lowest <- coverage_latest %>% slice_min(coverage_percent, n = 1, with_ties = FALSE)
highest <- coverage_latest %>% slice_max(coverage_percent, n = 1, with_ties = FALSE)
n_below <- sum(coverage_latest$coverage_percent < 75)
icb_note <- sprintf(
  "%d of %d below 75%%\n%s to %s",
  n_below, nrow(coverage_latest),
  fmt_pct(lowest$coverage_percent, 1), fmt_pct(highest$coverage_percent, 1)
)
p1b <- ggplot(coverage_latest, aes(coverage_percent, fill = gap_fill)) +
  geom_histogram(binwidth = 2.5, boundary = 50, colour = "white",
                 linewidth = 0.25, position = "identity") +
  geom_vline(xintercept = c(75, 80, 90), linetype = "dashed",
             linewidth = 0.3, colour = pub_colours$reference) +
  annotate("text", x = 50.8, y = 10.65, hjust = 0, vjust = 1, size = 2.55,
           lineheight = 0.92, colour = pub_colours$text, label = icb_note) +
  scale_fill_manual(values = c("Below 75%" = pub_colours$red,
                                "75% or higher" = pub_colours$blue),
                    guide = "none") +
  scale_x_continuous(limits = c(50, 95), breaks = c(50, 60, 75, 80, 90),
                     labels = function(x) paste0(x, "%"),
                     expand = expansion(mult = c(0.01, 0.02))) +
  scale_y_continuous(limits = c(0, 11.2), breaks = c(0, 4, 8),
                     expand = expansion(mult = c(0, 0))) +
  labs(x = paste0("ICB coverage, ", format(latest_month, "%B %Y")),
       y = "Number of ICBs") +
  panel_theme +
  theme(legend.position = "none")

# Reported contrast: Walker's window VE applied to coverage. The transmission
# stack is drawn beside it. Entry 0.02 + 0.55*uptake, exponential residence
# 180 days against a 0.25-year bin, and the legacy composite are the stack's
# own factors. They are not a second estimate of the published VE.
walker_ve <- 0.846
ve_lo <- 0.769
ve_hi <- 0.897
baseline_uptake <- 0.73
phi <- 180 / (180 + 0.25 * 365)
legacy_ve <- 1 - (1 - 0.75 * 0.55) * (1 - 0.75 * 0.92)
birth_exposure <- function(uptake) pmin(0.75, 0.02 + 0.55 * uptake)
screen_ratio <- function(uptake, ve) (1 - uptake * ve) / (1 - baseline_uptake * ve)
stack_ratio <- function(uptake) {
  e0 <- birth_exposure(baseline_uptake)
  (1 - birth_exposure(uptake) * phi * legacy_ve) / (1 - e0 * phi * legacy_ve)
}
icb_reduction <- 100 * (1 - (1 - 0.90 * walker_ve) / (1 - 0.544 * walker_ve))
if (abs(icb_reduction - 55.7964) > 0.01) {
  stop("Lowest-ICB contrast left 55.80%.", call. = FALSE)
}
if (abs(phi - 180 / 271.25) > 1e-12) stop("Person-time fraction left the 91.25-day bin.", call. = FALSE)
if (abs(legacy_ve - 0.817875) > 1e-12) stop("Legacy composite left 0.817875.", call. = FALSE)

curve <- tibble(uptake = seq(0.50, 0.95, length.out = 250)) %>%
  mutate(
    walker = screen_ratio(uptake, walker_ve),
    walker_slow = screen_ratio(uptake, ve_lo),
    walker_fast = screen_ratio(uptake, ve_hi),
    stack = stack_ratio(uptake)
  )
floors <- tibble(uptake = c(0.75, 0.80, 0.90)) %>%
  mutate(walker = screen_ratio(uptake, walker_ve))
p1c <- ggplot(curve, aes(uptake, walker)) +
  geom_ribbon(aes(ymin = walker_fast, ymax = walker_slow), fill = "#D6E4F5", colour = NA) +
  geom_hline(yintercept = 1, linewidth = 0.3, colour = pub_colours$reference) +
  geom_line(aes(y = stack), linetype = "dashed", linewidth = 0.7, colour = "#8A8D8F") +
  geom_line(linewidth = 0.9, colour = pub_colours$blue) +
  geom_point(data = floors, shape = 21, fill = "white", colour = pub_colours$blue,
             size = 2.3, stroke = 0.7) +
  geom_point(data = tibble(uptake = baseline_uptake, walker = 1),
             shape = 21, fill = pub_colours$text, colour = pub_colours$text, size = 2.5) +
  annotate("text", x = 0.805, y = 0.50, hjust = 0, vjust = 0, size = 2.45,
           colour = pub_colours$blue, label = "Walker, 84.6%") +
  annotate("text", x = 0.52, y = 1.22, hjust = 0, size = 2.45, colour = "#8A8D8F",
           label = "Age-structured model") +
  scale_x_continuous(limits = c(0.50, 0.95), breaks = c(0.50, 0.73, 0.80, 0.90),
                     labels = function(x) paste0(round(100 * x), "%"),
                     expand = c(0, 0)) +
  scale_y_continuous(limits = c(0.40, 1.70), breaks = c(0.6, 1.0, 1.4),
                     expand = c(0, 0)) +
  labs(x = "Antenatal uptake", y = "Infant cases relative\nto 73% coverage") +
  panel_theme +
  theme(legend.position = "none", plot.margin = margin(6, 8, 4, 6))

model_rows <- under3 %>%
  filter(anchor == "Legacy mapping", !is.na(coverage_pct)) %>%
  transmute(
    floor = factor(paste0(as.integer(coverage_pct), "%"), levels = c("90%", "80%", "75%")),
    uptake = coverage_pct / 100,
    stack_pct = 100 * relative_reduction_cases
  )
if (nrow(model_rows) != 3L) stop("Legacy reduction panel requires three floors.", call. = FALSE)
readings <- model_rows %>%
  mutate(
    walker_pct = 100 * (1 - screen_ratio(uptake, walker_ve)),
    walker_lo = 100 * (1 - screen_ratio(uptake, ve_lo)),
    walker_hi = 100 * (1 - screen_ratio(uptake, ve_hi))
  ) %>%
  pivot_longer(c(walker_pct, stack_pct), names_to = "reading", values_to = "reduction") %>%
  mutate(
    lo = if_else(reading == "walker_pct", walker_lo, reduction),
    hi = if_else(reading == "walker_pct", walker_hi, reduction),
    reading = recode(reading,
                     walker_pct = "Walker, <3 months",
                     stack_pct = "Age-structured model"),
    reading = factor(reading, levels = c("Age-structured model", "Walker, <3 months"))
  )
walker_expected <- c(`90%` = 37.6079, `80%` = 15.4856, `75%` = 4.4245)
stack_expected <- c(`90%` = 5.9161, `80%` = 2.4396, `75%` = 0.6975)
check_reading <- function(name, expected) {
  got <- readings %>% filter(reading == name)
  gap <- abs(got$reduction - unname(expected[as.character(got$floor)]))
  if (any(gap > 0.02)) {
    stop(name, " drifted from the letter arithmetic.", call. = FALSE)
  }
}
check_reading("Walker, <3 months", walker_expected)
check_reading("Age-structured model", stack_expected)
write_csv(readings %>% select(floor, reading, reduction, lo, hi),
          file.path(data_dir, "joi_reduction_readings.csv"))

reading_cols <- c(
  "Walker, <3 months" = pub_colours$blue,
  "Age-structured model" = "#8A8D8F"
)
p1d <- ggplot(readings, aes(reduction, reading, fill = reading)) +
  geom_col(width = 0.72, colour = NA) +
  geom_errorbar(aes(xmin = lo, xmax = hi), orientation = "y",
                width = 0.18, linewidth = 0.35, colour = pub_colours$text) +
  geom_text(aes(x = hi, label = sprintf("%.2f%%", reduction)),
            hjust = -0.08, size = 2.15, colour = pub_colours$text) +
  facet_grid(floor ~ ., switch = "y", scales = "free_y") +
  scale_fill_manual(values = reading_cols, guide = "none") +
  scale_x_continuous(limits = c(0, 62), breaks = c(0, 15, 30, 45),
                     labels = function(x) paste0(x, "%"),
                     expand = c(0, 0)) +
  labs(x = "Reduction versus 73% coverage", y = NULL) +
  panel_theme +
  theme(
    legend.position = "none",
    strip.placement = "outside",
    strip.text.y.left = element_text(angle = 0, face = "bold", size = 8,
                                      colour = pub_colours$text),
    panel.spacing.y = unit(2.2, "mm"),
    axis.text.y = element_text(size = 6.6)
  )

figure1 <- (p1a | p1b) / (p1c | p1d) +
  plot_layout(heights = c(1, 1.28), widths = c(1, 1.08)) +
  plot_annotation(
    tag_levels = "A",
    theme = theme(plot.tag = element_text(family = "Arial", face = "bold",
                                          size = 11, colour = pub_colours$text))
  )

# Within-year index isolates the annual term. From 2030 every weekly peak
# falls in late December. The year-to-year band is narrow because the shape
# repeats. The stop below catches only a zero-width ribbon.
season_source <- scenario_ts %>%
  filter(mechanism == "history_matched_legacy",
         year_of(calendar_date) >= 2030,
         year_of(calendar_date) <= 2035,
         scenario == "current") %>%
  mutate(year = year_of(calendar_date), month = month_of(calendar_date))
if (nrow(season_source) < 100L) stop("Seasonal profile has too few weekly rows.", call. = FALSE)
week_peak <- season_source %>%
  group_by(year) %>%
  slice_max(infant_cases, n = 1, with_ties = FALSE) %>%
  ungroup()
if (any(!month_of(week_peak$calendar_date) %in% c(11, 12, 1))) {
  stop("A year in 2030–2035 does not peak in November–January.", call. = FALSE)
}

season_year <- season_source %>%
  group_by(year, month) %>%
  summarise(cases = mean(infant_cases), .groups = "drop") %>%
  group_by(year) %>%
  filter(mean(cases) > 1e-6) %>%
  mutate(index = cases / mean(cases)) %>%
  ungroup()
# lo/hi must be computed before `index`: dplyr summarise sees earlier
# expressions, so min(index) after index = mean(index) would copy the mean.
season_mean <- season_year %>%
  group_by(month) %>%
  summarise(lo = min(index), hi = max(index), index = mean(index), .groups = "drop")
peak_row <- season_mean %>% slice_max(index, n = 1, with_ties = FALSE)
trough_row <- season_mean %>% slice_min(index, n = 1, with_ties = FALSE)
season_ratio <- peak_row$index / trough_row$index
if (!is.finite(season_ratio) || season_ratio < 1.25) {
  stop("UK seasonal term is still flat in the prospective infant series (peak/trough ",
       signif(season_ratio, 3), ").", call. = FALSE)
}
if (max(season_mean$hi - season_mean$lo) < 1e-3) {
  stop("Seasonal year-range band has no width. lo and hi were not computed from the yearly index.", call. = FALSE)
}
if (!peak_row$month %in% c(10, 11, 12, 1, 2)) {
  stop("UK prospective seasonal peak is month ", peak_row$month,
       "; the structural prior peaks in autumn and cases should follow in Oct–Feb.",
       call. = FALSE)
}

write_csv(season_mean, file.path(data_dir, "joi_seasonal_profile.csv"))
p2b <- ggplot(season_mean, aes(month, index)) +
  geom_hline(yintercept = 1, linewidth = 0.3, colour = pub_colours$reference) +
  geom_ribbon(aes(ymin = lo, ymax = hi), fill = "#C5D8F0", colour = NA) +
  geom_line(colour = pub_colours$text, linewidth = 0.95) +
  geom_point(data = peak_row, colour = pub_colours$text, size = 2.2) +
  annotate("text", x = 1.15, y = 1.40, hjust = 0, vjust = 1, size = 2.55,
           lineheight = 0.92, colour = pub_colours$text,
           label = sprintf("%s peak\n%.2f × annual mean\nband: range across years",
                           month.name[peak_row$month], peak_row$index)) +
  scale_x_continuous(breaks = 1:12, labels = month_lab,
                     expand = expansion(mult = 0.02)) +
  scale_y_continuous(limits = c(0.75, 1.42),
                     breaks = c(0.8, 0.9, 1.0, 1.1, 1.2, 1.3),
                     expand = c(0, 0)) +
  labs(x = "Calendar month, 2030–2035",
       y = "0–2-month cases\nrelative to that year's mean") +
  panel_theme +
  theme(legend.position = "none")

# ---------------------------------------------------------------------------
# Figure 2
# ---------------------------------------------------------------------------
# Individual effectiveness implied by the stack. Entry 0.57 if the mother was
# vaccinated and 0.02 if she was not; person-time fraction phi; composite v.
individual_ve <- function(v) {
  protected <- function(entry) 1 - entry * phi * v
  1 - protected(0.57) / protected(0.02)
}
legacy_individual <- 100 * individual_ve(legacy_ve)
walker_individual <- 100 * individual_ve(walker_ve)
if (abs(legacy_individual - 30.1781289361592) > 1e-6) {
  stop("Legacy individual effectiveness left 30.178%.", call. = FALSE)
}
if (abs(walker_individual - 31.22767560860299) > 1e-6) {
  stop("Walker-composite individual effectiveness left 31.228%.", call. = FALSE)
}
account <- tibble(
  label = factor(
    c("Published, onset <2 months", "Published, infants <3 months",
      "Model, composite set to 84.6%", "Model, own composite"),
    levels = c("Model, own composite", "Model, composite set to 84.6%",
               "Published, infants <3 months", "Published, onset <2 months")
  ),
  estimate = c(86.2, 84.6, walker_individual, legacy_individual),
  lo = c(78.3, 76.9, walker_individual, legacy_individual),
  hi = c(91.3, 89.7, walker_individual, legacy_individual),
  kind = c("Published", "Published", "Age-structured model", "Age-structured model")
)
p2a <- ggplot(account, aes(estimate, label, fill = kind)) +
  geom_col(width = 0.68, colour = NA) +
  geom_errorbar(aes(xmin = lo, xmax = hi), orientation = "y",
                width = 0.16, linewidth = 0.35, colour = pub_colours$text) +
  geom_text(aes(x = hi, label = sprintf("%.1f%%", estimate)),
            hjust = -0.08, size = 2.4, colour = pub_colours$text) +
  scale_fill_manual(values = c("Published" = pub_colours$blue,
                               "Age-structured model" = "#8A8D8F"),
                    guide = "none") +
  scale_x_continuous(limits = c(0, 118), breaks = c(0, 30, 60, 90),
                     labels = function(x) paste0(x, "%"), expand = c(0, 0)) +
  labs(x = "Individual effectiveness", y = NULL) +
  panel_theme +
  theme(legend.position = "none", axis.text.y = element_text(size = 6.7))

validation_plot <- validation_ts %>%
  mutate(year = as.character(year)) %>%
  pivot_longer(c(reported_cases, predicted_cases), names_to = "series", values_to = "cases") %>%
  mutate(
    series = recode(series, reported_cases = "Observed", predicted_cases = "Predicted"),
    panel = factor(paste(series, year),
                   levels = c("Observed 2023", "Observed 2024",
                              "Predicted 2023", "Predicted 2024"))
  )
panel_totals <- validation_plot %>%
  group_by(panel) %>%
  summarise(total = sum(cases), x = min(period_start), ymax = max(cases), .groups = "drop")
p2c <- ggplot(validation_plot, aes(period_start, cases, colour = series)) +
  geom_line(linewidth = 0.6) +
  geom_text(data = panel_totals, aes(x = x, y = ymax, label = paste0("Total ", fmt_num(total))),
            inherit.aes = FALSE, hjust = 0, vjust = 1.1, size = 2.4,
            colour = pub_colours$muted_text) +
  facet_wrap(~panel, nrow = 2, scales = "free") +
  scale_colour_manual(values = series_cols, guide = "none") +
  scale_x_date(
    breaks = function(limits) {
      year <- format(limits[1], "%Y")
      as.Date(paste0(year, c("-01-01", "-05-01", "-09-01", "-12-01")))
    },
    labels = function(x) format(x, "%b"),
    expand = expansion(mult = c(0.02, 0.04))
  ) +
  scale_y_continuous(labels = comma, expand = expansion(mult = c(0.04, 0.18))) +
  labs(x = NULL, y = "Weekly statutory notifications") +
  panel_theme +
  theme(legend.position = "none", strip.text = element_text(size = 7.6, face = "bold"))

shape <- validation_ts %>%
  mutate(year = as.character(year), month = as.integer(format(period_start, "%m"))) %>%
  group_by(year, month) %>%
  summarise(Observed = sum(reported_cases), Predicted = sum(predicted_cases), .groups = "drop") %>%
  group_by(year) %>%
  mutate(Observed = Observed / mean(Observed), Predicted = Predicted / mean(Predicted)) %>%
  ungroup() %>%
  pivot_longer(c(Observed, Predicted), names_to = "series", values_to = "index")
write_csv(shape, file.path(data_dir, "joi_validation_seasonal_profile.csv"))
pred_2023 <- shape %>% filter(year == "2023", series == "Predicted")
pred_peak <- pred_2023$month[which.max(pred_2023$index)]
if (!pred_peak %in% c(10, 11, 12, 1, 2)) {
  stop("Validation prediction does not express an autumn/winter peak (month ",
       pred_peak, ").", call. = FALSE)
}
p2d <- ggplot(shape, aes(month, index, colour = series)) +
  geom_hline(yintercept = 1, linewidth = 0.3, colour = pub_colours$reference) +
  geom_line(linewidth = 0.75) +
  geom_point(size = 1.5) +
  facet_wrap(~year, nrow = 1, scales = "free_y") +
  scale_colour_manual(values = series_cols, name = NULL) +
  scale_x_continuous(breaks = c(1, 5, 8, 12), labels = month_lab[c(1, 5, 8, 12)],
                     expand = expansion(mult = 0.03)) +
  scale_y_continuous(expand = expansion(mult = c(0.06, 0.10))) +
  labs(x = "Month", y = "Monthly cases relative\nto that series' own mean") +
  panel_theme +
  theme(legend.position = "bottom", strip.text = element_text(size = 8, face = "bold"))

figure2 <- (free(p2a) | p2b) / (p2c | p2d) +
  plot_layout(heights = c(1, 1.2), widths = c(1, 1)) +
  plot_annotation(
    tag_levels = "A",
    theme = theme(plot.tag = element_text(family = "Arial", face = "bold",
                                          size = 11, colour = pub_colours$text))
  )

# ---------------------------------------------------------------------------
# Ledgers and export
# ---------------------------------------------------------------------------
write_csv(under3, file.path(data_dir, "joi_figure_panel_data.csv"))
write_csv(coverage_icb, file.path(data_dir, "joi_coverage_panel_data.csv"))
write_csv(validation_ts, file.path(data_dir, "joi_validation_panel_data.csv"))

save_figure <- function(plot, stem, width_mm, height_mm) {
  stem_path <- file.path(out_dir, stem)
  vector_dir <- file.path(out_dir, "vector")
  dir.create(vector_dir, recursive = TRUE, showWarnings = FALSE)
  grDevices::cairo_pdf(paste0(stem_path, ".pdf"), width = width_mm / 25.4,
                       height = height_mm / 25.4, family = "Arial", bg = "white")
  print(plot)
  grDevices::dev.off()
  if (requireNamespace("svglite", quietly = TRUE)) {
    svglite::svglite(file.path(vector_dir, paste0(stem, ".svg")),
                     width = width_mm / 25.4, height = height_mm / 25.4)
    print(plot)
    grDevices::dev.off()
  }
  ragg::agg_png(paste0(stem_path, ".png"), width = width_mm, height = height_mm,
                units = "mm", res = 300, background = "white")
  print(plot)
  grDevices::dev.off()
}

save_figure(figure1, "joi_maternal_coverage_impact_figure1", 183, 184)
save_figure(figure2, "joi_maternal_coverage_impact_figure2", 183, 172)
message("Wrote Figure 1 and Figure 2. Prospective seasonal peak month ",
        peak_row$month, " (index ", signif(peak_row$index, 3),
        "); validation predicted 2023 peak month ", pred_peak, ".")
