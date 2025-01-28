# Copyright (c) 2024, Smart and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns,data

def get_columns(filters):
    if filters.get("transactions") == "Sales":

    
        columns = [
             {
                "fieldname": "date",
                "label": _("Invoice Date"),
                "fieldtype": "Date",
                "width": 250,
            },
            {
                "fieldname": "invoice",
                "label": _("Invoice"),
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": 250,
            },
   
              {
                "fieldname": "customer",
                "label": _("Customer"),
                "fieldtype": "Link",
                "options": "Customer",
                "width": 180,
            },
             {
                "fieldname": "tax_id",
                "label": _("Tax Id"),
                "fieldtype": "Data",
                "width": 180,
            },
            {
                "fieldname": "amount",
                "label": _("Amount"),
                "fieldtype": "Currency",
                "width": 180,
            },
            {
                "fieldname": "tax_amount",
                "label": _("Tax Amount"),
                "fieldtype": "Currency",
                "width": 180,
            },
            {
                "fieldname": "grand_total",
                "label": _("Grand Total"),
                "fieldtype": "Currency",
                "width": 180,
            }
        ]
    else:
        columns = [
            {
                "fieldname": "invoice_date",
                "label": _("Invoice Date"),
                "fieldtype": "Data",
                "width": 180,
            },
            {
                "fieldname": "voucher_type",
                "label": _("Voucher Type"),
                "fieldtype": "Link",
                "options": "Doctype",
                "width": 250,
            },
            {
                "fieldname": "voucher_no",
                "label": _("Voucher No"),
                "fieldtype": "Dynamic Link",
                "options": "voucher_type",
                "width": 250,
            },




              {
                "fieldname": "supplier",
                "label": _("Supplier"),
                "fieldtype": "Link",
                "options": "Supplier",
                "width": 180,
            },
            {

                "fieldname": "bill_no",
                "label": _("Supplier Invoice Number"),
                "fieldtype": "Data",
                "width": 180,

            },
             {
                "fieldname": "tax_id",
                "label": _("Tax Id"),
                "fieldtype": "Data",
                "width": 180,
            },
              {
                "fieldname": "purchase_amount",
                "label": _("Purchase Amount"),
                "fieldtype": "Currency",
                "width": 180,
            },
              {
                "fieldname": "purchase_tax_amount",
                "label": _("Purchase Tax Amount"),
                "fieldtype": "Currency",
                "width": 180,
            },
             {
                "fieldname": "purchase_grand_total",
                "label": _("Purchase Grand Total"),
                "fieldtype": "Currency",
                "width": 180,
            },
          

           
              {
                "fieldname": "qty",
                "label": _("Expense Qty"),
                "fieldtype": "Data",
                "width": 180,
            },
             {
                "fieldname": "expense_type",
                "label": _("Expense Type"),
                "fieldtype": "Data",
                "width": 180,
            },
          
        
            {
                "fieldname": "custom_invoice_number",
                "label": _("Expense Invoice Number"),
                "fieldtype": "Data",
                "width": 180,
            },
             {
                "fieldname": "gl_entry",
                "label": _("GL Entry"),
                "fieldtype": "Link",
                "options": "GL Entry",
                "width": 250,
            },
         
            {
                "fieldname": "debit_amount",
                "label": _("Debit Amount"),
                "fieldtype": "Currency",
                "width": 180,
            },
             {
                "fieldname": "credit_amount",
                "label": _("Credit Amount"),
                "fieldtype": "Currency",
                "width": 180,
            },
             {
                "fieldname": "balance",
                "label": _("Balance"),
                "fieldtype": "Currency",
                "width": 180,
            },
                  {
                "fieldname": "total_tax_amount",
                "label": _("Total Tax Amount"),
                "fieldtype": "Currency",
                "width": 180,
            },
        ]

    return columns



def get_data(filters):
    data = []
    to_date = filters.get("to_date")
    from_date = filters.get("from_date")
    branch = filters.get("branch")

    for title, account_name in [("٪ المبيعات الخاضعة للضريبة ١٥","210401 - VAT 15% - BC"),
                                ("٪ المبيعات الخاضعة للضريبة ٥", "VAT 5% - BC")]:
        if filters.get("transactions") == "Sales":
        
            if branch:
                data = frappe.db.sql("""
                    SELECT stc.tax_amount, si.name AS invoice,si.posting_date AS date, si.customer,si.tax_id,si.grand_total, (si.grand_total - stc.tax_amount) AS amount
                    FROM `tabSales Taxes and Charges` AS stc
                    INNER JOIN `tabSales Invoice` AS si ON stc.parent = si.name
                    WHERE stc.parenttype = 'Sales Invoice'
                    AND stc.docstatus = 1
                    AND stc.account_head = %s
                    AND si.branch = %s
                    AND posting_date BETWEEN %s AND %s
                """, (account_name, branch, from_date, to_date), as_dict=True)
            else:
                data = frappe.db.sql("""
                    SELECT stc.tax_amount, si.name AS invoice, si.posting_date AS date,si.customer,si.tax_id, si.grand_total, (si.grand_total - stc.tax_amount) AS amount
                    FROM `tabSales Taxes and Charges` AS stc
                    INNER JOIN `tabSales Invoice` AS si ON stc.parent = si.name
                    WHERE stc.parenttype = 'Sales Invoice'
                    AND stc.docstatus = 1
                    AND stc.account_head = %s
                    AND posting_date BETWEEN %s AND %s
                """, (account_name, from_date, to_date), as_dict=True)


        
        else:
            if branch:
                purchase  = frappe.db.sql("""
                        SELECT 
                            stc.tax_amount AS purchase_tax_amount,si.posting_date AS invoice_date,si.supplier,si.tax_id, si.name AS voucher_no,stc.parenttype AS  voucher_type,si.grand_total AS purchase_grand_total ,( si.grand_total - stc.tax_amount) AS purchase_amount,pii.item_code AS expense_type, si.bill_no
                        FROM 
                            `tabPurchase Taxes and Charges` AS stc
                            INNER JOIN `tabPurchase Invoice` AS si ON stc.parent = si.name
                            INNER JOIN `tabPurchase Invoice Item` AS pii ON si.name = pii.parent
                        WHERE 
                            stc.parenttype = 'Purchase Invoice'
                            AND stc.docstatus = 1
                            AND stc.account_head = '{account_name}'
                            AND si.branch = '{branch}'              
                            AND si.posting_date BETWEEN '{from_date}' AND '{to_date}'
                            AND pii.idx = 1
                                    
                        """.format(account_name=account_name,branch=branch ,from_date=from_date, to_date=to_date), as_dict=True)
            else:
                purchase  = frappe.db.sql("""
                        SELECT 
                            stc.tax_amount AS purchase_tax_amount, si.supplier,si.posting_date AS invoice_date, si.tax_id, si.name AS voucher_no,stc.parenttype AS  voucher_type ,si.grand_total AS purchase_grand_total ,( si.grand_total - stc.tax_amount) AS purchase_amount,pii.item_code AS expense_type, si.bill_no
                        FROM 
                            `tabPurchase Taxes and Charges` AS stc
                            INNER JOIN `tabPurchase Invoice` AS si ON stc.parent = si.name
                                          INNER JOIN `tabPurchase Invoice Item` AS pii ON si.name = pii.parent
                        WHERE 
                            stc.parenttype = 'Purchase Invoice'
                            AND stc.docstatus = 1
                            AND stc.account_head = '{account_name}'                                                
                            AND si.posting_date BETWEEN '{from_date}' AND '{to_date}'
                                          AND pii.idx = 1
                                    
                        """.format(account_name=account_name ,from_date=from_date, to_date=to_date), as_dict=True)
                
            
            if branch:
            
                gl = frappe.db.sql("""
                            SELECT 
                                gl.name AS gl_entry, 
                                   
                                gl.voucher_no AS voucher_no, 
                                gl.voucher_type AS voucher_type,
                                   
                                gl.debit AS debit_amount,
                                gl.credit AS credit_amount,
                                   (gl.debit - gl.credit) AS balance
                            FROM 
                                `tabGL Entry` AS gl
                            JOIN
                                `tabJournal Entry` AS je ON gl.voucher_no = je.name
                            WHERE 
                                
                                gl.is_cancelled = 0 
                                AND gl.account = '{account_name}'
                                AND gl.voucher_type = 'Journal Entry'
                                AND je.custom_branch = '{branch}'  
                                AND gl.posting_date BETWEEN '{from_date}' AND '{to_date}'
                        """.format(account_name=account_name, branch=branch, from_date=from_date, to_date=to_date), as_dict=True)
            else:
                gl = frappe.db.sql("""
                            SELECT 
                                gl.name AS gl_entry, 
                                gl.voucher_no AS voucher_no, 
                                gl.voucher_type AS voucher_type,
                                gl.debit AS debit_amount,
                                gl.credit AS credit_amount,
                                   (gl.debit - gl.credit) AS balance
                            FROM 
                                `tabGL Entry` AS gl
                            WHERE 
                               
                                gl.is_cancelled = 0 
                                   
                                AND gl.account = '{account_name}'
                                AND gl.voucher_type = 'Journal Entry'
                                AND gl.posting_date BETWEEN '{from_date}' AND '{to_date}'
                        """.format(account_name=account_name,  from_date=from_date, to_date=to_date), as_dict=True)
                
            
            data = purchase  + gl
            for item in data:
                item["total_tax_amount"] = item.get("purchase_grand_total" , 0) + item.get("balance", 0)
       


        return data
       
     
   
