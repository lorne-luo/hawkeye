import io
from datetime import datetime

import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries
from dateutil.relativedelta import relativedelta, FR

import config.settings.local as settings
from aws import dynamodb_batch_push

BATCH_LIMIT = 25


def get_alpha_vantage_api_key():
    return settings.ALPHA_VANTAGE_API_KEY2 if datetime.now().weekday() % 2 else settings.ALPHA_VANTAGE_API_KEY


ts = TimeSeries(key=get_alpha_vantage_api_key(), output_format='pandas', indexing_type='date')


def get_asx_df():
    asx_url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    asx_data = requests.get(asx_url).content
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1)

    return asx_df


def get_asx_200_df():
    # s = requests.session()
    # s.config['keep_alive'] = False
    requests.session().close()
    last_month = datetime.now() - relativedelta(months=1)
    month = last_month.strftime('%Y%m01')
    asx_url = f'https://www.asx200list.com/uploads/csv/{month}-asx200.csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    asx_data = requests.get(asx_url, headers=headers).content
    requests.session().close()
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1, usecols=[
        'Code', 'Company', 'Sector', 'Market Cap', 'Weight(%)'
    ], index_col='Code')

    return asx_df


def get_asx_200_list():
    df = get_asx_200_df()
    return df.index.values


def get_asx_20_df():
    requests.session().close()
    last_month = datetime.now() - relativedelta(months=1)
    month = last_month.strftime('%Y%m01')
    asx_url = f'https://www.asx20list.com/uploads/csv/{month}-asx20.csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    asx_data = requests.get(asx_url, headers=headers).content
    requests.session().close()
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1, usecols=[
        'Code', 'Company', 'Sector', 'Market Cap', 'Weight(%)'
    ], index_col='Code')

    return asx_df


def get_asx_20_list():
    df = get_asx_20_df()
    return df.index.values


def get_price(symbol, outputsize='compact'):
    aus_symbol = '%s.AUS' % symbol
    df, meta_data = ts.get_daily_adjusted(symbol=aus_symbol, outputsize=outputsize)
    df['Return'] = df['5. adjusted close'].pct_change(1)
    return df, meta_data


def push_industry(df):
    industry_set = df['GICS industry group'].unique()
    items = [{'name': i} for i in industry_set]

    dynamodb_batch_push('industry', items)


def push_company(df):
    items = [{'code': df.iloc[i]['ASX code'],
              'name': df.iloc[i]['Company name'],
              'industry': df.iloc[i]['GICS industry group'],
              'last_active': datetime.now().strftime('%Y-%m-%d')}
             for i in range(len(df))]

    dynamodb_batch_push('industry', items)


def get_last_friday():
    return datetime.now() + relativedelta(weekday=FR(-1))


def get_codes1():
    codes1 = list(get_asx_200_list()) + ['MFG', 'CHC', 'MGR', 'TML', 'DDR', 'EML', 'TLS', 'AD8', 'JIN', 'MVF', 'MCX',
                                         'APE', 'ASB', 'ASX', 'DTL', 'CKF', 'FMG', 'BRG', 'CNI', 'GMG', 'NCK', 'ABP',
                                         'CSR', 'MND', 'RIO', 'SXL', 'AMA', 'IVC', 'APA', 'NAN', 'AZJ', 'TCL', 'AIA',
                                         'CCL', 'SHL', 'SSM', 'BXB', 'NCM', 'CMA', 'DXS', 'JBH', 'BHP', 'VGL', 'ALX',
                                         'ILU', 'IPH', 'AST', 'VVR', 'CMW', 'GMA', 'CQE', 'SO4', 'MPL', 'AMC', 'GWA',
                                         'IEL', 'MP1', 'SUL', 'XRO', 'LLO', 'RHC', 'GOZ', 'CLW', 'NHF', 'IRE', 'CIA',
                                         'LIC', 'SYD', 'CIP', 'CWP', 'JLG', 'AOG', 'SSG', 'GOR', 'MGX', 'EHE', 'ALL',
                                         'GNE', 'CNU', 'SDG', 'ORI', 'VLW', 'IFM', 'SLR', 'JHX', 'WGX', 'JMS', 'EGF',
                                         'RND', 'AGM', 'RHP', 'HVN', 'PFP', 'STW', 'SDF', 'SGP', 'IFT', 'EGG', 'RMS',
                                         'BGP', 'AVN', 'HGL', 'REA', 'NEA', 'AQG', 'EOL', 'CNL', 'VEA', 'MTS', 'HGH',
                                         'CEN', 'SMR', 'XIP', 'SLF', 'SEK', 'WLL', 'LOV', 'KLL', 'M7T', 'MAU', 'IMA',
                                         'MYR', 'APX', 'NEC', 'SDI', 'BCI', 'GBT', 'CWY', 'SFL', 'ANN', 'NWH', 'HLS',
                                         'QUB', 'GCM', 'AHG', 'UOS', 'CBA', 'EGD', 'EFF', 'QBE', 'Z1P', 'KSL', 'AOF',
                                         'ARB', 'VIP', 'KLA', 'GPT', 'STO', 'CRD', 'HM1', 'INA', 'ARF', 'G1A', 'WTC',
                                         'AGH', 'MNY', 'WOW', 'ASG', 'EBO', 'IOD', 'WKT', 'NAB', 'MSV', 'PPT', '5GN',
                                         'CRB', 'DLX', 'FID', 'CMP', 'ALU', 'CUV', 'WES', 'NIC', 'RDC', 'TBR', 'DHG',
                                         'SVM', 'AGG', 'TIG', 'COE', 'EQT', 'HPI', 'CSL', 'KSS', 'IAG', 'SRS', 'CCP',
                                         'ELO', 'TGR', 'A2M', 'EAF', 'TLT', 'ANZ', 'PWH', 'CLV', 'KME', 'FRI', 'ZIM',
                                         'ONT', 'BOT', 'AS1', 'MQG', 'SKI', 'NGI', 'EOS', 'CVC', 'NSR', 'AZV', 'CQR',
                                         'ISX', 'CLF', 'MGC', 'BCB', 'PMV', 'ALK', 'EPW', 'MA1', 'ADI', 'CAM', 'WBC',
                                         'FBU', 'MEZ', 'CAR', 'AQR', 'VRT', 'WPL', 'CVN', 'ATM', 'DUI', 'APD', 'OML',
                                         '1AG', 'SDA', 'TPW', 'NVT', 'BEN', 'CUE', 'REH', 'MML', 'NBI', 'VG1', 'AWC',
                                         'VOC', 'SKC', 'AKG', 'TNE', 'TLX', 'DCG', 'MVP', 'ARG', 'FDV', 'EDC', 'MGG',
                                         'TNP', 'CL1', 'AB1', 'FFI', 'GRR', 'SUN', 'CCX', 'WHF', 'XF1', 'APZ', 'RFF',
                                         'BTH', 'FPH', 'COH', 'SGM', 'AUI', 'KSC', 'BVS', 'XRF', 'SVW', 'KGD', 'SAR',
                                         'DNA', 'ALI', 'SCP', 'BWP', 'CV1', 'PTB', 'ENN', 'GCI', 'FGR', 'AQZ', 'WAF',
                                         'SRV', 'ZEL', 'WLE', 'GDI', 'FGG', 'CII', 'LPI', 'BGL', 'CAT', 'BKT', 'BLD',
                                         'EAS', 'PPH', 'SHV', 'TPO', 'AYI', 'IPC', 'BPH', 'IKW', 'MTL', 'ACS', 'AIQ',
                                         'BDI', 'VYS', 'SHI', 'AMH', 'NVL', 'CIN', 'FGX', 'MDR', 'CMM', 'BUB', 'KPT',
                                         'MFF', 'KAT', 'HE8', 'STA', 'APT', 'SWF', 'JRL', 'VII', 'LYC', 'CYC', 'DUB',
                                         'SHM', 'LLC', 'IGO', 'TWD', 'HRL', 'KOV', 'CDA', 'JAL', 'DNK', 'ALC', 'JHC',
                                         'TOT', 'HIT', 'BKW', 'ASH', 'ICQ', 'RSH', 'SPL', 'GOW', 'IRI', 'STG', 'COL',
                                         'ABA', 'EME', 'NWS', 'NST', 'HT1', 'MCR', 'CZI', 'DGH', 'ERM', 'CTX', 'ANO',
                                         'CIM', 'OZL', 'ADT', 'GTR', 'HSN', 'LGD', 'RMC', 'WEB', 'RED', 'JHL', 'WGB',
                                         'EZL', 'ORA', 'MXT', 'MLD', 'SPO', 'UWL', 'RHL', 'LCM', 'DN8', 'BKI', 'IHL',
                                         'TNK', 'EXL', 'TIE', 'TAH', 'RUL', 'AHQ', 'GTK', 'SPK', 'VCX', 'NWL', 'VHT',
                                         'IDX', 'CUP', 'EVN', 'BRU', 'MWR', 'IGL', 'AVG', 'MCY', 'LEP', 'WMI', 'RMD',
                                         'CRN', 'ADH', 'KDR', '8EC', 'MLT', 'HGO', 'SGF', 'LEX', 'MYS', 'KCN', 'VEE',
                                         'AFG', 'DJW', 'AMB', 'ASL', 'CIW', 'SEC', 'CHR', 'TWR', 'NBL', 'ERF', 'AEF',
                                         'ING', 'GWR', 'MFD', 'KGN', 'BCT', 'S32', 'BBN', '8CO', 'MGU', 'NXT', 'DMG',
                                         'BPT', 'ASW', 'TAP', 'EVT', 'BTI', 'BC8', 'ALQ', 'SLC', 'SMC', 'EMR', 'ARA',
                                         'FML', 'BSE', 'INF', 'TWE', 'WAX', 'GRV', 'DOW', 'EQX', 'AHF', 'BSA', 'LYL',
                                         'AX1', 'BWR', 'HFR', 'ENR', 'FSA', 'FCT', 'AXE', 'REX', 'WEC', 'HT8', 'CDP',
                                         'CWL', 'SLX', 'BIQ', 'SNC', 'MWY', 'KNO', 'SCG', 'BMN', 'FNP', 'SIT', 'AYK',
                                         'BWX', 'RFT', 'IGN', 'NTC', 'JHG', 'GEM', 'AQI', 'QHL', 'KTE', 'MSB', 'TGP',
                                         'ABR', 'ORG', 'ERX', 'BFG', 'MRM', 'ABC', 'AGL', 'AMP', 'ALG', 'API', 'BOQ',
                                         'BAP', 'BGA', 'BAL', 'BIN', 'BKL', 'BSL', 'CGF', 'CPU', 'CTD', 'CGC', 'CWN',
                                         'CYB', 'DMP', 'ECX', 'ELD', 'EHL', 'FLT', 'GUD', 'GXY', 'GNC', 'HSO', 'HUB',
                                         'IPL', 'IFL', 'LNK', 'MIN', 'MMS', 'MYO', 'MYX', 'NHC', 'NUF', 'ORE', 'OSH',
                                         'PDL', 'PGH', 'PLS', 'PNI', 'PTM', 'QAN', 'RRL', 'RSG', 'RWC', 'SBM', 'SFR',
                                         'SGR', 'SIG', 'SIQ', 'SOL', 'SWM', 'SYR', 'TME', 'TPM', 'URW', 'WHC', 'WOR',
                                         'WSA', 'MOQ', '14D', '3PL', 'A2B', 'AEG', 'ACQ', 'ACF', 'ACR', 'ADA', 'AV1',
                                         'AML', 'AEI', 'AIS', 'AMN', 'AGR', 'AGI', 'AIZ', 'AJX', 'A40', 'A4N', 'ATC',
                                         'AJM', 'AYS', 'APL', 'AHX', 'AOP', 'ATL', 'AR9', 'ARL', 'ARQ', 'AHY', 'ATU',
                                         'AUB', 'AU8', 'AMI', 'A3D', 'AC8', 'AMG', 'ANG', 'AAC', 'ABX', 'AFI', 'ALF',
                                         'ATS', 'AVA', 'AVH', 'AVJ', 'AZS', 'BRL', 'BBX', 'BLX', 'BCC', 'BLT', 'BKY',
                                         'BFC', 'BID', 'BGT', 'BNO', 'BGS', 'BLA', 'BAF', 'BLG', 'BDA', 'BOL', 'BRB',
                                         'BUX', 'BYE', 'CDM', 'CAN', 'CP1', 'CAY', 'CAJ', 'CAA', 'CWX', 'CDV', 'CDD',
                                         'CCV', 'CYL', 'CDY', 'CTP', 'CXM', 'CFO', 'CHN', 'CSS', 'CLQ', 'CVW', 'CPV',
                                         'CGR', 'COB', 'CLH', 'COI', 'CIE', 'C6C', 'CYG', 'CPH', 'CSV', 'CYP', 'DCN',
                                         'DYL', 'DGR', 'DCL', 'DTS', 'DRO', 'D2O', 'DWS', 'E2M', 'EHH', 'EM2', 'EAR',
                                         'EGA', 'EAI', 'EGI', 'ELX', 'ELS', 'EPD', 'EMV', 'EAX', 'ERA', 'EVS', 'EGH',
                                         'EMN', 'EVO', 'EXP', 'FZO', 'FRM', 'FTZ', 'FWD', 'FXL', 'FLC', 'FOR', 'FLN',
                                         'GMV', 'GLN', 'GAP', 'GLL', 'GAL', 'GSS', 'GNX', 'GSW', 'GC1', 'GEV', 'GVF',
                                         'GNG', 'GPX', 'GTN', 'HAS', 'HAV', 'HZR', 'HLO', 'HMD', 'HRR', 'HXG', 'HIG',
                                         'HIL', 'HZN', 'HUO', 'HTA', 'IDT', 'IMD', 'IMF', 'IMC', 'IPD', 'IFN', 'IGE',
                                         'IRC', 'INR', 'IBC', 'ISU', 'ISD', 'JAN', 'JXT', 'JRV', 'K2F', 'KAR', 'KMD',
                                         'KTD', 'KGL', 'KNL', 'LSF', 'LBL', 'LCK', 'LAU', 'LNG', 'LVH', 'LVT', 'LPE',
                                         'LON', 'LOM', 'MAH', 'MNS', 'MAI', 'MMM', 'MYE', 'MCE', 'MAT', 'MXI', 'MEA',
                                         'MCP', 'MDC', 'MLX', 'MMI', 'MHJ', 'MX1', 'MOY', 'MIL', 'MRC', 'MIR', 'MNF',
                                         'MOD', 'MOE', 'MOC', 'MTO', 'MPW', 'MCA', 'MYQ', 'NSC', 'NTD', 'NMT', 'NEU',
                                         'NCZ', 'NEW', 'NWF', 'PIQ', 'QIP', 'QEM', 'QMS', 'QVE', 'RZI', 'RCE', 'RVR']
    return list(set(codes1))


def get_codes2():
    codes2 = get_codes1() + ['GPX', 'CD3', 'RHY', 'CXX', 'FLC', 'BWF', 'CWN', 'CYL', 'IPL', 'MAQ', 'AFA', 'QVE', 'HMD',
                             'TLG', 'GGG', 'MXC', 'GSS', 'CVF', 'URW', 'E2M', 'ESV', 'TDO', 'CXM', 'NWF', 'RAP', 'CLH',
                             'GBE', 'AVH', 'COO', 'ATU', 'HUO', 'FZR', 'FXL', 'NML', 'BLX', 'RRL', 'RYD', 'EBG', 'BAL',
                             'ANP', 'NTU', 'D2O', 'BYI', 'BGA', 'PNI', 'A4N', 'EEG', 'IFN', 'VRL', 'RVR', 'BOQ', 'WAM',
                             'MOC', 'TON', 'WOR', 'IMD', 'QMS', 'RBL', 'CAA', 'GAP', 'GLE', 'AFI', 'CRL', 'AUQ', 'TEK',
                             'SIO', 'CPU', 'SM1', 'IMF', 'MOD', 'NET', 'MAI', 'GVF', 'AVJ', 'SWK', 'RSG', 'ASP', 'CGA',
                             'AUB', 'MCP', 'HUB', 'MEI', 'TPS', 'MYL', 'EVS', 'RCE', 'RBR', 'AAC', 'GNX', 'WSI', 'OSH',
                             'ACQ', 'NEW', 'BAP', 'CGO', 'IKE', 'KLO', 'TTA', 'BSL', 'LPD', 'AEI', 'VML', 'AER', 'SFR',
                             'BCC', 'FEX', 'DMP', 'KAR', 'APC', 'PTM', 'CLI', 'FMS', 'VAH', 'REG', 'ARU', 'LAU', 'MZZ',
                             'VMY', 'STM', 'HIL', 'HCT', 'APW', 'GGE', 'EGH', 'VLS', 'LBL', 'SDV', 'BBX', 'CTD', '3PL',
                             'MIR', 'FLT', 'FWD', 'TGG', 'DWS', 'EHH', 'KTD', 'KZR', 'CKA', 'CBY', 'SLK', 'BUX', 'WBA',
                             'CNW', 'GNC', 'LTR', 'API', 'IBC', 'TFL', 'ATC', 'RES', 'HZR', 'EGI', 'CXL', 'KKL', 'IPB',
                             'UNV', 'EAX', 'MRN', 'SIQ', 'SNL', '14D', 'MIN', 'BBL', 'MMS', 'GTN', 'CP1', 'PDL', 'CGR',
                             'GSN', 'MEP', 'FEI', 'YAL', 'TMZ', 'NAC', 'BRL', 'NMT', 'VTG', 'NOX', 'HMX', 'AHY', 'FRN',
                             'HCH', 'GRB', 'N1H', 'RIC', 'DEV', 'A2B', 'PM1', 'MEY', 'NSB', 'MHJ', 'DCL', 'CR1', 'DXB',
                             'WEL', 'AIR', 'CD2', 'BCN', 'SOL', 'LAW', 'S2R', 'CAY', 'PLS', 'EAI', 'GFL', 'AMG', 'EMB',
                             'TPM', 'QIP', 'RXP', 'WNR', 'VMX', 'AOP', 'KOR', 'BAF', 'WZR', 'FFC', 'GUL', 'FSF', 'CYB',
                             'MXR', 'CTE', 'THC', 'CDD', 'EHX', 'VMT', 'CAI', 'SMP', 'YOJ', 'SIG', 'AWY', 'ACR', 'ABX',
                             'CFO', 'MOB', 'GEV', 'KNM', 'DFM', 'TGF', 'ELD', 'ARN', 'FAR', 'ABC', 'SGR', 'TNY', 'LVT',
                             'CAZ', 'WHK', 'COG', 'GUD', 'REY', 'BST', 'SRG', 'NOV', 'DBF', 'BMG', 'VXR', 'RNU', 'HAS',
                             'ELX', 'K2F', 'LNY', 'CSS', 'MMM', 'ZGL', 'CMC', 'CML', 'QEM', 'IFL', 'HNG', 'ADN', 'EM1',
                             'WPP', 'BYE', 'GC1', 'RDF', 'CLX', 'CAP', 'GAS', 'HTA', 'CIE', 'BGH', 'LCK', 'DCC', 'AVW',
                             'RCT', 'KMD', 'MCA', 'VN8', 'SHJ', 'SPX', '1ST', 'XST', 'JXT', 'SNZ', 'VRM', 'IEC', 'CYG',
                             'ZMI', 'VAN', 'NZK', 'DTS', 'SMX', 'AUH', 'FTT', 'RNO', 'SM8', 'LSF', 'MEA', 'BIS', 'NSE',
                             'WSA', 'BPP', 'AHN', 'VAL', 'SLM', 'IVZ', 'FPL', 'CXU', 'ELT', 'DW8', 'RTE', 'SEI', 'FTC',
                             'ARX', 'GLL', 'DDT', 'CDM', 'SKF', 'DKM', 'APL', 'ORE', '4DS', 'GBG', 'BLY', 'CUX', 'CTM',
                             'EMP', 'AIZ', 'DRE', 'ZER', 'AKN', 'BOL', 'RMG', 'AV1', 'CIO', 'ADR', 'SVY', 'EN1', 'RTR',
                             'NGE', 'NCC', 'CLZ', 'ISU', 'MNC', 'GLA', 'HAW', 'ROG', 'CG1', 'BD1', 'WND', 'AQX', 'MLS',
                             'CT1', 'IRD', 'ANL', 'LRS', 'LEG', 'AJX', 'NSC', 'MRC', 'ZNO', 'HOT', 'VMG', 'LBT', 'IDT',
                             'SOP', 'EER', 'ADD', 'TGN', 'MOQ', 'HLA', 'IME', 'DTR', 'NTI', 'MNF', 'AHX', 'SKN', 'ALF',
                             'SRO', '9SP', 'CHZ', 'THD', 'ST1', 'NCZ', 'NOR', 'NWE', 'BIN', 'MSI', 'SVT', 'DRO', 'WHC',
                             'AGD', 'KRX', 'TNG', 'SWM', 'SER', 'ABV', 'SUD', 'AQC', 'DGR', 'FLN', 'LIO', 'MRQ', 'TOP',
                             'VLT', 'AGI', 'RDM', 'EMV', 'GPP', 'RDH', 'IP1', 'BDC', 'MHC', 'NSX', 'WBE', 'LRT', 'KPO',
                             'AUL', 'CZN', 'AO1', 'AYR', 'BCK', 'IVO', 'HPR', 'MGT', 'HWK', 'ANG', 'HYD', 'FYI', 'WAT',
                             'COI', 'T3D', 'MTH', 'MDC', 'AMP', 'CHN', 'ICG', 'CLA', 'TRS', 'MRL', 'MEU', 'TRM', 'HLO',
                             'LKE', 'SRZ', 'AUP', 'ATR', 'SNS', 'RHT', 'MRV', 'XTE', 'DDD', 'APG', 'TMK', 'UBI', 'PUA',
                             'AGE', 'HZN', 'ABL', 'FHS', 'ARM', 'SEN', 'FTZ', 'SRK', 'CAD', 'ZNC', 'AUT', 'MAH', 'ICT',
                             'FEL', 'AWV', 'CYP', 'DHR', 'EGA', 'NME', 'TAM', 'TRY', 'SPZ', 'MSG', 'BEM', 'HNR', 'ECL',
                             'BRB', 'VAR', 'LKO', 'BSX', 'EXR', 'BEL', 'QTM', 'LCY', 'NVA', 'NCL', 'LML', 'ICI', 'RVS',
                             'SHK', 'EGY', 'GOO', 'AOA', 'LOM', 'DSE', 'CAF', 'IAM', 'TOU', 'TPE', 'FFG', 'LSH', 'DTM',
                             'E25', 'FOR', 'SGQ', 'EAR', 'AJC', 'RWC', 'TEG', 'TOE', 'AGJ', 'CVL', 'CPV', 'TPD', 'DGO',
                             'KTA', 'ATH', 'LNK', 'NTD', 'EMU', 'PIQ', 'IMM', 'NEU', 'ERA', 'BEE', 'BAU', 'TER', 'BOA',
                             'EPM', 'GID', 'AAR', 'KBC', 'LSA', 'JAN', 'TRL', 'MTB', 'TSL', 'EVO', 'URF', 'EVE', 'COY',
                             'ALG', 'SDX', 'EUR', 'HRN', 'SI6', 'FAM', 'ADV', 'TMX', 'NVX', 'CTP', 'RKN', 'SXE', 'AYZ',
                             'ENT', 'MGL', 'HRR', 'WOA', 'CAJ', 'CVW', 'TNT', 'DAU', 'VMS', 'GNG', 'SND', 'AEG', 'INR',
                             'GPR', 'AYS', 'ZLD', 'ARQ', 'CAN', 'CGN', 'UNL', 'AKP', 'AAP', 'SFG', 'GMC', 'BSR', 'MOE',
                             'MPP', 'CCJ', 'CPH', 'IVX', 'C6C', 'TTL', 'CA8', 'MAT', 'AWN', 'DME', 'RZI', 'KNL', 'BOE',
                             'BYH', 'ICN', 'FNT', 'DVL', 'CDV', 'MCE', 'SGH', 'MEL', 'SXY', 'SKT', 'DTI', 'SAU', 'MSR',
                             'NVU', 'XTD', 'EX1', 'TIA', 'NXM', 'MYE', 'CMD', 'MNW', 'IVQ', 'SMN', 'FE8', 'CSV', 'KIS',
                             'ATP', 'SRN', 'CM8', 'NHC', 'MHI', 'MAY', 'ATS', 'GTG', 'EMH', 'VRC', 'PVD', 'TBL', 'VMC',
                             'KGL', 'RMY', 'UCW', 'RCW', 'CXZ', 'DYL', 'ISD', 'CGF', 'AXI', 'STX', 'AJQ', 'LNU', 'SVL',
                             'FSG', 'EGN', 'EQE', 'AAU', 'TTT', 'JRV', 'GLB', 'ERL', 'LCD', 'ARO', 'A40', 'COB', 'KLH',
                             'BKL', 'CGC', 'HHY', 'LI3', 'FCC', 'MJC', 'EGL', 'BKY', 'BHL', 'AGS', 'MYX', 'MRP', 'SIH',
                             'GXY', '88E', 'SUP', 'KZA', 'TMR', 'DTZ', 'KSN', 'LIT', 'IBG', 'MSE', 'GMN', 'HAV', 'INP',
                             'NAM', 'AML', 'WRM', 'ENE', 'AJJ', 'EUC', 'TAO', 'RDS', 'MMI', 'MDI', 'VBS', 'CXO', 'BRK',
                             'GDG', 'EVZ', 'RXM', 'ARL', 'RNE', 'WHA', 'SE1', 'FZO', 'SP3', 'CCV', 'HXG', 'BUY', 'AVZ',
                             'BGS', 'MX1', 'TPC', 'SLZ', 'MGV', 'JAT', 'CRO', 'KPG', 'CRS', 'SMD', 'ACF', 'JCS', 'CGM',
                             'MCM', 'IRC', 'ASN', 'AOU', 'TNO', 'AVC', 'WMC', 'BFC', 'LRM', 'INV', 'CL8', 'NUF', 'MEM',
                             'LVH', 'TBH', 'EXP', 'MAM', 'PGH', 'AMN', 'LPE', 'IMU', 'ADO', 'BUG', 'LNG', 'RWD', 'ALT',
                             'AVA', 'ED1', 'AGR', 'UBN', 'MQR', 'BAT', 'WBT', 'WWI', 'ARD', 'ZIP', 'MTO', 'CSE', 'SGI',
                             'EHL', 'GME', 'IS3', 'AR9', 'CDY', 'FAU', 'GMV', 'AIB', 'ENX', 'GLH', 'SCU', 'GED', 'VKA',
                             'CZR', 'AKM', 'FIJ', 'TCN', 'ESK', 'RLC', 'RNT', 'SAN', 'GBP', 'KWR', 'AU8', 'TIN', 'ATX',
                             'AXT', 'EPD', 'BTC', 'TDL', 'HOR', 'ALY', 'CVV', 'AJM', 'MAG', 'AQD', 'SGC', 'TTI', 'DEG',
                             'TGA', 'FIN', 'TSN', 'CI1', 'VEN', 'TKL', 'A3D', 'NWC', 'ADJ', 'CDX', 'RLE', 'GMD', 'KKT',
                             'RHI', 'KIN', 'DEM', 'MXI', 'YBR', 'DVN', 'AHK', 'TMT', 'ADX', 'BLZ', 'IGE', 'CCA', 'SBM',
                             'MNS', 'KRR', 'THR', 'LHB', 'HIP', 'FGO', 'AMI', 'ESH', 'CLT', 'RGS', 'SXA', 'PGR', 'ESR',
                             'ENA', 'EWC', 'PSC', 'XPD', 'AZM', 'TPP', 'JAY', 'WGN', 'GGX', 'RNX', 'GAL', 'ROO', 'MKG',
                             'MPW', 'SFX', 'CAG', 'FBR', 'SBW', 'ADY', 'SES', 'WWG', 'BRI', 'BXN', 'EMN', 'LMG', 'AME',
                             'MIL', 'KAM', 'DAF', 'MRG', 'SEQ', 'TRT', 'BNR', 'TTM', 'EDE', 'AVL', 'AUC', 'HLX', 'RAN',
                             'DAV', 'AZY', 'RMX']
    return list(set(codes2))


dead_codes = ['IRL', 'KAI', 'SM9', 'BKM', 'LVE', 'TKF', 'TGS', 'INH', 'MOT', 'NMI', 'JKA', 'WSZ', 'BGR', 'XQL', 'SAY', 'EOR',
        'MZC', 'GSL', 'SF1', 'SAZ', 'AOW', 'IMK', 'PUU', 'AOR', 'ZOR', 'RT2', 'QIN', 'AOJ', 'LI4', 'NRO', 'SXB', 'TT7',
        'ELK', 'RT9', 'TES', 'QBC', 'KNH', 'MZA', 'ANW', 'FGF', 'QSS', 'MZI', 'RFB', 'AHZ', 'ZTA', 'SHU', 'ATA', 'PLC',
        'KOP', 'WSQ', 'SKY', 'HTB', 'CM1', 'MPZ', 'E88', 'DAM', 'XCL', 'IFX', 'CDU', 'NFN', 'D13', 'IMQ', 'STL', 'REK',
        'CU1', 'EGS', 'LC1', 'NIB', 'USR', 'TCO', 'KFW', 'IMG', 'SVH', 'PUZ', 'WSH', 'RUB', 'OGX', 'SAC', 'MBT', 'SKP',
        'FSI', 'BMH', 'AXP', 'CDG', 'RBX', 'BSN', 'DGF', 'GBI', 'CAS', 'NXR', 'CHU', 'IQ3', 'INB', 'IB8', 'KGM', 'CBL',
        'OXX', 'MIG', 'MBL', 'MZF', 'MEQ', 'CNX', 'LO1', 'DXA', 'RFE', 'MXU', 'B2Y', 'PKA', 'VRI', 'SBU', 'SFV', 'WSC',
        'AZT', 'ACL', 'EPA', 'AMO', 'VTH', 'SXX', 'DAZ', 'BPB', 'APV', 'IMX', 'QST', 'AIY', 'S3R', 'GFI', 'TTZ', 'LGR',
        'IBN', 'TRA', 'WFE', 'NIO', 'NIU', 'SDL', 'MLL', 'LTN', 'RNL', 'SSN', 'ANS', 'CD1', 'DMA', 'LMW', 'MZB', 'WEJ',
        'LCT', 'SAM', 'MIH', 'CLY', 'RTD', 'PUK', 'SAS', 'TNB', 'TMG', 'OOK', 'SBK', 'SVA', 'SGL', 'SHZ', 'MCH', 'GBA',
        'REZ', 'SS7', 'SIX', 'MZT', 'TB8', 'KIG', 'ZAM', 'FIG', 'FDX', 'ATB', 'CHJ', '360', 'GBM', 'KPC', 'WEF', 'VIA',
        'BHD', 'CCE', 'RF1', 'LI1', 'FCG', 'WLC', 'ENB', 'ABW', 'CSK', 'AXL', 'IXC', 'SMG', 'PUJ', 'RNY', 'GFS', 'AFT',
        'AOK', 'PCI', 'BMP', 'KRS', 'MMG', 'WSO', 'TNJ', 'WE1', 'ICB', 'IAN', 'KEB', 'AOL', 'RFC', 'TT9', 'GO2', 'JCI',
        'EMI', 'WEK', 'SGU', 'RT1', 'RTC', 'LTF', 'IMN', 'IDF', 'SCW', 'GPS', 'PES', 'PPZ', 'CU2', 'PEP', 'PUO', 'XVG',
        'MAX', 'NAJ', 'DAE', 'RCR', 'MGZ', 'JVG', 'LSX', 'TEX', 'AO3', 'TIH', 'RMM', 'RDA', 'VCD', 'MAR', 'IHR', 'JIP',
        'KP2', 'NAO', 'BPG', 'LHM', 'PUV', 'ECT', 'VPC', 'MBJ', 'BSP', 'RRS', 'ANV', 'INN', 'CTL', 'BBR', 'WPG', 'HDX',
        'LAA', 'VPG', 'AN1', 'TOZ', 'LI2', 'NAH', 'WEN', 'IOR', 'LCN', 'LAM', 'AO2', 'LSR', 'SUM', 'DA1', 'IMO', 'OEQ',
        'RVA', 'CSD', 'PUB', 'IPT', 'HOG', 'QFE', 'LIN', 'POB', 'IDH', 'XTV', 'LCE', 'MZN', 'LER', 'MDZ', 'AEB', 'NMM',
        'MZ2', 'LT1', 'OTR', 'DAQ', 'MZ1', 'HCS', 'MAS', 'AQM', 'WNS', 'HAR', 'CCZ', 'SRF', 'TNF', 'IOT', 'IEQ', 'IDJ',
        'HDY', 'SSF', 'PEL', 'BCL', 'POV', 'MPO', 'PER', 'KIK', 'TTS', 'PEU', 'WLF', 'MMR', 'STC', 'WSN', 'PUQ', 'CVT',
        'HMO', 'SBI', 'IAB', 'MHD', 'LI5', 'ACP', 'CIZ', 'ODN', 'GCN', 'SS6', 'POT', 'CEL', 'SSE', 'WEH', 'ZYB', 'AYG',
        'KMT', 'IND', 'KYK', 'SMT', 'LGO', 'ICU', 'TNH', 'CCB', 'MPX', 'QNB', 'NAF', 'CGB', 'MED', 'AJY', 'WSJ', 'WSD',
        'SYS', 'SCA', 'AYU', 'ANQ', 'NRM', 'KKO', 'HML', 'VIV']


def get_all_codes():
    codes2 = get_codes2()
    df = get_asx_df()
    all_codes = list(df['ASX code'].values)
    for code in codes2:
        if code in all_codes:
            all_codes.remove(code)
    return codes2 + all_codes


if __name__ == '__main__':
    df = get_asx_df()
    push_industry(df)
    push_company(df)
