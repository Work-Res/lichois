import csv

from datetime import datetime

from django.http import HttpResponse
from django.views import View

from gazette.models import BatchApplication
from gazette.service import PrepareGazetteForDownload


class DownloadGazetteCSVView(View):

    def get(self, request, batch_id):
        # Generate the filename with the current date
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        csv_file_name = f"gazette-{formatted_date}.csv"

        # Prepare the response with CSV headers
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{csv_file_name}"'},
        )

        # Retrieve all batch applications related to the given batch_id
        batch_applications = BatchApplication.objects.filter(batch_id=batch_id)

        if not batch_applications.exists():
            return HttpResponse("No batch applications found.", status=404)

        # Prepare the data for download
        try:
            data = self.prepare_data(batch_applications)
        except Exception as e:
            # Log the error (add logging if necessary)
            return HttpResponse(f"Error preparing data: {e}", status=500)

        # Write data to CSV
        writer = csv.writer(response)
        for row in data:
            writer.writerow(row)

        return response

    def prepare_data(self, batch_applications):
        """
        Prepare the data for CSV download by using the PrepareGazetteForDownload class.
        This method helps in separating logic and improving readability.
        """
        prepare_download_data = PrepareGazetteForDownload(batch_applications=batch_applications)
        return prepare_download_data.prepared_data()
