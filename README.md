# Update-Catalog-Info
The purpose of this project is to automatically update the information catalog with data provided by suppliers. After the catalog is updated, the suppliers should be notified with an email that indicates which fruits were uploaded. The service should also have a mechanism to check the health of the system and send an email notification if something goes wrong.

## Project's Goals
The summary of the projects goals are as follows:
* Summarize and process product data into different categories
* Upload new products to online store
* Generate a PDF report based on data uploaded
* Automatically send that PDF by email to supplier of product uploaded
* Continuously monitor the health status of the system
* Send email alert if server is ever unhealthy

## Data Format
The data from the suppliers comes in two files: one for images of the products saved as '.TIF' and the other for descriptions of the product saved as '.txt'. The images need to be converted to smaller '.jpeg' images and product descriptions need to be converted to '.HTML' files that also shows the image. The images and descriptions should be uploaded separately, using different web endpoints.
