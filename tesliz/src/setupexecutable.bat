echo "you need 7zip and upx" for the runthis.bat"
echo "you also need msvcr71 and msvpr71"
set pythonogre=c:\pythonogre
set exeplace=runthis_exe

copy %pythonogre%\packages_2.5\ogre\renderer\OGRE\* .
copy %pythonogre%\packages_2.5\ogre\gui\cegui\* .

mkdir %exeplace%\plugins
copy %pythonogre%\plugins %exeplace%\plugins
mkdir %exeplace%\media
xcopy media %exeplace%\media /e
mkdir %exeplace%\resources
copy %pythonogre%\demos\media\packs %exeplace%\resources
copy %pythonogre%\packages_2.5\ogre\renderer\OGRE\* %exeplace%
copy %pythonogre%\packages_2.5\ogre\gui\cegui\* %exeplace%

pause