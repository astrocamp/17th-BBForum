# Generated by Django 5.1.1 on 2024-09-09 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofiles", "0003_alter_profile_education_alter_profile_gender_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="location",
            field=models.CharField(
                choices=[
                    ("TPE", "台北市"),
                    ("NTPC", "新北市"),
                    ("TPE", "台中市"),
                    ("TN", "台南市"),
                    ("KH", "高雄市"),
                    ("KHH", "基隆市"),
                    ("TYC", "桃園市"),
                    ("HCC", "新竹市"),
                    ("HSC", "新竹縣"),
                    ("MIA", "苗栗縣"),
                    ("CHW", "彰化縣"),
                    ("NTO", "南投縣"),
                    ("YUN", "雲林縣"),
                    ("CYI", "嘉義市"),
                    ("CYC", "嘉義縣"),
                    ("TNN", "台南縣"),
                    ("KHH", "高雄縣"),
                    ("PIF", "屏東縣"),
                    ("ILA", "宜蘭縣"),
                    ("HUN", "花蓮縣"),
                    ("TTT", "台東縣"),
                    ("PEN", "澎湖縣"),
                    ("KMN", "金門縣"),
                    ("MZC", "馬祖縣"),
                ],
                default="TP",
                max_length=100,
            ),
        ),
    ]
