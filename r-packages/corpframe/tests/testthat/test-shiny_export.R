# Tests for Shiny export functions

test_that("corporate_export_plotly is exported", {
  expect_true(is.function(corpframe::corporate_export_plotly))
})

test_that("corporate_export_gg is exported", {
  expect_true(is.function(corpframe::corporate_export_gg))
})

test_that("corporate_export_plotly errors without shiny", {
  # The function exists but requires shiny at runtime
  expect_true("session" %in% names(formals(corpframe::corporate_export_plotly)))
})

test_that("corporate_export_gg errors without shiny", {
  expect_true("session" %in% names(formals(corpframe::corporate_export_gg)))
})
