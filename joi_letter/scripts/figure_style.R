# Copy this file into a project's figure-script directory and source it from
# individual renderers. It supplies a compact publication style, not a theme
# replacement mandate for projects that already have an established system.

suppressPackageStartupMessages({
  library(ggplot2)
  library(grid)
})

pub_colours <- list(
  white = "#FFFFFF",
  text = "#1B1B1B",
  muted_text = "#4B4D4F",
  reference = "#747678",
  light_grey = "#DADCDD",
  grid = "#F7F8F8",
  blue = "#2A6EBB",
  orange = "#E37222",
  green = "#69BE28",
  teal = "#00B2A9",
  red = "#CD202C",
  gold = "#F0AB00",
  purple = "#7D5CC6",
  pink = "#C50084"
)

pub_text <- list(
  base = 6.3,
  title = 6.8,
  subtitle = 5.5,
  axis_title = 6.3,
  axis_text = 5.6,
  axis_text_dense = 4.8,
  strip = 6.0,
  legend_title = 5.9,
  legend_text = 5.4,
  legend_text_dense = 4.8,
  tag = 8.0
)

pub_full_width_mm <- 183
pub_single_width_mm <- 89
pub_max_height_mm <- 170

theme_publication <- function(
    base_size = pub_text$base,
    grid = c("none", "x", "y", "both"),
    border = FALSE,
    show_titles = FALSE,
    plot_margin = margin(3, 4, 3, 4)) {
  grid <- match.arg(grid)
  delta <- base_size - pub_text$base
  scaled <- function(size) pmax(1, size + delta)
  grid_line <- element_line(linewidth = 0.14, colour = pub_colours$grid)

  theme_classic(base_size = base_size, base_family = "sans") +
    theme(
      text = element_text(
        family = "sans", colour = pub_colours$text, size = scaled(pub_text$base)
      ),
      axis.line = element_line(linewidth = 0.26, colour = pub_colours$text),
      axis.ticks = element_line(linewidth = 0.22, colour = pub_colours$text),
      axis.ticks.length = unit(1, "mm"),
      axis.text = element_text(size = scaled(pub_text$axis_text)),
      axis.title = element_text(size = scaled(pub_text$axis_title), face = "bold"),
      legend.title = element_text(size = scaled(pub_text$legend_title), face = "bold"),
      legend.text = element_text(size = scaled(pub_text$legend_text)),
      legend.key.height = unit(2.6, "mm"),
      legend.key.width = unit(4, "mm"),
      legend.spacing.x = unit(1.4, "mm"),
      legend.position = "bottom",
      legend.background = element_blank(),
      legend.box.background = element_blank(),
      panel.grid.major.x = if (grid %in% c("x", "both")) grid_line else element_blank(),
      panel.grid.major.y = if (grid %in% c("y", "both")) grid_line else element_blank(),
      panel.grid.minor = element_blank(),
      panel.border = if (border) {
        element_rect(colour = pub_colours$text, fill = NA, linewidth = 0.24)
      } else {
        element_blank()
      },
      plot.title = if (show_titles) {
        element_text(size = scaled(pub_text$title), face = "bold", hjust = 0,
                     margin = margin(b = 1.2))
      } else {
        element_blank()
      },
      plot.subtitle = if (show_titles) {
        element_text(size = scaled(pub_text$subtitle), colour = pub_colours$muted_text,
                     hjust = 0, margin = margin(b = 2.2))
      } else {
        element_blank()
      },
      strip.background = element_blank(),
      strip.text = element_text(size = scaled(pub_text$strip), face = "bold"),
      plot.tag = element_text(size = scaled(pub_text$tag), face = "bold"),
      plot.margin = plot_margin
    )
}

panel_tags <- function(plot) {
  if (!requireNamespace("patchwork", quietly = TRUE)) {
    stop("panel_tags() requires the patchwork package.", call. = FALSE)
  }
  plot + patchwork::plot_annotation(tag_levels = "a") &
    theme(plot.tag = element_text(face = "bold", size = pub_text$tag))
}

save_publication_figure <- function(
    plot, stem, directory, width_mm = pub_full_width_mm, height_mm, dpi = 600) {
  dir.create(directory, recursive = TRUE, showWarnings = FALSE)
  ggplot2::ggsave(
    file.path(directory, paste0(stem, ".png")), plot,
    width = width_mm, height = height_mm, units = "mm", dpi = dpi, bg = "white"
  )
  ggplot2::ggsave(
    file.path(directory, paste0(stem, ".pdf")), plot,
    width = width_mm, height = height_mm, units = "mm",
    device = grDevices::cairo_pdf, bg = "white"
  )
}

save_supplement_figure <- function(
    plot, stem, directory, width_mm = pub_full_width_mm, height_mm, dpi = 600) {
  dir.create(directory, recursive = TRUE, showWarnings = FALSE)
  ggplot2::ggsave(
    file.path(directory, paste0(stem, ".png")), plot,
    width = width_mm, height = height_mm, units = "mm", dpi = dpi, bg = "white"
  )
}
