echo "you need 7zip and upx" for the runthis.bat"
echo "you also need msvcr71 and msvpr71"
set pythonogre=c:\pythonogre
set exeplace=runthis_exe
copy %pythonogre%\packages_2.5\ogre\renderer\OGRE\* .
copy %pythonogre%\packages_2.5\gui\cegui\OGRE\* .

copy %pythonogre%\plugins %exeplace%\plugins
copy %pythonogre%\media %exeplace%\plugins
copy %pythonogre%\demos\media\packs %exeplace%\resources
copy %pythonogre%\packages_2.5\ogre\renderer\OGRE\* %exeplace%
copy %pythonogre%\packages_2.5\ogre\gui\cegui\* %exeplace%

pause