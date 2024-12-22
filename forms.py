from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write something...',
                'rows': 3,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a comment...',
                'rows': 2,
            }),
        }



from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write something...',
                'rows': 3,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')

        if not content and not image:
            raise forms.ValidationError("You must provide either text or an image.")
        
        return cleaned_data


# forms.py
# from django import forms
# from .models import Group

# class GroupForm(forms.ModelForm):
#     class Meta:
#         model = Group
#         fields = ['name', 'description']
