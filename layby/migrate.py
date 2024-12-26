import frappe

from frappe import get_doc

from frappe.custom.doctype.custom_field.custom_field import create_custom_field as add_custom_field


def before_migrate():
    "Removes the virtual field allow_layby from the Customer doctype"
    from frappe.model import delete_docfield
    delete_docfield("Customer", "allow_layby")


def after_migrate():
    "Udates exsiting customers to add the allow_layby field value"
    

    #Add the allow_layby field to the Customer doctype
    add_custom_field("Customer", {
        "fieldname": "allow_layby",
        "label": "Allow Layby",
        "fieldtype": "Check",
        "insert_after": "customer_primary_contact"
    })
    # set value of allow_layby field to True for customers with valid id numbers and contact numbers
  
    customers = frappe.db.sql("select name from tabCustomer", as_dict=True)
    for customer in customers:
        customer_doc=get_doc("Customer",customer)
        valid_id=customer_doc.id_number or (customer_doc.passport_number and customer_doc.passport_country)
        has_mobile=customer_doc.customer_primary_contact != None and customer_doc.customer_primary_contact.strip() != ""

        if valid_id and has_mobile:
            frappe.db.set_value("Customer",customer,"allow_layby",True)
        else:
            frappe.db.set_value("Customer",customer,"allow_layby",False)
            
    frappe.db.commit()
            


   