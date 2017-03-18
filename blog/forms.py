"""Django blog forms."""
from django import forms

from blog.models import Post, Blog

EMPTY_POST_TITLE_ERROR = "You can't have an empty post title"


class PostForm(forms.models.ModelForm):
    """Post form."""

    class Meta:
        """Meta."""

        model = Post
        fields = ('title',)
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a post title',
                'class': 'post-title',
            }),
        }
        error_messages = {
            'title': {'required': EMPTY_POST_TITLE_ERROR}
        }


class NewBlogForm(PostForm):
    """New blog form."""

    def save(self, owner):
        """Save."""
        if owner.is_authenticated:
            return Blog.create_new(first_post_title=self.cleaned_data['title'], owner=owner)
        else:
            return Blog.create_new(first_post_title=self.cleaned_data['title'])
