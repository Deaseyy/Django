from django import forms
from django.forms import ValidationError

from user.models import Profile


class ProfileForm(forms.ModelForm):

    def clean_max_distance(self):  # 单独额外校验某个字段(字段格式通过验证后自动调用)，函数名固定格式，clean_字段名
        # 校验某字段,只能获取到
        cleaned_data = self.clean()  # clean() 返回cleaned_data 为校验ok过后的所有字段{}
        min_distance = cleaned_data.get('min_distance')
        max_distance = cleaned_data.get('max_distance')
        if min_distance > max_distance:
            raise ValidationError('min distance > max distance')
        return max_distance


    def clean_max_dating_age(self):
        clean_data = self.clean()
        min_dating_age = clean_data.get('min_dating_age')
        max_dating_age = clean_data.get('max_dating_age')

        if min_dating_age > max_dating_age:
            raise ValidationError('min dating age > max dating age')
        return max_dating_age


    class Meta:
        model = Profile
        fields = '__all__'
