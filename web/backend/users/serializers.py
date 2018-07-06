from core.serializers import DynamicFieldsModelSerializer
from .models import Profile, UserComment


class ProfileSerializer(DynamicFieldsModelSerializer):

        class Meta:
            model = Profile
            fields = (
                "user",
                "name",
                "surname",
                "patronymic",
                "birth_date"
            )


class UserCommentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = UserComment
        fields = (
            "user",
            "text",
        )