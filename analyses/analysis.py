import uproot # for reading .root files
import awkward as ak # to represent nested data in columnar format
import vector # for 4-momentum calculations
import math # for mathematical functions such as square root
import numpy as np # for numerical calculations such as histogramming
import matplotlib.pyplot as plt # for plotting
from matplotlib.ticker import AutoMinorLocator # for minor ticks
import matplotlib.colors as mcolors # for changing the hatch color
import time # to measure time to analyse
import os
import json
import argparse
import sys
import logging

# Global variables
# Units
MeV = 0.001
GeV = 1.0

SKIM = '2to4lep'
TUPLE_PATH = f'/eos/user/m/mvivasal/{SKIM}/'

    # Samples to use for the analysis
SAMPLES = {
    'data': {
        'list' : ['data15_periodD','data15_periodE',
                'data15_periodF','data15_periodG',
                'data15_periodH','data15_periodJ',
                'data16_periodA','data16_periodB',
                'data16_periodC','data16_periodD',
                'data16_periodE','data16_periodF',
                'data16_periodG','data16_PeriodI',
                'data16_periodK','data16_periodL'],
    },
    
    r'Background $Z,t\bar{t},t\bar{t}+V,VVV$' : { # Z+t+vvv
        'list' : ['410472.PhPy8EG_A14_ttbar_hdamp258p75_dil',
                    '410155.aMcAtNloPythia8EvtGen_MEN30NLO_A14N23LO_ttW',
                    '410218.aMcAtNloPythia8EvtGen_MEN30NLO_A14N23LO_ttee',
                    '410219.aMcAtNloPythia8EvtGen_MEN30NLO_A14N23LO_ttmumu',
                    '412043.aMcAtNloPythia8EvtGen_A14NNPDF31_SM4topsNLO',
                    '364243.Sherpa_222_NNPDF30NNLO_WWZ_4l2v_EW6',
                    '364242.Sherpa_222_NNPDF30NNLO_WWW_3l3v_EW6',
                    '364246.Sherpa_222_NNPDF30NNLO_WZZ_3l3v_EW6',
                    '364248.Sherpa_222_NNPDF30NNLO_ZZZ_4l2v_EW6',
                    '700320.Sh_2211_Zee_maxHTpTV2_BFilter',
                    '700321.Sh_2211_Zee_maxHTpTV2_CFilterBVeto',
                    '700322.Sh_2211_Zee_maxHTpTV2_CVetoBVeto',
                    '700323.Sh_2211_Zmumu_maxHTpTV2_BFilter',
                    '700324.Sh_2211_Zmumu_maxHTpTV2_CFilterBVeto',
                    '700325.Sh_2211_Zmumu_maxHTpTV2_CVetoBVeto'
                ],
        'color' : "#6b59d3" # purple
    },

    r'Background $ZZ^*$' : { # ZZ
        'list' : ['700600.Sh_2212_llll',
                '700601.Sh_2212_lllv'],
        'color' : "#ff0000" # red
    },

    r'Signal ($m_H$ = 125 GeV)' : { # H -> ZZ -> llll
        'list' : ['345060.PowhegPythia8EvtGen_NNLOPS_nnlo_30_ggH125_ZZ4l',
                    '346228.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_ZZ4lep_notau',
                    '346414.aMcAtNloPythia8EvtGen_tHjb125_4fl_ZZ4l',
                    '346511.aMcAtNloPythia8EvtGen_tWH125_ZZ4l',
                    '346310.PowhegPythia8EvtGen_NNPDF30_AZNLO_ZH125J_Zincl_H_incl_MINLO',
                    '346311.PowhegPythia8EvtGen_NNPDF30_AZNLO_WpH125J_Wincl_H_incl_MINLO',
                    '346312.PowhegPythia8EvtGen_NNPDF30_AZNLO_WmH125J_Wincl_H_incl_MINLO',
                    '346340.PowhegPy8EG_A14NNPDF23_NNPDF30ME_ttH125_ZZ4l_allhad',
                    '346341.PowhegPy8EG_A14NNPDF23_NNPDF30ME_ttH125_ZZ4l_semilep',
                    '346342.PowhegPy8EG_A14NNPDF23_NNPDF30ME_ttH125_ZZ4l_dilep',
                    '345066.PowhegPythia8EvtGen_NNPDF3_AZNLO_ggZH125_ZZ4lepZinc'],
        'color' : "#00cdff" # light blue
    },

}

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define log format
    handlers=[
        logging.FileHandler("logfile.log"),  # File to log messages
        logging.StreamHandler(sys.stdout)  # Optional: also prints to console
    ]
)

def lepton_type_cut(lep_type, n_leptons, cut):
    """
    Apply a cut based on the lepton type.
    
    Parameters:
    lep_type (array): The array of lepton types.
    n_leptons (int): The number of leptons expected in the event.
    cut (str): Selected flavor cut ('Yes' for same flavor, 'No' for different flavor).
    
    Returns:
    mask (array): A mask to apply to the data for filtering the events.
    """
    # Check only the first two leptons
    if cut == 'same':
        if n_leptons == 2 or n_leptons == 3:
            # For 2 or 3 leptons, we apply the same-flavor cut to the first two leptons
            sum_lep_type = lep_type[:, 0] + lep_type[:, 1]
            mask = (sum_lep_type == 22) | (sum_lep_type == 26)  # Same-flavor: e+e- or mu+mu-

        elif n_leptons == 4 or n_leptons == 5:
            # For 4 or 5 leptons, check combinations of four leptons
            sum_lep_type = lep_type[:, 0] + lep_type[:, 1] + lep_type[:, 2] + lep_type[:, 3]
            mask = (sum_lep_type == 44) | (sum_lep_type == 48) | (sum_lep_type == 52)

    elif cut == 'different':
        if n_leptons == 2 or n_leptons == 3:
            # For 2 or 3 leptons, allow different flavor for the first two leptons
            sum_lep_type = lep_type[:, 0] + lep_type[:, 1]
            mask = (sum_lep_type == 24)  # e+mu- or e-mu+
            
            # Ensure that if there is a third lepton, it is an electron or muon
            if n_leptons == 3:
                third_lepton_mask = (lep_type[:, 2] == 11) | (lep_type[:, 2] == 13)  # Allow electron or muon for the third lepton
                mask = mask & third_lepton_mask  # Combine both conditions

        elif n_leptons == 4 or n_leptons == 5:
            # For 4 or 5 leptons, check combinations of four leptons
            sum_lep_type = lep_type[:, 0] + lep_type[:, 1] + lep_type[:, 2] + lep_type[:, 3]
            mask = (sum_lep_type == 48) 

    return mask

def lepton_charge_cut(lep_charge, n_leptons, cut):
    if cut=='opposite':
        if n_leptons == 2 or n_leptons == 3:
            # For 2 or 3 leptons, the mask is based on the sum of the first two leptons
            sum_lep_charge = lep_charge[:, 0] + lep_charge[:, 1]
            mask = sum_lep_charge == 0
            
        elif n_leptons == 4 or n_leptons == 5:
            # For 4 or 5 leptons, the mask checks combinations of four leptons
            sum_lep_charge_first = lep_charge[:, 0] + lep_charge[:, 1]
            sum_lep_charge_second = lep_charge[:, 2] + lep_charge[:, 3]
            mask = (sum_lep_charge_first == 0) & (sum_lep_charge_second == 0)

    elif cut=='same':
        if n_leptons == 2 or n_leptons == 3:
            # For 2 or 3 leptons, the mask is based on the sum of the first two leptons
            sum_lep_charge = lep_charge[:, 0] + lep_charge[:, 1]
            mask = (sum_lep_charge == 2)|(sum_lep_charge == -2)
            
        elif n_leptons == 4 or n_leptons == 5:
            # For 4 or 5 leptons, the mask checks combinations of four leptons
            sum_lep_charge_first = lep_charge[:, 0] + lep_charge[:, 1]
            sum_lep_charge_second = lep_charge[:, 2] + lep_charge[:, 3]
            mask = ((sum_lep_charge_first == 2)|(sum_lep_charge_first == -2))&((sum_lep_charge_second == 2)|(sum_lep_charge_second == -2))
    
    return mask

def calc_weight(events,lumi):
    return (
        (lumi*1000*events.xsec*events.filteff*events.kfac #events.corrected_xsec#
        * events.mcWeight
        * events.ScaleFactor_PILEUP
        * events.ScaleFactor_ELE
        * events.ScaleFactor_MUON)/(events.sum_of_weights)
        #* events.scaleFactor_LepTRIGGER
    )

def invariant_mass(pt, eta, phi, E, n_leptons):
    p4 = vector.zip({"pt": pt, "eta": eta, "phi": phi, "E": E})

    if n_leptons == 2:
        mass = (p4[:, 0] + p4[:, 1]).M
    elif n_leptons == 3:
        mass = (p4[:, 0] + p4[:, 1] + p4[:, 2]).M
    elif n_leptons == 4:
        mass = (p4[:, 0] + p4[:, 1] + p4[:, 2] + p4[:, 3]).M
    elif n_leptons == 5:
        mass = (p4[:, 0] + p4[:, 1] + p4[:, 2] + p4[:, 3]+ + p4[:, 4]).M

    return mass

def read_file(path,sample, lumi_used, n_leptons, flavor, charge_pair, bin_edges, lumi_weights=None):
    start = time.time() # start the clock
    logging.info("\tProcessing: "+sample) # print which sample is being processed
    # Initialize histograms for 'mass' and sum of weights squared
    hist_mass = np.zeros(len(bin_edges) - 1)
    hist_mass_weights_squared = np.zeros(len(bin_edges) - 1)
    
    # Initialize counters for event counts
    event_counts = {'initial_events':0,
                   'after_cleaning_leptons':0,
                   'after_lepton_type_cut':0,
                   'after_lepton_charge_cut':0,
                   'after_leptonpt_cut':0}
    
    # open the tree called mini using a context manager (will automatically close files/resources)
    with uproot.open(path + ":analysis") as tree:
        numevents = tree.num_entries # number of events
        #if 'data' not in sample: xsec_weight = get_xsec_weight(sample) # get cross-section weight
        for data in tree.iterate(['lep_n','lep_pt','lep_eta','lep_phi','lep_e','lep_charge','lep_type', 
                                  'lep_isTightID', 'lep_isLooseID','lep_isMediumID','lep_isLooseIso',
                                  'lep_isTightIso',
                                  #'lep_isLooseID','lep_isMediumID',
                                  # add more variables here if you make cuts on them 
                                  'mcWeight','ScaleFactor_PILEUP',
                                  'ScaleFactor_ELE','ScaleFactor_MUON','scaleFactor_LepTRIGGER',
                                  'sum_of_weights','corrected_xsec','xsec','num_events',
                                  'filteff','kfac',
                                 'trigE','trigM'] + ((['DatasetNumber'] if not "data" in sample else [])),
                                  #'ScaleFactor_LepTRIGGER'], # variables to calculate Monte Carlo weight
                                 library="ak", # choose output type as awkward array
                                 entry_stop=numevents*lumi_used/36): # process up to numevents*fraction
            
            nIn = len(data) # number of events in this batch
            
            if 'data' in sample:
                # Update the initial event count
                event_counts['initial_events'] += nIn
             
            # N_leptons cut
            data = data[data['lep_n'] == n_leptons]
            
            # Prepare variables
            for i in range(0,n_leptons):
                data[f'lep_pt{i+1}'] = data['lep_pt'][:,i]
                data[f'lep_looseID{i+1}'] = data['lep_isLooseID'][:,i]
                data[f'lep_mediumID{i+1}'] = data['lep_isMediumID'][:,i]
                data[f'lep_looseIso{i+1}'] = data['lep_isLooseIso'][:,i]
                data[f'lep_type{i+1}'] = data['lep_type'][:,i]
            
            # Apply trigger
            data = data[data['trigE'] | data['trigM']]
            
            for i in range(0,n_leptons):
                # Keep events where all four leptons pass the loose isolation criteria.
                data = data[data[f'lep_looseIso{i+1}']]
                # Make sure that every muon is medium and every electron is loose
                data = data[((data[f'lep_type{i+1}'] == 13) & (abs(data[f'lep_mediumID{i+1}'])==1)) | \
                            ((data[f'lep_type{i+1}'] == 11) & (abs(data[f'lep_looseID{i+1}'])==1))]
            
            if 'data' in sample:
                # Update the event count after cleaning leptons
                event_counts['after_cleaning_leptons'] += len(data)
            
            logging.info("Cut : After cleaning leptons       : %i"%len(data)) 

            # Cut on lepton charge using the function cut_lep_charge defined above
            mask_lep_type = lepton_type_cut(data.lep_type, n_leptons, flavor)
            data = data[mask_lep_type]
            
            if 'data' in sample:
                # Update the event count after lepton type cut
                event_counts['after_lepton_type_cut'] += len(data)
            logging.info(f"Cut : After lepton_type_cut : {len(data)}")

            # cut on lepton type using the function cut_lep_type defined above
            mask_lep_charge = lepton_charge_cut(data.lep_charge, n_leptons, charge_pair)
            data = data[mask_lep_charge]
            
            if 'data' in sample:
                # Update the event count after lepton charge cut
                event_counts['after_lepton_charge_cut'] += len(data)
            logging.info(f"Cut : After lepton_charge_cut : {len(data)}")
            
            if lumi_weights: #mening it is higgs
                # pT cuts
                data = data[data['lep_pt1'] > 20]
                data = data[data['lep_pt2'] > 15]
                data = data[data['lep_pt3'] > 10]

                if 'data' in sample:
                    # Update the event count after lepton charge cut
                    event_counts['after_leptonpt_cut'] += len(data)
                
                logging.info(f"Cut : After lepton pT cut : {len(data)}")

            # calculation of 4-lepton invariant mass using the function calc_mllll defined above
            data['mass'] = invariant_mass(data.lep_pt, data.lep_eta, data.lep_phi, data.lep_e, n_leptons)
            
            # Calculate weights for MC samples
            if 'data' not in sample:
                logging.info("Bkg   : %s"%sample)
                data['totalWeight'] = calc_weight(data, lumi_weights)
                weights = data['totalWeight']
                weights_squared = weights ** 2
            else:
                weights = None
                weights_squared = None

            # Fill histograms
            counts, _ = np.histogram(data['mass'], bins=bin_edges, weights=weights)
            hist_mass += counts

            # Accumulate sum of weights squared for statistical errors
            if weights is not None:
                counts_weights_squared, _ = np.histogram(data['mass'], bins=bin_edges, weights=weights_squared)
                hist_mass_weights_squared += counts_weights_squared

            # Optional: print progress
            nOut = np.sum(counts)
            elapsed = time.time() - start
            logging.info(f"\t\tProcessed {nOut} events out of {nIn} in {round(elapsed, 1)}s")

    return hist_mass, hist_mass_weights_squared, event_counts

def get_data_from_files(lumi_data, lumi_mc, n_leptons, flavor, charge_pair, bin_edges, process_mc=True):
    data = {}  # Dictionary to hold histograms for each sample
    data_weights_squared = {}  # For statistical uncertainties
    
    # Initialize counters data for event counts
    event_counts = {'initial_events':0,
                   'after_cleaning_leptons':0,
                   'after_lepton_type_cut':0,
                   'after_lepton_charge_cut':0,
                   'after_leptonpt_cut':0}

    for s in SAMPLES:
        logging.info(f'Processing {s} samples')
        hist_mass_total = np.zeros(len(bin_edges) - 1)
        hist_mass_weights_squared_total = np.zeros(len(bin_edges) - 1)

        for val in SAMPLES[s]['list']:
            period_event_counts = {'initial_events':0,
                   'after_cleaning_leptons':0,
                   'after_lepton_type_cut':0,
                   'after_lepton_charge_cut':0,
                   'after_leptonpt_cut':0}
            
            if s == 'data':
                prefix = "Data/"
                fileString = TUPLE_PATH + prefix + val + ".root"
            else:
                prefix = "MC/mc_"
                fileString = TUPLE_PATH + prefix + val + f".{SKIM}" + ".root"

            if not os.path.isfile(fileString):
                logging.info(f"WARNING: File {fileString} does not exist. Skipping.")
                continue
                
            if process_mc:
                if s == 'data':
                    hist_mass, hist_mass_weights_squared, period_event_counts = read_file(fileString, val, lumi_data, 
                                                                                     n_leptons, flavor, charge_pair, 
                                                                                     bin_edges, lumi_weights=lumi_data)
                else:
                    # period_event_counts should be just zeros here
                    hist_mass, hist_mass_weights_squared, _ = read_file(fileString, val, lumi_mc, 
                                                                                     n_leptons, flavor, charge_pair, 
                                                                                     bin_edges, lumi_weights=lumi_data)
                    
            elif s == 'data':
                hist_mass, hist_mass_weights_squared, period_event_counts = read_file(fileString, val, lumi_data, 
                                                                                     n_leptons, flavor, charge_pair, 
                                                                                     bin_edges)

            hist_mass_total += hist_mass
            hist_mass_weights_squared_total += hist_mass_weights_squared

            event_counts['initial_events'] += period_event_counts['initial_events']
            event_counts['after_cleaning_leptons'] += period_event_counts['after_cleaning_leptons']
            event_counts['after_lepton_type_cut'] += period_event_counts['after_lepton_type_cut']
            event_counts['after_lepton_charge_cut'] += period_event_counts['after_lepton_charge_cut']
            event_counts['after_leptonpt_cut'] += period_event_counts['after_leptonpt_cut']

        data[s] = hist_mass_total
        data_weights_squared[s] = hist_mass_weights_squared_total

    return data, data_weights_squared, event_counts

def make_plot(data, data_weights_squared, lumi_used, bin_edges, background='light', components_to_plot=None, 
              filename_suffix='data_backgrounds_signal', filename_prefix='Higgs_', n_leptons='4'):
    # Set colors based on background
    if background == 'light':
        text_color = 'black'
        data_point_color = 'black'
        axes_color = 'black'
        legend_edge_color = 'white'  # Optional: Hide legend frame
    else:
        text_color = 'white'
        data_point_color = 'white'
        axes_color = 'white'
        legend_edge_color = 'none'  # Optional: Hide legend frame

    # Adjust the figure size
    plt.figure(figsize=(10, 6))
    plt.rcParams['text.color'] = text_color
    plt.rcParams['axes.labelcolor'] = text_color
    plt.rcParams['xtick.color'] = text_color
    plt.rcParams['ytick.color'] = text_color
    plt.rcParams['axes.edgecolor'] = axes_color

    # Set transparent background
    plt.gca().patch.set_alpha(0.0)

    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = bin_edges[1] - bin_edges[0]

    # Extract data histogram and errors
    data_x = data['data']
    data_x_errors = np.sqrt(data_x)  # Poisson errors for data

    # Plot data points if 'data' is in components_to_plot or components_to_plot is None
    if components_to_plot is None or 'data' in components_to_plot:
        plt.errorbar(bin_centres, data_x, yerr=data_x_errors, fmt='o', color=data_point_color, label='Data')

    # Prepare MC histograms
    mc_histograms = []
    mc_histograms_weights_squared = []
    mc_colors = []
    mc_labels = []
    identifiers = []

    # Determine which samples to include
    if components_to_plot is None:
        components_to_plot = [key for key in SAMPLES.keys() if key != 'data']

    for s in SAMPLES.keys():
        if s != 'data' and s in components_to_plot:
            mc_histogram = data[s]
            mc_histograms.append(mc_histogram)
            mc_histogram_weights_squared = data_weights_squared[s]
            mc_histograms_weights_squared.append(mc_histogram_weights_squared)
            mc_colors.append(SAMPLES[s]['color'])
            mc_labels.append(s)
            identifiers.append(s)

    # Plot stacked MC histograms
    bottom = np.zeros(len(bin_centres))
    for hist, color, label in zip(mc_histograms, mc_colors, mc_labels):
        plt.bar(bin_centres, hist, width=bin_width, bottom=bottom, color=color, label=label)
        bottom += hist  # Update bottom for stacking

    # Calculate total MC histogram and errors
    if mc_histograms:
        mc_total_histogram = np.sum(mc_histograms, axis=0)
        mc_total_weights_squared = np.sum(mc_histograms_weights_squared, axis=0)
        mc_total_errors = np.sqrt(mc_total_weights_squared)

        # Plot MC statistical uncertainties
        bars = plt.bar(bin_centres, 2 * mc_total_errors, width=bin_width, bottom=mc_total_histogram - mc_total_errors,
                       alpha=0.5, color='none', hatch='////', label='MC Stat. Unc.')

        # Set the hatch color by converting text_color to an RGBA tuple
        import matplotlib.colors as mcolors
        hatch_color_rgba = mcolors.to_rgba(text_color)

        for bar in bars:
            bar._hatch_color = hatch_color_rgba
            
        # Determine the maximum y-value based on MC histograms
        y_max = mc_total_histogram.max() * 1.6
    else:
        # If no MC histograms are plotted, use the maximum of the data
        y_max = data_x.max() * 1.6

    # Customize plot
    plt.xlabel(fr'{n_leptons}-lepton invariant mass $\mathrm{{m_{{{n_leptons}}}}}$ [GeV]', fontsize=12)
    plt.ylabel(f'Events / {bin_width} GeV')
    plt.xlim(bin_edges[0], bin_edges[-1])
    plt.ylim(0, y_max)
    plt.legend(frameon=False, edgecolor=legend_edge_color, loc='upper right', fontsize=12)

    # The anotations for Higgs are more towards the middle, to avoid th Z peak
    if filename_prefix=='Higgs_': # Only for higgs
        plt.text(0.2, 0.93, 'ATLAS Open Data', transform=plt.gca().transAxes, fontsize=16, color=text_color)
        plt.text(0.2, 0.88, 'for education', transform=plt.gca().transAxes, style='italic', fontsize=12, color=text_color)
        plt.text(0.2, 0.82, f'$\sqrt{{s}}$=13 TeV, $\int$L dt = {lumi_used} fb$^{{-1}}$', transform=plt.gca().transAxes, color=text_color, fontsize=12)
        plt.text(0.2, 0.76, r'$H \rightarrow ZZ^* \rightarrow 4\ell$', transform=plt.gca().transAxes, color=text_color, fontsize=12)

    # The anotations for everything else are more towards the corner, to avoid th Z peak
    # That is more centered in these
    else:
        # Add text annotations
        plt.text(0.05, 0.93, 'ATLAS Open Data', transform=plt.gca().transAxes, fontsize=16, color=text_color)
        plt.text(0.05, 0.88, 'for education', transform=plt.gca().transAxes, style='italic', fontsize=12, color=text_color)
        plt.text(0.05, 0.82, f'$\sqrt{{s}}$=13 TeV, $\int$L dt = {lumi_used} fb$^{{-1}}$', transform=plt.gca().transAxes, color=text_color, fontsize=12)


    plt.tight_layout()
    filename = f'{lumi_used}_{filename_prefix}_{filename_suffix}_{background}.png'
    plt.savefig(filename, bbox_inches='tight', transparent=True)
    plt.close()

    return filename

def main():
    # All the prints to a logfile
    sys.stdout = open('logfile.log', 'w')
    # DEFAULT SETTINGS
    parser = argparse.ArgumentParser(description="Run analysis for teachers app with ATLAS Open Data")
    parser.add_argument('-l', '--lumis', nargs='+', type=int, default=[36],
                        help='List of Integrated luminosities for the analysis [Default: 36]')
    parser.add_argument('-n', '--nlep', nargs='+', type=int, default=[2],
                        help='List of Number of leptons for the analysis [Default: 2]')
    parser.add_argument('-f', '--flavlep', nargs='+', type=str, default=['same'],
                        help='List of Flavors for lepton pairs. Options: same, different [Default: same]')
    parser.add_argument('-c', '--charlep', nargs='+', type=str, default=['opposite'],
                        help='List of Charges for lepton pairs. Options: same, opposite [Default: opposite]')
    
    flags = parser.parse_args()

    # Options for the analysis
    LUMIS_USED = flags.lumis # Integrated luminosity
    NLEPTONS = flags.nlep
    FLAVORS_LEPTONS = flags.flavlep
    CHARGES_LEPTONS = flags.charlep

    # Initialize the JSON structure
    results_json = {}

    # Iterate over all combinations of parameters
    for lumi in LUMIS_USED:
        logging.info(f"\nRunning analysis for Luminosity: {lumi}")
        lumi_key = str(lumi)
        results_json[lumi_key] = {}
        results_json[lumi_key]['nEvents'] = 0  # Initialize total initial_events for this luminosity

        for n_leptons in NLEPTONS:
            for flavor_leptons in FLAVORS_LEPTONS:
                for charge_leptons in CHARGES_LEPTONS:
                    logging.info(f"Processing configuration: n_leptons={n_leptons}, "
                          f"flavor={flavor_leptons}, charge={charge_leptons}")
                    
                    # Determine if this configuration corresponds to Higgs analysis
                    is_higgs = (n_leptons == 4) and (flavor_leptons == 'same') and (charge_leptons == 'opposite')

                    # Define bin edges based on whether it's Higgs or not
                    if is_higgs:
                        xmin = 80 * GeV
                        xmax = 170 * GeV
                        step_size = 2.5 * GeV
                        MC = True  # Process MC only for Higgs configurations
                    else:
                        xmin = 50 * GeV
                        xmax = 140 * GeV
                        step_size = 2.5 * GeV
                        MC = False  # Do not process MC for non-Higgs configurations

                    bin_edges = np.arange(start=xmin, stop=xmax + step_size, step=step_size)

                    # Run the analysis for the current configuration
                    start_time = time.time()
                    data, data_weights_squared, event_counts = get_data_from_files(lumi_data=lumi,
                                                                                   lumi_mc=36, 
                                                                                   n_leptons=n_leptons, 
                                                                                   flavor=flavor_leptons, 
                                                                                   charge_pair=charge_leptons, 
                                                                                   bin_edges=bin_edges, 
                                                                                   process_mc = MC
                                                                                   )
                    
                    elapsed_time = time.time() - start_time
                    logging.info(f"Time taken for this configuration: {round(elapsed_time, 1)}s")
                    logging.info(f"event counts: {event_counts}")

                    # Map configuration to JSON keys
                    nlep_key = f"{n_leptons}leptons"
                    flavor_key = f"flavor{flavor_leptons.capitalize()}"
                    charge_key = f"charge{charge_leptons.capitalize()}"
                    pt_key = "ptLeptons"

                    # Initialize nested dictionaries if they don't exist
                    if nlep_key not in results_json[lumi_key]:
                        results_json[lumi_key][nlep_key] = {}
                    if flavor_key not in results_json[lumi_key][nlep_key]:
                        results_json[lumi_key][nlep_key][flavor_key] = {}
                    if charge_key not in results_json[lumi_key][nlep_key][flavor_key]:
                        results_json[lumi_key][nlep_key][flavor_key][charge_key] = {}
                    if (pt_key not in results_json[lumi_key][nlep_key][flavor_key][charge_key]) and (is_higgs):
                        results_json[lumi_key][nlep_key][flavor_key][charge_key][pt_key] = {}

                    # Assign event counts to the nested JSON structure
                    # Top-level 'nEvents' accumulates initial_events across configurations
                    results_json[lumi_key]['nEvents'] = event_counts['initial_events']

                    # Assign 'nEvents' after cleaning leptons
                    results_json[lumi_key][nlep_key]['nEvents'] = event_counts['after_cleaning_leptons']

                    # Assign 'n_events' after lepton type cut under flavor
                    results_json[lumi_key][nlep_key][flavor_key]['nEvents'] = event_counts['after_lepton_type_cut']

                    # Assign 'nEvents' after lepton charge cut under charge
                    results_json[lumi_key][nlep_key][flavor_key][charge_key]['nEvents'] = event_counts['after_lepton_charge_cut']

                    if is_higgs:
                        # Assign 'nEvents' after lepton pT cut under 'ptLeptons'
                        results_json[lumi_key][nlep_key][flavor_key][charge_key][pt_key]['nEvents'] = event_counts['after_leptonpt_cut']

                    # Define plot configurations based on whether it's Higgs or not
                    if is_higgs:
                        current_plot_configs = [
                            {
                                'components_to_plot': ['data'],
                                'filename_suffix': 'data_only',
                                'filename_prefix': f'Higgs_'
                            },
                            {
                                'components_to_plot': ['data', r'Background $Z,t\bar{t},t\bar{t}+V,VVV$', r'Background $ZZ^*$'],
                                'filename_suffix': 'data_backgrounds',
                                'filename_prefix': f'Higgs_'
                            },
                            {
                                'components_to_plot': None,  # None will plot all components
                                'filename_suffix': 'data_backgrounds_signal',
                                'filename_prefix': f'Higgs_'
                            }
                        ]
                    else:
                        current_plot_configs = [
                            {
                                'components_to_plot': ['data'],
                                'filename_suffix': 'data_only',
                                'filename_prefix': f'{n_leptons}_{flavor_leptons}_{charge_leptons}_'
                            },
                        ]

                    # Loop over plot configurations and generate plots
                    for config in current_plot_configs:
                        components = config['components_to_plot']
                        filename_suffix = config['filename_suffix']
                        filename_prefix = config['filename_prefix']  # Fixed the typo here

                        # Call the make_plot function for 'light' background
                        plot_light = make_plot(
                            data=data,
                            data_weights_squared=data_weights_squared,
                            lumi_used=lumi,
                            bin_edges=bin_edges,
                            background='light',
                            components_to_plot=components,
                            filename_suffix=filename_suffix,
                            filename_prefix=filename_prefix,
                            n_leptons=n_leptons
                        )

                        # Call the make_plot function for 'dark' background
                        plot_dark = make_plot(
                            data=data,
                            data_weights_squared=data_weights_squared,
                            lumi_used=lumi,
                            bin_edges=bin_edges,
                            background='dark',
                            components_to_plot=components,
                            filename_suffix=filename_suffix,
                            filename_prefix=filename_prefix,
                            n_leptons=n_leptons
                        )

                        # Assign plot filenames to the JSON structure
                        # Assuming you want to store both 'light' and 'dark' plots
                        if is_higgs:
                            results_json[lumi_key][nlep_key][flavor_key][charge_key][pt_key][f'plot_{filename_suffix}_light'] = plot_light
                            results_json[lumi_key][nlep_key][flavor_key][charge_key][pt_key][f'plot_{filename_suffix}_dark'] = plot_dark
                        else:
                            results_json[lumi_key][nlep_key][flavor_key][charge_key][f'plot_{filename_suffix}_light'] = plot_light
                            results_json[lumi_key][nlep_key][flavor_key][charge_key][f'plot_{filename_suffix}_dark'] = plot_dark


    # Save the results to a JSON file after all configurations are processed
        with open('event_counts.json', 'w') as json_file:
            json.dump(results_json, json_file, indent=4)

        logging.info("\nAnalysis complete. Results saved to 'event_counts.json'.")
 
if __name__ == "__main__":
    main()
