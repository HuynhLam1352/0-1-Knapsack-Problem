# Convert resource file to py file
pyrcc5 ./UIDesign/Resource/resource.qrc -o ./UIDesign/Resource/resource_rc.py

# Convert ui file to py file
pyuic5 -x ./UIDesign/mainwindow.ui -o ./UIDesign/UI_mainwindow.py