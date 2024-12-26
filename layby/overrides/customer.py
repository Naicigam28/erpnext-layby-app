import frappe
from frappe.model.document import Document
from erpnext.selling.doctype.customer.customer import Customer


class LaybyCustomer(Customer):

    def validate_id_number(self):

        if self.passport_number!=None and self.passport_number.strip()!="":
            frappe.throw("Only one of ID Number or Passport Number should be provided")
        

    def validate(self):
        super(LaybyCustomer, self).validate()
        self.validate_id_number()
        self.validate_passport_number()
    
    @property
    def allow_layby(self):
        #Checks if An ID number or passport number and passport country of origin is provided
        # And a primary mobile number is associated with the customer
        valid_id=self.id_number or (self.passport_number and self.passport_country)
        has_mobile=self.customer_primary_contact != None and self.customer_primary_contact.strip() != ""
        if valid_id and has_mobile:
            return True
        else:
            return False
        
        




