from email.utils import format_datetime
from rest_framework import serializers
from inventoryApp.models.report import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'item', 'dateTime', 'status', 'observation', 'employee']    

    def to_representation(self, obj):
        report = Report.objects.get(id=obj.id)
        return {
            'id': report.id,
            'item_id': report.item.id,
            'item_name': report.item.name,
            'dateTime': format_datetime(report.dateTime, '%Y-%m-%d %H:%M'),
            'date': report.dateTime.date().strftime('%d-%m-%Y'),
            'time': report.dateTime.time().strftime('%H:%M'),
            'status': report.status,
            'observation': report.observation,
            'employee': report.employee
        }
