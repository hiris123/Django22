'''

venv/Scripts/activate.bat
python manage.py startapp blog ( blog라는 앱 생성)


```cpp
venv/Scripts/activate.bat
python manage.py startapp blog ( blog라는 앱 생성)
```
[settings.py]
'blog',

[admin.py]
from .models import Post

admin.site.register(Post)




'''