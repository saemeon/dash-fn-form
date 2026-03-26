# Copyright (c) Simon Niederberger.
# Distributed under the terms of the MIT License.

MM_TO_INCH <- 1 / 25.4

#' Named figure sizes for corporate layouts
#'
#' A named list of \code{c(width, height)} vectors in inches, matching the
#' layout options on the gallery portal. Use with \code{corporate_frame()}
#' or \code{ggsave()}.
#'
#' @format Named list. Each element is a numeric vector \code{c(width, height)}
#'   in inches.
#'
#' @examples
#' \dontrun{
#' library(ggplot2)
#'
#' # Use with corporate_frame:
#' ggplot(mtcars, aes(wt, mpg)) + geom_point() +
#'   corporate_frame(figsize = "publication_half")
#'
#' # Use with ggsave:
#' sz <- figsizes$publication_full
#' ggsave("chart.png", p, width = sz[1], height = sz[2])
#'
#' # List all available sizes:
#' names(figsizes)
#' }
#' @export
figsizes <- list(
  publication_half       = c(88.0  * MM_TO_INCH, 76.0  * MM_TO_INCH),
  publication_twothirds  = c(119.0 * MM_TO_INCH, 76.0  * MM_TO_INCH),
  publication_full       = c(181.0 * MM_TO_INCH, 76.0  * MM_TO_INCH),
  publication_full_high  = c(181.0 * MM_TO_INCH, 152.0 * MM_TO_INCH),
  presentation_43_half       = c(108.0 * MM_TO_INCH, 130.5 * MM_TO_INCH),
  presentation_43_twothirds  = c(144.0 * MM_TO_INCH, 130.5 * MM_TO_INCH),
  presentation_43_full       = c(228.0 * MM_TO_INCH, 130.5 * MM_TO_INCH),
  presentation_169_onethird  = c(96.8  * MM_TO_INCH, 130.5 * MM_TO_INCH),
  presentation_169_half      = c(151.4 * MM_TO_INCH, 130.5 * MM_TO_INCH),
  presentation_169_twothirds = c(206.0 * MM_TO_INCH, 130.5 * MM_TO_INCH),
  presentation_169_full      = c(314.8 * MM_TO_INCH, 130.5 * MM_TO_INCH),
  word_half         = c(74.0  * MM_TO_INCH, 63.9 * MM_TO_INCH),
  word_full         = c(160.0 * MM_TO_INCH, 67.2 * MM_TO_INCH),
  word_scaled_half  = c(74.0  * MM_TO_INCH, 63.9 * MM_TO_INCH),
  word_scaled_full  = c(160.0 * MM_TO_INCH, 67.2 * MM_TO_INCH),
  mobile_full       = c(48.0  * MM_TO_INCH, 43.5 * MM_TO_INCH),
  report_half       = c(88.0  * MM_TO_INCH, 42.0 * MM_TO_INCH)
)
