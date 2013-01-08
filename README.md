classsite
=========

Jan 7 Changes

kalendar_list.html
    Changed permission for links to add event to .is_staff
    Changed permission for links to change day number to .is_superuser

homework models.py
    HomeworkModelForm
    Commented out clean_class_db
    Changed clean function to allow teachers to add homework to all classes
    
messages views.py
    order_by('-last_msg')
    
registration views.py
    added .replace to first and last name to get rid of white space
    still may be problems with other characters

contact 
    forms.py
    changed teachermodelchoicefield to include all teachers and their last name
    views.py
    changed teacher to use user to get the email address of the teacher

404.html
    added one to see if that solves django errors on live site