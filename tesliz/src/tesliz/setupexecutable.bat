echo "you need 7zip and upx" for the runthis.bat"
echo "you also need msvcr71 and msvpr71"
set pythonogre="c:\pythonogre"
set exeplace="runthis_exe"
move %pythonogre%\packages_2.5\ogre\renderer\OGRE\* .
move %pythonogre%\packages_2.5\gui\cegui\OGRE\* .

call runthis
move %pythonogre%\plugins %exeplace%\plugins
move %pythonogre%\media %exeplace%\plugins
move %pythonogre%\demos\media\packs %exeplace%\resources
move %pythonogre%\packages_2.5\ogre\renderer\OGRE\* %exeplace%
move %pythonogre%\packages_2.5\gui\cegui\OGRE\* %exeplace%
move scenes\* %exeplace%\scenes