from pypdf import PdfWriter, PdfReader
import io

from ..exceptions import UnsupportedFileTypeException


class PDF:
    allowed_content_type = ['application/pdf']

    @staticmethod
    def supported_file_type(data_list):
        for data in data_list:
            if data["ContentType"] not in PDF.allowed_content_type:
                raise UnsupportedFileTypeException(
                    f"File type not supported only: {str(PDF.allowed_content_type)} is allowed")

    @staticmethod
    def combine_files(data_list):
        # validate file type is supported
        PDF.supported_file_type(data_list)

        pdf_writer = PdfWriter()

        for data in data_list:
            # read each file into a stream
            object_bytes = io.BytesIO(data["ReadBodyStram"])
            object_read_pdf = PdfReader(object_bytes)

            pdf_writer.append_pages_from_reader(object_read_pdf)

        merged_pdf = io.BytesIO()
        pdf_writer.write(merged_pdf)
        merged_pdf.seek(0)

        return merged_pdf
