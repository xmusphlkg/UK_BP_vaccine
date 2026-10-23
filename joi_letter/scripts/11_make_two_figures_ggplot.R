# Compatibility entry point for the canonical two-figure renderer.
# The implementation lives in 09_make_figure_ggplot.R so one source of truth
# controls data validation, panel construction and publication exports.
renderer <- if (file.exists(file.path("manuscript", "joi_letter", "scripts",
                                      "09_make_figure_ggplot.R"))) {
  file.path("manuscript", "joi_letter", "scripts", "09_make_figure_ggplot.R")
} else {
  file.path("scripts", "09_make_figure_ggplot.R")
}
source(renderer)
