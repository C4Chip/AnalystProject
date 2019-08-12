from django.db import models
from django.utils import timezone

import pandas as pd

import numpy as np
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
from io import BytesIO

# Create your models here.
class StockInfo(models.Model):
    date = models.DateTimeField(blank=False,  help_text='Date')
    open = models.DecimalField(max_digits=10, decimal_places=2,blank=True,  help_text='Open')
    high = models.DecimalField(max_digits=10, decimal_places=2,blank=True, help_text='High')
    close = models.DecimalField(max_digits=10, decimal_places=2,blank=True, help_text='Close')
    low = models.DecimalField(max_digits=10, decimal_places=2,blank=True, help_text='Low')
    volume = models.IntegerField(blank=True,  help_text='Volume')
    code = models.CharField(max_length=150,default=False, help_text='Code')
    # def __float__(self):
    #     return self.close
    # def multiChart(self):
    #     plt.plot(self.close)
    #     buffer = BytesIO()
    #     plt.savefig(buffer)
    #     plot_data = buffer.getvalue()
    #     return plot_data

    #returns = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default = 0.0, help_text='Low')
