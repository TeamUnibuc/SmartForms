# Structure of the Backend

## Intro

The backend service's purpose is to:

 * Generate on-demand PDF form previews.
 * Generate and save on the database finalized PDF forms.
 * Add answers for a given form.
 * Retrieve from the database forms / answers given an ID.
 * Extrapolate (we call it infer) data from a given form.

Note that for infering and uploading the data from a pdf scan, the frontend has to:

 * Upload the scan to the backend, to extrapolate the data from the form.
 * Submit the data again, as an answer.

This might seem redundent, but the OCR is not 100% accurate, so we want to offer the user the posibility to change the extrapolation results.

## Structure

The backend is devided in multiple `Python` modules, each within its own folder.
The modules are:

 * [`database`](./backend-database.md), which connects the backend to `Mongo Cloud`.
 * [`ocr`](./backend-ocr.md), which implements a `Pytorch` neural network for performing optical character recognition.
 * [`pdf_processor`](./backend-pdf-processor.md), generating and extracting single characters from a form.
 * [`routers`](./backend-fast-api.md), implementing the actual HTTP REST API.
 * [`smart_forms_types`](./backend-smart-forms-types.md), the datatypes used within the project or exposed via our API.

## Testing

TBD