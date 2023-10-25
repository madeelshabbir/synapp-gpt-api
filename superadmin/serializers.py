from rest_framework import serializers
from .models import PDFFile, Parameter, Subcriber, Statistic, Userchat

from account.models import User

class UserAllProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'occupation', 'specialty']



# class PdfSerializer(serializers.ModelSerializer):
#     file = serializers.ListField(child=serializers.FileField())

#     class Meta:
#         model = PDFFile
#         fields = '__all__'

#     def create(self, validated_data):
#         files_data = validated_data.pop('file')
     

#         for file_data in files_data:
#             pdf=PDFFile.objects.create(file=file_data)

#             return pdf
class PdfSerializer(serializers.ModelSerializer):
    file = serializers.ListField(child=serializers.FileField())

    class Meta:
        model = PDFFile
        fields = '__all__'

    def create(self, validated_data):
        files_data = validated_data.pop('file')
        pdf_files = []

        for file_data in files_data:
            pdf_file = PDFFile.objects.create(file=file_data)
            pdf_files.append(pdf_file)

        return pdf_files

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'
class SubcriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcriber
        fields = '__all__'
class StaticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = '__all__'
class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userchat
        fields = '__all__'
class NewPdfSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    def get_file_name(self, obj):
        filename = obj.file.name
        file = filename.split("/")[1].lower()
        return file

    class Meta:
        model = PDFFile
        fields = ['id','file', 'status', 'file_name']
        