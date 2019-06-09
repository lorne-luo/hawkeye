import io
import os
import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR
import config.settings.local as settings
from aws import dynamodb, dynamodb_batch_push

BATCH_LIMIT = 25

ts = TimeSeries(key=settings.ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='date')


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
    return list(get_asx_200_list()) + ['MOQ', '14D', 'TGP', 'TOT', '3PL', '5GN', '8CO', 'A2B', 'AEG', 'AX1', 'ACQ',
                                       'ACF', 'ACR', 'ADA', 'ADH', 'ADT', 'ANO', 'AV1', 'AML', 'AEI', 'AIS', 'AMN',
                                       'AGR', 'AGI', 'AIZ', 'AQG', 'LEP', 'AJX', 'ALK', 'AQZ', 'A40', 'A4N', 'ATC',
                                       'AGH', 'AJM', 'AMA', 'AYS', 'AMH', 'ABR', 'AS1', 'AB1', 'APL', 'APE', 'AHX',
                                       'APD', 'AOP', 'ATL', 'AR9', 'ARL', 'ARF', 'ALI', 'ARG', 'ARQ', 'AHY', 'ASH',
                                       'ATU', 'AUB', 'AIA', 'AD8', 'AU8', 'AMI', 'A3D', 'AC8', 'AMG', 'ASB', 'ANG',
                                       'AAC', 'ABX', 'AHF', 'AEF', 'AFG', 'AFI', 'ALF', 'AOF', 'AVG', 'ATS', 'AHG',
                                       'ASG', 'AVA', 'AVN', 'AVH', 'AVJ', 'AZS', 'BBN', 'BTI', 'BSE', 'BRL', 'BBX',
                                       'BCI', 'BLX', 'BCC', 'BFG', 'BGL', 'BLT', 'BKY', 'BFC', 'BID', 'BTH', 'BGT',
                                       'BNO', 'BGS', 'BKI', 'BC8', 'BKT', 'BLA', 'BAF', 'BLG', 'BDA', 'BOL', 'BOT',
                                       'BRB', 'BSA', 'BUB', 'BRU', 'BUX', 'BWX', 'BYE', 'CDM', 'CAN', 'CP1', 'CAY',
                                       'CAJ', 'CAA', 'CWX', 'CDV', 'CDD', 'CVN', 'CCV', 'CYL', 'CAT', 'CWP', 'CDY',
                                       'CTP', 'CXM', 'CNI', 'CIP', 'CMA', 'CFO', 'CHN', 'CIA', 'CQE', 'CCX', 'CL1',
                                       'CSS', 'CLQ', 'CVW', 'CPV', 'CAM', 'CUV', 'CLV', 'CGR', 'COB', 'CDA', 'CLH',
                                       'CKF', 'COI', 'CMP', 'CIE', 'COE', 'C6C', 'CRN', 'CYG', 'CRD', 'CPH', 'CSV',
                                       'CV1', 'CYP', 'DCN', 'DNK', 'DTL', 'DCG', 'DYL', 'DGR', 'DDR', 'DUI', 'DJW',
                                       'DCL', 'DTS', 'DN8', 'DRO', 'DUB', 'D2O', 'DWS', 'E2M', 'EHH', 'EM2', 'EAR',
                                       'EGA', 'ENN', 'EOS', 'EXL', 'EAI', 'EGI', 'ELX', 'ELS', 'EML', 'EPD', 'EMV',
                                       'EAX', 'ERA', 'EGG', 'EVS', 'EPW', 'EGH', 'EMN', 'EZL', 'EGD', 'EVT', 'EVO',
                                       'EXP', 'FZO', 'FRM', 'FTZ', 'FCT', 'FWD', 'FXL', 'FLC', 'FOR', 'FNP', 'FLN',
                                       'FDV', 'GMV', 'GLN', 'GAP', 'G1A', 'GLL', 'GAL', 'GBT', 'GDI', 'GSS', 'GNX',
                                       'GMA', 'GSW', 'GC1', 'GEV', 'GVF', 'GOR', 'GNG', 'GRR', 'GPX', 'GTN', 'HSN',
                                       'HAS', 'HAV', 'HZR', 'HM1', 'HE8', 'HLO', 'HMD', 'HRR', 'HXG', 'HFR', 'HIG',
                                       'HIL', 'HZN', 'HPI', 'HRL', 'HT1', 'HUO', 'HTA', 'ICQ', 'IDT', 'IMA', 'IMD',
                                       'IMF', 'IMC', 'IPD', 'IFN', 'IFM', 'INA', 'IDX', 'IGE', 'IRI', 'IRC', 'INR',
                                       'IBC', 'ISU', 'ISD', 'ISX', 'IGL', 'JAL', 'JAN', 'JHC', 'JXT', 'JRV', 'JLG',
                                       'JIN', 'JMS', 'K2F', 'KLL', 'KAR', 'KMD', 'KTD', 'KGL', 'KNL', 'KDR', 'KSL',
                                       'KCN', 'KSS', 'KGN', 'LSF', 'LBL', 'LEX', 'LGD', 'LCK', 'LIC', 'LAU', 'LNG',
                                       'LPI', 'LVH', 'LVT', 'LPE', 'LCM', 'LON', 'LOV', 'LOM', 'MLD', 'M7T', 'MAH',
                                       'MGG', 'MAU', 'MNS', 'MAI', 'MMM', 'MYE', 'MCE', 'MAT', 'MXI', 'MFD', 'MEA',
                                       'MXT', 'MCP', 'MVP', 'MDC', 'MML', 'MP1', 'MEZ', 'MSB', 'MLX', 'MMI', 'MFF',
                                       'MGC', 'MHJ', 'MX1', 'MWY', 'MOY', 'MIL', 'MLT', 'MCR', 'MRC', 'MIR', 'MRM',
                                       'MNF', 'MOD', 'MOE', 'MA1', 'MVF', 'MNY', 'MOC', 'MTO', 'MGX', 'MPW', 'MCA',
                                       'MYR', 'MYQ', 'MYS', 'NSC', 'NTD', 'NVL', 'NGI', 'NBI', 'NEA', 'NMT', 'NTC',
                                       'NWL', 'NEU', 'NCZ', 'NEW', 'NWF', 'NCK', 'NIC', 'NBL', 'PFP', 'PIQ', 'PTB',
                                       'PPH', 'PWH', 'QIP', 'QEM', 'QMS', 'QVE', 'RZI', 'RMS', 'RCE', 'RED', 'RVR']


def get_codes2():
    return get_codes1() + ['RBL', 'RDC', 'REH', 'REG', 'RAP', 'RMC', 'RHT', 'RFG', 'RVS', 'RNO', 'RHP', 'RHY', 'RIC',
                           'RMY', 'RGI', 'RUL', 'RFF', 'RHL', 'RXP', 'SO4', 'SCT', 'SDI', 'SLK', 'SMX', 'SHV', 'SWF',
                           'SXY', 'SNS', 'SE1', 'SRV', 'SSM', 'SGF', 'SSG', 'SFX', 'SBW', 'SHJ', 'SHM', 'SLX', 'SIV',
                           'SLR', 'SKT', 'SKF', 'SPZ', 'SMP', 'SIL', 'SXE', 'STW', 'SP3', 'SEC', 'ST1', 'SRG', 'SGQ',
                           'SMR', 'SPL', 'GAS', 'SVY', 'STA', 'SMN', 'SDG', 'SLC', 'SWK', 'SW1', 'SM1', 'TLG', 'TFL',
                           'TMT', 'TLX', 'TPW', 'TGG', 'TMR', 'TER', 'THC', 'CGL', 'TRS', 'VMX', 'VAN', 'VLT', 'VEE',
                           'VXR', 'VMC', 'VG1', 'VLW', 'VRL', 'VEN', 'VAH', 'VRT', 'VTG', 'VMT', 'VHT', 'VN8', 'WGN',
                           'WKT', 'WAM', 'WGB', 'WLE', 'WMI', 'WAX', 'WGO', 'WHA', 'WBA', 'WBT', 'WAF', 'WGX', 'WHK',
                           'WND', 'WNR', 'WWG', 'WZR', 'WPP', 'XIP', 'XF1', 'XRF', 'YOJ', 'ZGL', 'Z1P', 'ZNO', 'MEI',
                           'RDS', 'INP', 'MRP', 'CKA', 'IDZ', 'HSC', 'AVQ', '9SP', 'LBT', 'AVZ', 'CLI', 'AGS', 'ADR',
                           'BLZ', 'ALY', 'SHO', 'CFE', 'ICI', 'NXE', 'BSR', 'VRC', 'APC', 'SCU', 'AD1', 'NTI', 'BDC',
                           'SGI', 'AUZ', 'KSN', 'EN1', 'ACB', 'RAC', 'AAU', 'ENR', 'BXN', 'GSN', 'PSC', 'FUN', 'DOR',
                           'IVZ', 'BCK', 'RGL', 'CNJ', 'ASN', 'PUR', 'MEP', 'INF', 'JHL', 'IHR', 'CAP', 'LKE', 'SPX',
                           'CNW', 'SIS', 'ARV', 'STX', 'MGU', '1ST', 'DVL', 'RDM', 'TAS', 'ASP', 'GBG', 'AHQ', 'ARS',
                           'CAF', 'MTC', 'NVU', 'KAS', 'STM', 'ESR', 'IME', 'AQD', 'ACL', 'MSG', 'SIH', 'EMR', 'EUR',
                           'MAY', 'AAR', 'NNW', 'HNR', 'TLM', 'SRZ', 'FYI', 'AZM', 'BIQ', 'COG', 'DEV', 'GGG', 'DXN',
                           'BPP', 'SVM', 'FMS', 'MXR', 'AXT', 'AME', 'MEL', 'SES', 'CRB', 'AUR', 'RFT', 'SEN', 'FHS',
                           'AQI', 'DNA', 'SOP', 'VRS', 'AEV', 'EUC', 'IMU', 'SVL', 'ADO', 'CUL', 'BMG', 'TAM', 'MPR',
                           'IBX', 'AHN', 'MZI', 'EHX', 'SDV', 'FFG', 'BCT', 'LER', 'AJL', '1AG', 'CAE', 'RWD', 'EEG',
                           'HMX', '88E', 'TPP', 'PUA', 'KTA', 'ICN', 'ARD', 'CE1', 'CXX', 'QTM', 'AGY', 'DCC', 'XTD',
                           'HLX', 'BCB', 'EM1', 'SGC', 'LAW', 'AFR', 'G88', 'PM1', 'IVX', 'CAZ', 'CZR', 'CWL', 'AJQ',
                           'ATP', 'YBR', 'CUE', 'SVD', 'VTI', 'MYL', 'LNU', 'FSG', 'RXM', 'GOO', 'BRN', 'ARM', 'RGS',
                           'DRX', 'VRM', 'IP1', 'KYK', 'IHL', 'GTR', 'MSV', 'SRS', 'ECT', 'WML', 'GWR', 'QHL', 'NML',
                           'MRG', 'ZNC', 'IPB', 'FIN', 'B2Y', 'ESH', 'ANW', 'ERX', 'KNM', 'COO', 'RFX', 'EGL', 'KOR',
                           'SUP', 'ADY', 'KPO', 'ACW', 'ALC', 'ESE', 'ABT', 'GID', 'ARE', 'AIY', 'AQX', 'CZL', 'MEB',
                           'LCT', 'CRL', 'SBB', 'REF', 'RCP', 'AWY', 'ICT', 'EXR', 'S2R', 'LSH', 'ERM', 'IEC', 'RLE',
                           'ROO', 'TNT', 'TBH', 'AHZ', 'AKM', 'FEX', 'EWC', 'RBR', 'GMN', 'ESV', 'SYA', 'AL8', 'BMN',
                           'RTG', 'CHZ', 'BIT', 'RNE', 'GRB', 'CCG', 'PVD', 'DXB', 'WEL', 'KFE', 'GTG', 'CGN', 'GPR',
                           'CLA', 'JAT', 'DTI', 'EDE', 'TAP', 'VKA', 'MGV', 'FBR', 'BDG', 'MNW', 'SXA', 'IMM', 'GML',
                           'BPL', 'MBM', 'CMM', 'MEY', 'MXC', 'RNT', 'SFG', 'MOB', 'AZY', 'CVV', 'CZI', 'GIB', 'AON',
                           'BSX', 'RAN', 'MEM', 'ATH', 'PPL', 'MOH', 'CMC', 'KRR', 'MGL', 'INK', 'DSE', 'JCS', 'BRK',
                           'GBR', 'LIT', 'AVL', 'CXO', 'CCA', 'XPD', 'RTR', 'AXP', 'BAR', 'KMT', 'N27', 'BD1', 'ARU',
                           'BCN', 'SLZ', 'FDM', 'ANP', 'MLM', 'RDG', 'HGO', 'TNO', 'HAW', 'WNB', 'AUQ', '4DS', 'VMY',
                           'RNU', 'NXM', 'LEG', 'BEE', 'KNO', 'SRK', 'KRM', 'FEL', 'MJC', 'MEU', 'SVT', 'DMG', 'LTR',
                           'NTU', 'WMC', 'NWC', 'IOD', 'SGO', 'WLD', 'BEM', 'HCH', 'AUC', 'WEC', 'PSZ', 'MDR', 'TDO',
                           'IGN', 'XAM', 'VRX', 'KP2', 'DEG', 'ENA', 'BLU', 'EMU', 'GCY', 'LPD', 'SEI', 'CM8', 'AZV',
                           'AXE', 'ABV', 'LCD', 'ADJ', 'KIS', 'BOE', 'CAI', 'SAS', 'GMR', 'RMG', 'GMD', 'CI1', 'DTZ',
                           'BUD', 'HYD', 'FOD', 'RMP', 'SIT', 'NAG', 'NET', 'GED', 'BAT', 'LAA', 'HPR', 'SKN', 'VMS',
                           'YOW', 'KIN', 'IBG', 'VIV', 'FAR', 'SOR', 'CDX', 'ZLD', 'FRN', 'AMD', 'SM8']


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
