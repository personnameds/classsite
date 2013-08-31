classsite v5

To Do:
    -make sure everything looks good
    -resetup everything on server
    -add all classes and teachers
    -teacher names instead of their username etc
    -fail silently off emails before going live

Admin
    -update all admin.py

Initialize
    -need to automate day creation based on schedule format, right now hardcoded
    -need to autmoate classes and teacher creation, right now hardcoded
    -everything is too hardcoded in
    -should break up into parts from an admin only webpage
    -admin only webpage should display class and teacher info
    -if fail security login redirect not setup

Day_No
    -nothing upgraded same as classsite4

Kalendar
    -creation of kalendar same as old nothing upgraded
    -need to add permissions to Kalendar_list
    -I cleaned up Kalendar_List a little
    -events needs cleaning up

Links

Schedule
    -update schedule needs to look nicer for teachers
    -add_day_no form needs revising
    -any teacher can change and teachers schedule

Messages
    -edit messages????
    -if 0 messages topic should delete

Documents
    -different directories for each class

Contact

Homework
    -check if actually in class adding homework too
    -multiple class homework

Classlists
    -resize banner images when uploaded (saved link in readitlater)
    -Student Model turned off... do I need it?

Homepage
    -can I make homepage updateview cleaner, is it a hack or is it good?
    -homepage templates form and modify still old style not updated yet

Login
    -do I need to include path in context everytime to make ?next work
    
Registration
    -works but needs to be revised, focus on redirect stuff
    -I really doubt I need the path context thing
    
Other
    -memcached
    -No hard coded urls (reverse lazy etc.)
    -Get_absolute_url
        -need to use and add so I can click from admin to see on website

    