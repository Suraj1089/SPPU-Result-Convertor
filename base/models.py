from django.db import models
import os

class HomePageData(models.Model):
    """Model definition for HomePageData."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for HomePageData."""

        verbose_name = 'HomePageData'
        verbose_name_plural = 'HomePageDatas'

   
    title = models.CharField(max_length=50, default='Result Analyser')
    titleLine = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='img/logo', blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    
   
    def __str__(self):
        """Unicode representation of HomePageData."""
        
        return self.title


class MenuItem(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    link = models.CharField(max_length=100,blank=True,null=True)
    homePageData = models.ForeignKey('HomePageData', on_delete=models.CASCADE, blank=True, null=True)



class UploadFile(models.Model):
    """Model definition for UploadFile."""
    class Meta:
        verbose_name = 'UploadFile'
        verbose_name_plural = 'UploadFile'
    
    pdf_file = models.FileField(upload_to='students_results')
    # store extracted text from pdf_file
    extracted_text = models.TextField()

    def get_file_name(self):
        return os.path.basename(self.pdf_file.name)
    
    def get_extracted_text(self):
        return self.extracted_text
    
    def __str__(self):
        return self.get_file_name()
    


class ExcelFileFromPdf(models.Model):
    """Model definition for ExcelFileFromPdf.
    store excel file generated from pdf file
    """
    class Meta:
        verbose_name = 'ExcelFileFromPdf'
        verbose_name_plural = 'ExcelFileFromPdf'
    
    pdf_file = models.ForeignKey('UploadFile', on_delete=models.CASCADE, blank=True, null=True)
    excel_file = models.FileField(upload_to='students_results_excel')

    def get_file_name(self):
        return os.path.basename(self.excel_file.name)
    
    def get_file(self):
        return self.excel_file
    
    def __str__(self):
        return self.get_file_name()
    
