from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Comment, CustomUser, ContactModel
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    age = forms.IntegerField(max_value=100)

    class Meta:
        model = CustomUser

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.age = self.cleaned_data['age']
        user.save()

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'required': False, 'cols': 50, 'rows': 20}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'keywords', 'overview', 'content', 'thumbnail', 
        'categories', 'featured', 'previous_post', 'next_post')


class CommentForm(forms.ModelForm):

    """content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4',
        'name': 'usercomment',
    }))"""
    class Meta:
        model = Comment
        fields = ('content', 'email', 'name' )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control",
                'placeholder': 'Please enter your name',
                'id': 'usercomment',
                'rows': '4',
                'name': 'usercomment'}),
            "email": forms.EmailInput(attrs={"class": "form-control",
                'placeholder': 'Please enter your email',
                'id': 'usercomment',
                'rows': '4',
                'name': 'usercomment'}),
            "content": forms.Textarea(attrs={'class': 'form-control',
                'placeholder': 'Please enter your comment',
                'id': 'usercomment',
                'rows': '4',
                'name': 'usercomment',})
            }


class ContactForm(forms.Form):
    email = forms.EmailField(widget = forms.EmailInput(attrs={"class": "form-control border",
                'placeholder': 'Your email',}), required=False)
    subject = forms.CharField(widget= forms.TextInput(attrs={"class": "form-control border",
                'placeholder': 'Subject of your message',}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                'placeholder': 'Your message',
                'id': 'usercomment',
                'rows': '4',
                'name': 'usercomment',}), required=True)

    class Meta:
        model = ContactModel
        fields = '__all__'

        """widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "message": forms.Textarea(attrs={"class": "form-control border"})
        }"""

        """widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control border",
                'placeholder': 'Subject of your message',}),
            "email": forms.EmailInput(attrs={"class": "form-control border",
                'placeholder': 'Your email'}),
            "message": forms.Textarea(attrs={'class': 'form-control',
                'placeholder': 'Your message',
                'id': 'contact_message',
                'rows': '4',
                'name': 'contact_message',})
            }"""


class TestCommentForm(forms.ModelForm):

    """content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4',
        'name': 'usercomment',
    }))"""
    class Meta:
        model = Comment
        fields = ('content', 'email', 'name' )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border",
                'placeholder': 'Please enter your name',
                'id': 'usercomment',
                'rows': '4',
                'name': 'usercomment'}),
            "email": forms.EmailInput(attrs={"class": "form-control border",
                'placeholder': 'Please enter your email',
                'id': 'usercomment',
                'rows': '4',
                'name': 'usercomment'}),
            "content": forms.Textarea(attrs={'class': 'form-control',
                'placeholder': 'Please enter your comment',
                'id': 'usercomment',
                'rows': '4',
                'name': 'usercomment',})
            }
