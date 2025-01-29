// Copyright (c) 2024, Smart and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Detailed Vat Report"] = {
	"filters": [ 

		,
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			  reqd: 1,
			default: frappe.sys_defaults.year_start_date,
		  },
		  {
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			  reqd: 1,
			default: frappe.sys_defaults.year_end_date,
		  },
	   {
		 fieldname: "transactions",
		 label: __("Transactions"),
		 fieldtype: "Select",
		 options:["Sales","Purchases"],
		   reqd: 1,
	   },
	 ]
};
