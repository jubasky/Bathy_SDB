# script para compilar forms qt tipo *.ui par *.py

from PyQt4 import uic

# fin = open('FormNewDatabase.ui','r')
# fout = open('FormNewDatabase.py','w')

# fin = open('FormEdit.ui','r')
# fout = open('FormEdit.py','w')

# fin = open('FormImportFile.ui','r')
# fout = open('FormImportFile.py','w')
#
# fin = open('FormConfig.ui','r')
# fout = open('FormConfig.py','w')
#
# fin = open('formPesquisa.ui','r')
# fout = open('FormPesquisa.py','w')
#
# fin = open('main_window.ui','r')
# fout = open('main_window.py','w')

fin = open('FormExportMetadata.ui','r')
fout = open('FormExportMetadata.py','w')

# fin = open('formCorrigirMetadata.ui','r')
# fout = open('formCorrigirMetadata.py','w')

# fin = open('formExtrairXYZ.ui','r')
# fout = open('formExtrairXYZ.py','w')

uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()