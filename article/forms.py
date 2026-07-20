from django import forms
from article.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '請輸入文章標題...',
                'required': True,
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '網址簡稱 (選填，若留空將自動生成)',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'id': 'markdown-editor',
                'placeholder': '使用 Markdown 編寫文章內容...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 移除隱藏 textarea 的 HTML5 required 屬性，避免 EasyMDE 隱藏元素後引發瀏覽器焦點錯誤
        if 'content' in self.fields:
            self.fields['content'].widget.attrs.pop('required', None)
