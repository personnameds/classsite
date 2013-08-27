classsite v5

To Do:
    -teacher names instead of their username etc
    -security!

Admin
    -update all admin.py

Initialize
    -need to automate day creation based on schedule format, right now hardcoded
    -need to autmoate classes and teacher creation, right now hardcoded


Day_No
    -nothing upgraded same as classsite4

Kalendar
    -creation of kalendar same as old nothing upgraded
    -need to add permissions to Kalendar_list
    -I cleaned up Kalendar_List a little
    -events needs cleaning up

Links
    -original

Schedule
    -original
    -permissions
    -Add_Day_No Stuff needs revising?????

Messages
    -original
    -edit messages????
    -if 0 messages topic should delete

Documents
    -works same as original
    -different directories for each class

Contact
    -works same as original

Homework
    -security
    -multiple class homework
    -original nothing updated

Classlists
    -resize banner images when uploaded (saved link in readitlater)
    -Student admin page only shows username not first and last
        doable but not easy with admin I have now
        I can switch back to regular admin page and then it will use unicode from model
    -Don't have teachers setup

Homepage
    -add security
    -can I make homepage updateview cleaner, is it a hack or is it good?
    -homepage templates form and modify still old style not updated yet

Login
    -do I need to include path in context everytime to make ?next work
    
Registration
    -Fail Silently needs to be turned off for production version
    
Other
    -No hard coded urls (reverse lazy etc.)
    -Get_absolute_url
        -need to use and add so I can click from admin to see on website
    -need to get rid of @reciever for user when syncdb???
    