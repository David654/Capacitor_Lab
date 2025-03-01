"""
    Electricity and Magnetism
    Practical P1: Capacitor
    
    All data files (.csv) should be in a subfolder 'data' of the folder
    this file is.
    VQ expects file name to start with VQ
    VR expects VR
    VX expects VX
    
    VQ data files should contain columns
        'Number #(number)' and 'Voltage #(number)'
    VR data files should contain columns
        'Radius #(number)' and 'Voltage #(number)'
    VX data files should contain columns
        'Distance #(number)' and 'Voltage #(number)'
        
        
    When calling functions it is possible to specify optional parameters:
        - 'save' saves .eps image in a subfolder 'figures';
        - for others see each function.
    
    26/02/2025
"""

from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import numpy as np
import os

path = r'\data'

basepath = os.path.dirname(__file__)

"""
Make a graph of the measured voltage versus the number of
charges applied, for both distances used.
"""

def VQ(path, **kwargs):
    # Optional arguments to save (see at the end) and plot error bars
    save = kwargs.get('save', False)
    xerr = kwargs.get('xerr', -1)
    yerr = kwargs.get('yerr', -1)
    
    folder = glob(basepath + path + r'\VQ*')
    for file in folder:
        num, max_n, max_v = 1, 0, 0
        file_data = pd.read_csv(file)
        fig, ax = plt.subplots(1, 1)
        
        ax.set_xlabel("Number of charge transfers")
        ax.set_ylabel("Capacitor voltage, V")
        
        num_col = r'Number #' + str(num)
        vlt_col = r'Voltage #' + str(num)
        
        
        while num_col in file_data.columns:
            n = pd.read_csv(file, usecols=[num_col], skip_blank_lines=True)
            n.dropna(how="all", inplace=True)
            n = n.values.flatten()
            
            voltage = pd.read_csv(file, usecols=[vlt_col], skip_blank_lines=True)
            voltage.dropna(how="all", inplace=True)
            voltage = voltage.values.flatten()
            
            
            n, voltage = (list(t) for t in zip(*sorted(zip(n, voltage))))
            max_n = max(max_n, n[-1])
            max_v = max(max_v, voltage[-1])
            
            if xerr >= 0 and yerr >= 0:
                plt.errorbar(n, voltage, xerr = xerr, yerr = yerr, fmt='o', linestyle='--', capsize=2, label='Run: '+str(num))
            else:
                plt.plot(n, voltage, label=num_col)
            num += 1
            num_col = r'Number #' + str(num)
            vlt_col = r'Voltage #' + str(num)
            
        plt.xticks(np.arange(0, max_n+1, 1))
        plt.yticks(np.arange(0, max_v+1, 5))
        plt.ylim(ymax=max_v+2)
        plt.tight_layout()
        plt.legend()
        if save:
            plt.savefig(basepath+r'/figures/'+os.path.basename(file)[:-4]+r'.eps', format="eps")
        plt.show()
    
        
# Voltage vs Radius
# Assinment D
def VR(path, **kwargs):
    save = kwargs.get('save', False)
    
    folder = glob(basepath + path + r'\VR*')
    for file in folder:
        num = 1
        file_data = pd.read_csv(file)
        fig, ax = plt.subplots(1, 1)
        
        ax.set_title('Voltage $V$ vs radius $r$')
        ax.set_xlabel("Radius")
        ax.set_ylabel("Voltage")
        
        num_col = r'Radius #' + str(num)
        vlt_col = r'Voltage #' + str(num)
        
        while num_col in file_data.columns:
            n = pd.read_csv(file, usecols=[num_col], skip_blank_lines=True)
            n.dropna(how="all", inplace=True)
            n = n.values.flatten()
            
            voltage = pd.read_csv(file, usecols=[vlt_col], skip_blank_lines=True)
            voltage.dropna(how="all", inplace=True)
            voltage = voltage.values.flatten()
            
            n, voltage = (list(t) for t in zip(*sorted(zip(n, voltage))))
            
            plt.plot(n, voltage)
            num += 1
            num_col = r'Radius #' + str(num)
            vlt_col = r'Voltage #' + str(num)
        
        plt.tight_layout()
        if save:
            plt.savefig(basepath+r'/figures/'+os.path.basename(file)[:-4]+r'.eps', format="eps")
        plt.show()


# Voltage vs Plate Distance
# Assinment E
def VX(path, **kwargs):
    save = kwargs.get('save', False)
    inverse = kwargs.get('inverse', False)
    extrapolate = kwargs.get('extrp', False)
    
    folder = glob(basepath + path + r'\VX*')
    for file in folder:
        if not inverse:
            num = 1
            file_data = pd.read_csv(file)
            fig, ax = plt.subplots(1, 1)
            
            ax.set_title('Voltage $V$ vs distance $x$')
            ax.set_xlabel("Distance")
            ax.set_ylabel("Voltage")
            
            num_col = r'Distance #' + str(num)
            vlt_col = r'Voltage #' + str(num)
            
            while num_col in file_data.columns:
                n = pd.read_csv(file, usecols=[num_col], skip_blank_lines=True)
                n.dropna(how="all", inplace=True)
                n = n.values.flatten()
                
                voltage = pd.read_csv(file, usecols=[vlt_col], skip_blank_lines=True)
                voltage.dropna(how="all", inplace=True)
                voltage = voltage.values.flatten()
                
                n, voltage = (list(t) for t in zip(*sorted(zip(n, voltage))))
                
                plt.plot(n, voltage)
                num += 1
                num_col = r'Distance #' + str(num)
                vlt_col = r'Voltage #' + str(num)
                
            plt.tight_layout()
            if save:
                plt.savefig(basepath+r'/figures/'+os.path.basename(file)[:-4]+r'.eps', format="eps")
            plt.show()
        else:
            num = 1
            file_data = pd.read_csv(file)
            fig, ax = plt.subplots(1, 1)
            
            ax.set_title('Voltage $V$ vs distance $x$')
            ax.set_xlabel("Inv distance")
            ax.set_ylabel("Inv voltage")
            
            num_col = r'Distance #' + str(num)
            vlt_col = r'Voltage #' + str(num)
            
            while num_col in file_data.columns:
                n = pd.read_csv(file, usecols=[num_col], skip_blank_lines=True)
                n.dropna(how="all", inplace=True)
                n = 1/(n.values.flatten())
                
                voltage = pd.read_csv(file, usecols=[vlt_col], skip_blank_lines=True)
                voltage.dropna(how="all", inplace=True)
                voltage = 1/(voltage.values.flatten())
                
                plt.plot(n, voltage)
                num += 1
                num_col = r'Distance #' + str(num)
                vlt_col = r'Voltage #' + str(num)
                
                if extrapolate:
                    print("yay")
                    f = interp1d(n, voltage, fill_value="extrapolate")
                    xx = np.linspace(0, max(n), 1000)
                    plt.plot(xx, f(xx))
                
            plt.tight_layout()
            if save:
                plt.savefig(basepath+r'/figures/'+os.path.basename(file)[:-4]+r'.eps', format="eps")
            plt.show()
            
# VQ1 - 2mm
# VQ2 - 4mm

# VR plate distance 10+-0.1cm

#VX(path)
#VX(path,inverse=True)
VQ(path, xerr=0, yerr=1)