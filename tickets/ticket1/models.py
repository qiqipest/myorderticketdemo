from django.db import models

# Create your models here.
# ID start from: 20000
class City(models.Model):
    City_ID= models.CharField(max_length=5 , primary_key=True)
    City_Name= models.CharField(max_length=20)
    City_Pingyin= models.CharField(max_length=20)
    City_Pingyin_Short= models.CharField(max_length=3)
    City_Country= models.CharField(max_length=20)
    City_Country_Pingyin= models.CharField(max_length=20,blank=True)
    City_Country_Pingyin_Short= models.CharField(max_length=3,blank=True)

    def __unicode__(self):
        return self.City_ID
    
    class Meta:
        ordering = ['City_Name']
class Route(models.Model):

    Route_ID= models.CharField(max_length=5 , primary_key=True)
    Route_Start_City_ID= models.CharField(max_length=5)
    Route_To_City_ID= models.CharField(max_length=5)

#    Route_Start_City= models.CharField(max_length=20)
#    Route_To_City= models.CharField(max_length=20)

    def __unicode__(self):
        return self.Route_ID
    
    class Meta:
        ordering = ['Route_Start_City_ID']
# ID start from: 10000

        
# ID start from: 30000
class Catalog(models.Model):
    Catalog_ID= models.CharField(max_length=5 , primary_key=True)
    Catalog_Route_ID= models.CharField(max_length=5)
    Catalog_Original_Price= models.IntegerField()
    Catalog_Current_Price= models.IntegerField()
    Catalog_Line_Number= models.CharField(max_length=10)
    Catalog_Line_Company= models.CharField(max_length=10)
    Catalog_Line_Time_From= models.CharField(max_length=4)
    Catalog_Line_Time_To= models.CharField(max_length=4)
    Catalog_Line_Date_From= models.CharField(max_length=8)
    Catalog_Line_Date_To= models.CharField(max_length=8)
    Catalog_Name= models.CharField(max_length=10)
    Catalog_Description= models.CharField(max_length=100)

    def __unicode__(self):
        return self.Catalog_ID
    
    class Meta:
        ordering = ['Catalog_Name']
        
        
# ID start from: 40000
class Order(models.Model):
    Order_ID= models.AutoField(primary_key=True)
    Order_Catalog_ID= models.CharField(max_length=5)
    Order_Quantity= models.IntegerField()
    Order_Price= models.IntegerField()
    Order_Cus_Name= models.CharField(max_length=10)
    Order_Cus_Phone= models.CharField(max_length=20)
    Order_Cus_Remarks= models.TextField()
    Order_Create_Time= models.DateTimeField(auto_now_add=True)
    Order_Modify_Time= models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Order_ID
    
    class Meta:
        ordering = ['Order_ID']
        