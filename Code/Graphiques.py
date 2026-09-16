import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import randint
from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.labelsize"] = 10
plt.rcParams.update({'font.size': 12})

Valorisation = pd.read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valorisation fusion.xlsx",
                             sheet_name = "Différences de richesses")

X = Valorisation['Age']
y = Valorisation['Diff']
plt.plot(X,y, color='teal', linewidth=2)
plt.grid(which='major',axis = 'y', color='dimgray', linestyle=':')
plt.grid(which='major',axis = 'x', color='dimgray', linestyle=':')
plt.title('Difference in % of wealth per age\n2012-2022')
plt.xlabel("Age")
plt.ylabel("Total wealth")
plt.ticklabel_format(style='plain')
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
plt.xticks(np.arange(20, max(X)+1, 10.0))
plt.savefig('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Diff_richesse_euros.svg',
            format='svg', bbox_inches="tight")

X = Valorisation['Age']
y = Valorisation['Diff_Pourcentage']
plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5)
plt.plot(X,y, color='teal', linewidth=2)
plt.grid(which='major',axis = 'y', color='dimgray', linestyle=':')
plt.grid(which='major',axis = 'x', color='dimgray', linestyle=':')
plt.xlabel("Age")
plt.ylabel("Diff. in share of housing wealth")
plt.ticklabel_format(style='plain')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
plt.xticks(np.arange(20, max(X)+1, 10.0))
plt.savefig('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Diff_richesse_%.svg',
            format='svg', bbox_inches="tight")
