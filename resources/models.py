from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    resources = models.ManyToManyField(Resource, through='Allocation')

    def __str__(self):
        return self.name

class Allocation(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    percentage_allocation = models.DecimalField(max_digits=5, decimal_places=2, null=True)


    def __str__(self):
        return f"{self.resource.name} - {self.project.name}"
