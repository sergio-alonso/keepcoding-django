"""Django blog forms."""
from django import forms

from blog.models import Post

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

    def save(self, for_blog):
        """Save."""
        self.instance.blog = for_blog
        return super().save()
