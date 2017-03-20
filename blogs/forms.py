"""Blogs forms."""

from django import forms

from blogs.models import Post

EMPTY_POST_TITLE_ERROR = "You can't have an empty post title"
DUPLICATE_POST_TITLE_ERROR = 'A post with same title already exists.'


class PostForm(forms.models.ModelForm):
    """Post form."""

    class Meta:
        """Meta."""

        model = Post
        fields = ('title','summary','imagen','description','published_date')
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a post title',
                'class': 'post-title',
            }),
        }
        error_messages = {
            'title': {'required': EMPTY_POST_TITLE_ERROR, 'unique': DUPLICATE_POST_TITLE_ERROR}
        }


class NewPostForm(PostForm):
    """New post form."""

    def save(self, owner):
        """Save."""
        if owner.is_authenticated:
            return Post.objects.create(title=self.cleaned_data['title'], owner=owner)
