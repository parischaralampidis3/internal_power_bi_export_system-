from django.db import models

# Create your models here.
class Report(models.Model):
    report_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    iframe_url = models.TextField(max_length=400)
    pages = models.JSONField(default=list)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Filter(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='filters')
    filter_label = models.CharField(max_length=100)
    column_name = models.CharField(max_length=100)
    allowed_values = models.JSONField(default=list,blank=True)
    default_values = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.filter_label.title}: {self.report.title}"
    

class Pages(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='page_objects')
    page_name = models.CharField(max_length=100)
    page_id = models.CharField(max_length=100)
    powerbi_page_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    order = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.page_name 