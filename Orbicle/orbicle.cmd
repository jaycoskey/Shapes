SET BLENDER_SHARE=C:\Program Files\Blender Foundation\Blender
SET BLENDER_PATH="%BLENDER_SHARE%\blender.exe"

SET BLENDER_VERSION="2.82"

%BLENDER_PATH% --background --python blend.py -- -W error 
