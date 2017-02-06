from data_analysis.get_data import get_main_rows, get_val_time_data
from data_analysis.make_boxplots import make_boxplots
from data_analysis.make_ijk_plots import make_ijk_plots
from data_analysis.make_lineplots import make_lineplots

make_boxplots(get_main_rows())
make_lineplots(get_val_time_data())
#make_ijk_plots(get_main_rows())