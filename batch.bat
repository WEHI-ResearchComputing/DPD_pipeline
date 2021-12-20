:url
set /P u=ENA code of the data?

IF "%u%"=="" ECHO ENA not defined

IF "%u%"!="" ECHO %u% defined

ECHO batch finished