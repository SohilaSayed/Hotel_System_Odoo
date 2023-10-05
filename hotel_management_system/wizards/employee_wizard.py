from odoo import fields, models


class EmployeeWizard(models.TransientModel):
    _name = 'employee.report'

    reservation_from = fields.Date("Reservation Date From", required=True)
    reservation_to = fields.Date("Reservation Date To", required=True)
    employee = fields.Many2one('hr.employee', string="Employee")

    def print_report(self):
        data = {"reservation_from": self.reservation_from, "reservation_to": self.reservation_to, "employee": self.employee.id}
        return self.env.ref("hotel_management_system.report_employee").report_action(self, data)


class CustomReport(models.AbstractModel):
    _name = "report.hotel_management_system.employee_template"

    def _get_report_values(self, docids, data=None):
        cr = self._cr

        if data["employee"]:
            employee_cond = f"and r.employee_name = {data['employee']}"
        else:
            employee_cond = " "
        query = f"""
                    SELECT        
                        hr_employee.name AS employee_name,
                        COUNT(CASE WHEN r.state = 'draft' THEN 1 ELSE NULL END) AS draft_count,
                        COUNT(CASE WHEN r.state = 'confirmed' THEN 1 ELSE NULL END) AS confirmed_count,
                        COUNT(CASE WHEN r.state = 'cancel' THEN 1 ELSE NULL END) AS cancelled_count
                    FROM 
                        hotel_reservation r
                    JOIN 
                        hr_employee  ON r.employee_name = hr_employee.id
                    WHERE 
                        (r.reservation_date BETWEEN '{data['reservation_from']}' AND '{data['reservation_to']}')
                        {employee_cond}
                    GROUP BY  hr_employee.name
        
        """
        cr.execute(query)
        values = cr.fetchall()

        return {
            "doc_ids": docids,
            "doc_model": "employee.report",
            "values": values,
            "data": data,
        }
