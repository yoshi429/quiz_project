from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import ContactUs, Profile


User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    ユーザー登録機能
    """
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='確認用パスワード', widget=forms.PasswordInput)
    is_understand = forms.BooleanField(label='利用規約に同意する',  widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=False):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        user.save()
        return user
    
    def clean_username(self):
        """
        ユーザーネームが存在しているかどうか
        """
        username = self.cleaned_data['username']
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise ValidationError('このユーザー名はすでに使われています。')
        return username
    
    def clean_email(self):
        """
        メールのチェック
        """
        email = self.cleaned_data['email']
        qs = User.objects.filter(username__iexact=email)
        if qs.exists():
            raise ValidationError('このメールアドレスはすでに使われています。')
        return email

    def clean_password(self):
        """
        パスワードの文字数と単純かどうかチェック
        """
        password = self.cleaned_data['password']
        if len(password) <= 7:
            raise ValidationError('8字以上のパスワードを入力して下さい')
        validate_password(password)
        return password
    
    def clean_is_understand(self):
        """
        利用規約に同意しているかどうか
        """
        is_understand = self.cleaned_data['is_understand']
        if not is_understand:
            raise ValidationError('利用規約に同意してください。')
        return is_understand

    def clean(self):
        """
        パスワードと確認用パスワードのチェック
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        print(password, confirm_password)
        if password != confirm_password:
            print('パスワードと確認用パスワードが一致しません！')
            raise ValidationError('パスワードと確認用パスワードが一致しません！')
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    """
    ログインフォーム
    """
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)


class ContactUsForm(forms.ModelForm):
    """
    お問い合わせフォーム
    """
    author = forms.CharField(label='氏名')
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='件名')
    description = forms.CharField(label='内容', widget=forms.Textarea)

    class Meta:
        model = ContactUs
        fields = ('author', 'email', 'title', 'description')


class EditProfileForm(forms.Form):
    """
    プロフィールの編集フォーム
    """
    profile_picture = forms.FileField(label='トプ画', required=False)
    introduce = forms.CharField(label='紹介文', required=False)

    def clean_introduce(self):
        """
        文字数制限
        """
        introduce = self.cleaned_data['introduce']
        if len(introduce) > 255:
            raise ValidationError("255字以内です。")
        return introduce