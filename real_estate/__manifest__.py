{
    'name': 'Real Estate',
    'version': '18.0.0.1.0',
  
    'author': 'Abdel karim',
    
    'category': '',
    'depends': ['report_xlsx','base'],  
    'data': [
        'views/main_menu.xml',
      'views/type_view.xml',
      'views/tag_view.xml',
      'views/property_view.xml',
      'views/users_view.xml',
      'security/ir.model.access.csv',
        'report/report_property_template.xml',
        'report/report_estate_xlsx.xml',
       'report/report_property_action.xml',
       'views/estate_report_wizard_view.xml',
       
       
      
    ],
    
    'application': True,
    'installable': True
    
}
