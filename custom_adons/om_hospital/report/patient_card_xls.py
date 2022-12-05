# -*- coding: utf-8 -*-

from odoo import models
import base64
import io


class PatientCardXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_id_card_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        sheet = workbook.add_worksheet('Patient ID Card')
        bold = workbook.add_format({'bold': True})
        format1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})

        row = 3
        col = 3
        sheet.set_column('D:D', 12)
        sheet.set_column('E:E', 13)
        for obj in patients:
            row += 1
            sheet.merge_range(row, col, row, col + 1, 'ID Card', format1)

            row += 1
            if obj.image:
                patient_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row, col, "image.png", {'image_data': patient_image, 'x_scale': 0.2, 'y_scale': 0.2})

                row += 6

            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col + 1, obj.name)
            row += 1
            sheet.write(row, col, 'Age', bold)
            sheet.write(row, col + 1, obj.age)
            row += 1
            sheet.write(row, col, 'Reference', bold)
            sheet.write(row, col + 1, obj.ref)

            row += 2
            sheet.merge_range(row, col, row + 1, col + 1, '', format1)

