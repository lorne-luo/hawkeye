import io
import os
import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR
import settings
from aws import dynamodb, dynamodb_batch_push

BATCH_LIMIT = 25

ts = TimeSeries(key=settings.ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='date')


def get_asx_df():
    asx_url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    asx_data = requests.get(asx_url).content
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1)

    return asx_df




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


if __name__ == '__main__':
    df = get_asx_df()
    push_industry(df)
    push_company(df)


codes1 = ['MOQ', '14D', '1ST', 'TGP', 'TOT', 'TDO', '3PL', '4DS', '5GN',
          '8CO', '9SP', 'NNW', 'ACB', 'A2B', 'ABP', 'AEG', 'ABT', 'AX1',
          'ACQ', 'ACF', 'ACR', 'ADA', 'ADH', 'ABC', 'ADR', 'AHZ', 'ADT',
          'ADJ', 'ANO', 'AV1', 'AML', 'AEI', 'AIS', 'APT', 'AGL', 'AMN',
          'AGR', 'AGI', 'AIZ', 'AXP', 'AJL', 'AQG', 'AUQ', 'ALC', 'AL8',
          'LEP', 'AJX', 'AQI', 'ALK', 'AHQ', 'AQZ', 'A40', 'AGS', 'A4N',
          'ALQ', 'ARS', 'ATC', 'ATH', '1AG', 'AGH', 'ALU', 'AME', 'AJM',
          'AWC', 'AMA', 'AYS', 'AMH', 'AMC', 'ABR', 'AMP', 'AS1', 'AAR',
          'AB1', 'ANN', 'ASN', 'APL', 'ANP', 'APE', 'APA', 'AHX', 'APD',
          'AOP', 'AON', 'ATL', 'APX', 'ARU', 'ARB', 'AXE', 'AR9', 'ARL',
          'ALG', 'ARF', 'ALI', 'ARG', 'AGY', 'ALL', 'AJQ', 'ARQ', 'ARV',
          'AHY', 'ASH', 'ASX', 'ALX', 'ATU', 'AUB', 'AIA', 'AD8', 'AU8',
          'AMI', 'AUR', 'AZJ', 'A3D', 'AC8', 'ASL', 'AMG', 'AST', 'ASB',
          'ANG', 'ANZ', 'AAC', 'ABX', 'AHF', 'AEF', 'AFG', 'AFI', 'ALF',
          'API', 'APC', 'AOF', 'AVG', 'AWY', 'ATS', 'AIY', 'AHG', 'ASG',
          'AVA', 'AVN', 'AOG', 'AVH', 'AVJ', 'AVZ', 'AVQ', 'AZV', 'AZS',
          'BBN', 'BTI', 'BOQ', 'BMN', 'BAP', 'BDC', 'BAR', 'BSE', 'BRL',
          'BAT', 'BBX', 'BCI', 'BPT', 'BLX', 'BCC', 'BGA', 'BFG', 'BAL',
          'BGL', 'BEN', 'BLT', 'BKY', 'BFC', 'BHP', 'BID', 'BTH', 'BIN',
          'BGT', 'BNO', 'BIT', 'BGS', 'BKI', 'BC8', 'BDG', 'BKT', 'BEM',
          'BKL', 'BSX', 'BLU', 'BLA', 'BAF', 'BCT', 'BSL', 'BLG', 'BDA',
          'BOL', 'BLD', 'BOE', 'BOT', 'B2Y', 'BCB', 'BRN', 'BXB', 'BVS',
          'BRB', 'BRG', 'BKW', 'BCK', 'BEE', 'BSA', 'BUB', 'BUD', 'BIQ',
          'BRU', 'BUX', 'BWP', 'BWX', 'BYE', 'CDM', 'CAI', 'CE1', 'CTX',
          'CAN', 'CP1', 'CAY', 'CAJ', 'CAA', 'CMM', 'CVV', 'CWX', 'CRB',
          'CDX', 'CDV', 'CDD', 'CVN', 'CAP', 'CAR', 'CCV', 'CZI', 'CYL',
          'CAT', 'CAZ', 'CWP', 'CDY', 'CLA', 'CTP', 'CAF', 'CXM', 'CNI',
          'CIP', 'CMA', 'CFO', 'CHN', 'CGF', 'CIA', 'CCA', 'CWL', 'CQE',
          'CHC', 'CLW', 'CQR', 'CHZ', 'CNU', 'CIM', 'CNW', 'CCX', 'CL1',
          'CSS', 'CLQ', 'CWY', 'CVW', 'CPV', 'CAM', 'CUV', 'CLV', 'CGR',
          'COB', 'CCL', 'COH', 'CDA', 'CKA', 'COL', 'CLH', 'CKF', 'CRL',
          'COI', 'CBA', 'CCG', 'CMP', 'CPU', 'COG', 'CIE', 'COE', 'C6C',
          'CXO', 'CRN', 'CTD', 'COO', 'CGC', 'CYG', 'CXX', 'CRD', 'CCP',
          'CPH', 'CMW', 'CLI', 'CWN', 'CSV', 'CSL', 'CSR', 'CUE', 'CV1',
          'CYB', 'CYP', 'DCN', 'DNK', 'DTL', 'DEG', 'DCG', 'DYL', 'DEV',
          'DXS', 'DGR', 'DDR', 'DCC', 'DXB', 'DUI', 'DJW', 'DCL', 'DHG',
          'DMP', 'DNA', 'DOR', 'DVL', 'DTZ', 'DOW', 'DTS', 'DN8', 'DRO',
          'DSE', 'DTI', 'DUB', 'DLX', 'D2O', 'DWS', 'E2M', 'EHH', 'EM2',
          'EAR', 'ECX', 'EDE', 'EGA', 'EHX', 'ENN', 'ELD', 'EOS', 'EXL',
          'EXR', 'EAI', 'EGI', 'ELX', 'ELS', 'EHL', 'EMR', 'EML', 'ERM',
          'EPD', 'EMU', 'EMV', 'ENR', 'EAX', 'ERA', 'EWC', 'EGG', 'EN1',
          'ENA', 'EGL', 'EVS', 'EPW', 'ESV', 'EHE', 'EGH', 'EMN', 'EUC',
          'EUR', 'EZL', 'EGD', 'EVT', 'EVN', 'EVO', 'ERX', 'EXP', 'FZO',
          'FAR', 'FRM', 'FBR', 'FEX', 'FTZ', 'FCT', 'FPH', 'FWD', 'FBU',
          'FXL', 'FLT', 'FMS', 'FLC', 'FOR', 'FMG', 'FNP', 'FDM', 'FLN',
          'FDV', 'FUN', 'FYI', 'GMV', 'GUD', 'GEM', 'GRB', 'GLN', 'GXY',
          'GAP', 'G1A', 'GLL', 'GAL', 'GCY', 'GBT', 'GDI', 'GMD', 'GSS',
          'GNX', 'GMA', 'GSW', 'GID', 'GIB', 'GBG', 'GC1', 'GEV', 'GVF',
          'GMN', 'GOR', 'GED', 'G88', 'GMG', 'GOO', 'GPT', 'GNG', 'GNC',
          'GRR', 'GPX', 'GBR', 'GSN', 'GGG', 'GOZ', 'GTN', 'GWA', 'GWR',
          'HMX', 'HSN', 'HVN', 'HAS', 'HAV', 'HAW', 'HZR', 'HLS', 'HSO',
          'HM1', 'HE8', 'HLO', 'HMD', 'HRR', 'HXG', 'HPR', 'HFR', 'HIG',
          'HGO', 'HIL', 'HZN', 'HCH', 'HPI', 'HRL', 'HT1', 'HUB', 'HUO',
          'HTA', 'HYD', 'ICI', 'ICQ', 'ICT', 'IEL', 'IDT', 'IGN', 'ILU',
          'IMA', 'IBX', 'IMD', 'IME', 'IMF', 'IMC', 'IMM', 'IPD', 'IHL',
          'INP', 'IPL', 'INK', 'IGO', 'IFN', 'INF', 'IFM', 'INA', 'ING',
          'IAG', 'IDX', 'IGE', 'IRI', 'IHR', 'IRC', 'IVZ', 'IVX', 'IVC',
          'IOD', 'INR', 'IFL', 'IPB', 'IPH', 'IRE', 'IBC', 'IBG', 'ISU',
          'ISD', 'ISX', 'IGL', 'JHX', 'JAL', 'JAN', 'JHG', 'JHC', 'JAT',
          'JXT', 'JHL', 'JBH', 'JCS', 'JRV', 'JLG', 'JIN', 'JMS', 'K2F',
          'KPO', 'KLL', 'KAR', 'KAS', 'KMD', 'KTD', 'KGL', 'KNL', 'KDR',
          'KIN', 'KSL', 'KIS', 'KRR', 'KCN', 'KRM', 'KSS', 'KNM', 'KNO',
          'KGN', 'KFE', 'KOR', 'KP2', 'KTA', 'KYK', 'LSF', 'LKE', 'LBL',
          'LAA', 'LAW', 'LBT', 'LER', 'LEX', 'LGD', 'LEG', 'LCK', 'LLC',
          'LPD', 'LSH', 'LIC', 'LAU', 'LNU', 'LNK', 'LTR', 'LNG', 'LIT',
          'LPI', 'LVH', 'LVT', 'LCT', 'LPE', 'LCM', 'LON', 'LOV', 'LOM',
          'LYC', 'MLD', 'M7T', 'MAH', 'MRP', 'MQG', 'MFG', 'MGG', 'MAU',
          'MNS', 'MGU', 'MGL', 'MAI', 'MEY', 'MMM', 'MYE', 'MCE', 'MAT',
          'MXR', 'MXI', 'MFD', 'MYX', 'MEA', 'MMS', 'MXT', 'MCP', 'MDR',
          'MPL', 'MVP', 'MDC', 'MML', 'MP1', 'MJC', 'MEM', 'MEZ', 'MSB',
          'MLX', 'MTS', 'MEL', 'MMI', 'MFF', 'MGC', 'MXC', 'MHJ', 'MX1',
          'MWY', 'MOY', 'MIL', 'MLT', 'MCR', 'MRC', 'MIN', 'MEP', 'MNW',
          'MIR', 'MGR', 'MSV', 'MRM', 'MNF', 'MBM', 'MOB', 'MOD', 'MOE',
          'MOH', 'MND', 'MA1', 'MVF', 'MNY', 'MOC', 'MTO', 'MGX', 'MPR',
          'MPW', 'MCA', 'MRG', 'MGV', 'MYL', 'MYR', 'MYQ', 'MYS', 'NAG',
          'NAN', 'NVU', 'NSC', 'NAB', 'NSR', 'NTD', 'NVL', 'NML', 'NGI',
          'NVT', 'NBI', 'NEA', 'NMT', 'NTC', 'NET', 'NWL', 'NEU', 'NCZ',
          'NXE', 'NEW', 'NHC', 'NCM', 'NWF', 'NWS', 'NXT', 'NXM', 'NHF',
          'NCK', 'NIC', 'NEC', 'NBL', 'N27', 'NTU', 'PFP', 'PIQ', 'PSZ',
          'PTB', 'PUA', 'PPH', 'PWH', 'QAN', 'QIP', 'QBE', 'QEM', 'QMS',
          'QTM', 'QUB', 'QHL', 'QVE', 'RAC', 'RZI', 'RMS', 'RHC', 'RAN',
          'REA', 'RLE', 'RCE', 'RFT', 'RED', 'RDM', 'RVR', 'RBL', 'RDC',
          'RFX', 'REH', 'RGS', 'REG', 'RRL', 'RWC', 'RNU', 'RNT', 'RNE',
          'RAP', 'RMC', 'RMD', 'RSG', 'RHT', 'RDG', 'RFG', 'RVS', 'REF',
          'RWD', 'RXM', 'RNO', 'RHP', 'RHY', 'RIC', 'RIO', 'RGL', 'RMY',
          'ROO', 'RGI', 'RUL', 'RTG', 'RTR', 'RFF', 'RHL', 'RXP', 'S2R',
          'SGC', 'SO4', 'SFR', 'STO', 'SAR', 'SCG', 'SDV', 'SCT', 'SDI',
          'SFG', 'SLK', 'SES', 'SMX', 'SEK', 'SHV', 'SWF', 'SEN', 'SXY',
          'SNS', 'SE1', 'SRV', 'SSM', 'SVW', 'SWM', 'SGF', 'SSG', 'SFX',
          'SBW', 'SHJ', 'SCP', 'SHM', 'SIG', 'SLX', 'SIV', 'SLR', 'SVL',
          'SIS', 'SGM', 'SIT', 'SKN', 'SAS', 'SKT', 'SKC', 'SKF', 'SM8',
          'SPZ', 'SIQ', 'SMP', 'SIL', 'SHL', 'S32', 'SXE', 'SXL', 'SVM',
          'SKI', 'SPK', 'STW', 'SEI', 'SPX', 'SP3', 'SDA', 'SEC', 'SRS',
          'ST1', 'SHO', 'SRG', 'SBM', 'SGQ', 'SMR', 'SPL', 'GAS', 'SVY',
          'SDF', 'SGI', 'SGP', 'STA', 'SXA', 'SOR', 'STX', 'SRK', 'SMN',
          'SLZ', 'SUN', 'SDG', 'STM', 'SUL', 'SUP', 'SLC', 'SWK', 'SW1',
          'SYD', 'SOP', 'SM1', 'SYR', 'TAH', 'TLG', 'TLM', 'TAM', 'TNO',
          'TAP', 'TFL', 'TAS', 'TGR', 'TMT', 'TNE', 'TLX', 'TLS', 'TPW',
          'TGG', 'TPP', 'TMR', 'TER', 'TNT', 'THC', 'A2M', 'TBH', 'CGL',
          'DXN', 'FOD', 'TRS', 'SGR', 'VMX', 'VAN', 'VLT', 'VEE', 'VMS',
          'VXR', 'VMC', 'VRM', 'VRS', 'VG1', 'VCX', 'VLW', 'VRL', 'VMY',
          'VEN', 'VAH', 'VRT', 'VTI', 'VTG', 'VEA', 'VVR', 'VIV', 'VMT',
          'VOC', 'VHT', 'VN8', 'VRX', 'WGN', 'WKT', 'WAM', 'WGB', 'WLE',
          'WMI', 'WAX', 'WGO', 'SOL', 'WHA', 'WEB', 'WBA', 'WBT', 'WLD',
          'WES', 'WAF', 'WSA', 'WGX', 'WBC', 'WEC', 'WHC', 'WHK', 'WEL',
          'WND', 'WNR', 'WTC', 'WWG', 'WZR', 'WPL', 'WOW', 'WML', 'WOR',
          'WPP', 'XAM', 'XIP', 'XRO', 'XF1', 'XRF', 'XTD', 'YBR', 'YOJ',
          'YOW', 'ZLD', 'ZNC', 'ZGL', 'Z1P', 'ZNO']

codes2 = ['MOQ', '14D', '1ST', 'TGP', 'TOT', 'TDO', '3PL', '4DS', '5GN',
          '8CO', '9SP', 'NNW', 'ACB', 'A2B', 'ABP', 'AEG', 'ABT', 'AX1',
          'ACQ', 'ACF', 'ACR', 'ADA', 'ADH', 'ABC', 'ADR', 'AHZ', 'ADT',
          'ADJ', 'ANO', 'AV1', 'AML', 'AEI', 'AIS', 'APT', 'AGL', 'AMN',
          'AGR', 'AGI', 'AIZ', 'AXP', 'AJL', 'AQG', 'AUQ', 'ALC', 'AL8',
          'LEP', 'AJX', 'AQI', 'ALK', 'AHQ', 'AQZ', 'A40', 'AGS', 'A4N',
          'ALQ', 'ARS', 'ATC', 'ATH', '1AG', 'AGH', 'ALU', 'AME', 'AJM',
          'AWC', 'AMA', 'AYS', 'AMH', 'AMC', 'ABR', 'AMP', 'AS1', 'AAR',
          'AB1', 'ANN', 'ASN', 'APL', 'ANP', 'APE', 'APA', 'AHX', 'APD',
          'AOP', 'AON', 'ATL', 'APX', 'ARU', 'ARB', 'AXE', 'AR9', 'ARL',
          'ALG', 'ARF', 'ALI', 'ARG', 'AGY', 'ALL', 'AJQ', 'ARQ', 'ARV',
          'AHY', 'ASH', 'ASX', 'ALX', 'ATU', 'AUB', 'AIA', 'AD8', 'AU8',
          'AMI', 'AUR', 'AZJ', 'A3D', 'AC8', 'ASL', 'AMG', 'AST', 'ASB',
          'ANG', 'ANZ', 'AAC', 'ABX', 'AHF', 'AEF', 'AFG', 'AFI', 'ALF',
          'API', 'APC', 'AOF', 'AVG', 'AWY', 'ATS', 'AIY', 'AHG', 'ASG',
          'AVA', 'AVN', 'AOG', 'AVH', 'AVJ', 'AVZ', 'AVQ', 'AZV', 'AZS',
          'BBN', 'BTI', 'BOQ', 'BMN', 'BAP', 'BDC', 'BAR', 'BSE', 'BRL',
          'BAT', 'BBX', 'BCI', 'BPT', 'BLX', 'BCC', 'BGA', 'BFG', 'BAL',
          'BGL', 'BEN', 'BLT', 'BKY', 'BFC', 'BHP', 'BID', 'BTH', 'BIN',
          'BGT', 'BNO', 'BIT', 'BGS', 'BKI', 'BC8', 'BDG', 'BKT', 'BEM',
          'BKL', 'BSX', 'BLU', 'BLA', 'BAF', 'BCT', 'BSL', 'BLG', 'BDA',
          'BOL', 'BLD', 'BOE', 'BOT', 'B2Y', 'BCB', 'BRN', 'BXB', 'BVS',
          'BRB', 'BRG', 'BKW', 'BCK', 'BEE', 'BSA', 'BUB', 'BUD', 'BIQ',
          'BRU', 'BUX', 'BWP', 'BWX', 'BYE', 'CDM', 'CAI', 'CE1', 'CTX',
          'CAN', 'CP1', 'CAY', 'CAJ', 'CAA', 'CMM', 'CVV', 'CWX', 'CRB',
          'CDX', 'CDV', 'CDD', 'CVN', 'CAP', 'CAR', 'CCV', 'CZI', 'CYL',
          'CAT', 'CAZ', 'CWP', 'CDY', 'CLA', 'CTP', 'CAF', 'CXM', 'CNI',
          'CIP', 'CMA', 'CFO', 'CHN', 'CGF', 'CIA', 'CCA', 'CWL', 'CQE',
          'CHC', 'CLW', 'CQR', 'CHZ', 'CNU', 'CIM', 'CNW', 'CCX', 'CL1',
          'CSS', 'CLQ', 'CWY', 'CVW', 'CPV', 'CAM', 'CUV', 'CLV', 'CGR',
          'COB', 'CCL', 'COH', 'CDA', 'CKA', 'COL', 'CLH', 'CKF', 'CRL',
          'COI', 'CBA', 'CCG', 'CMP', 'CPU', 'COG', 'CIE', 'COE', 'C6C',
          'CXO', 'CRN', 'CTD', 'COO', 'CGC', 'CYG', 'CXX', 'CRD', 'CCP',
          'CPH', 'CMW', 'CLI', 'CWN', 'CSV', 'CSL', 'CSR', 'CUE', 'CV1',
          'CYB', 'CYP', 'DCN', 'DNK', 'DTL', 'DEG', 'DCG', 'DYL', 'DEV',
          'DXS', 'DGR', 'DDR', 'DCC', 'DXB', 'DUI', 'DJW', 'DCL', 'DHG',
          'DMP', 'DNA', 'DOR', 'DVL', 'DTZ', 'DOW', 'DTS', 'DN8', 'DRO',
          'DSE', 'DTI', 'DUB', 'DLX', 'D2O', 'DWS', 'E2M', 'EHH', 'EM2',
          'EAR', 'ECX', 'EDE', 'EGA', 'EHX', 'ENN', 'ELD', 'EOS', 'EXL',
          'EXR', 'EAI', 'EGI', 'ELX', 'ELS', 'EHL', 'EMR', 'EML', 'ERM',
          'EPD', 'EMU', 'EMV', 'ENR', 'EAX', 'ERA', 'EWC', 'EGG', 'EN1',
          'ENA', 'EGL', 'EVS', 'EPW', 'ESV', 'EHE', 'EGH', 'EMN', 'EUC',
          'EUR', 'EZL', 'EGD', 'EVT', 'EVN', 'EVO', 'ERX', 'EXP', 'FZO',
          'FAR', 'FRM', 'FBR', 'FEX', 'FTZ', 'FCT', 'FPH', 'FWD', 'FBU',
          'FXL', 'FLT', 'FMS', 'FLC', 'FOR', 'FMG', 'FNP', 'FDM', 'FLN',
          'FDV', 'FUN', 'FYI', 'GMV', 'GUD', 'GEM', 'GRB', 'GLN', 'GXY',
          'GAP', 'G1A', 'GLL', 'GAL', 'GCY', 'GBT', 'GDI', 'GMD', 'GSS',
          'GNX', 'GMA', 'GSW', 'GID', 'GIB', 'GBG', 'GC1', 'GEV', 'GVF',
          'GMN', 'GOR', 'GED', 'G88', 'GMG', 'GOO', 'GPT', 'GNG', 'GNC',
          'GRR', 'GPX', 'GBR', 'GSN', 'GGG', 'GOZ', 'GTN', 'GWA', 'GWR',
          'HMX', 'HSN', 'HVN', 'HAS', 'HAV', 'HAW', 'HZR', 'HLS', 'HSO',
          'HM1', 'HE8', 'HLO', 'HMD', 'HRR', 'HXG', 'HPR', 'HFR', 'HIG',
          'HGO', 'HIL', 'HZN', 'HCH', 'HPI', 'HRL', 'HT1', 'HUB', 'HUO',
          'HTA', 'HYD', 'ICI', 'ICQ', 'ICT', 'IEL', 'IDT', 'IGN', 'ILU',
          'IMA', 'IBX', 'IMD', 'IME', 'IMF', 'IMC', 'IMM', 'IPD', 'IHL',
          'INP', 'IPL', 'INK', 'IGO', 'IFN', 'INF', 'IFM', 'INA', 'ING',
          'IAG', 'IDX', 'IGE', 'IRI', 'IHR', 'IRC', 'IVZ', 'IVX', 'IVC',
          'IOD', 'INR', 'IFL', 'IPB', 'IPH', 'IRE', 'IBC', 'IBG', 'ISU',
          'ISD', 'ISX', 'IGL', 'JHX', 'JAL', 'JAN', 'JHG', 'JHC', 'JAT',
          'JXT', 'JHL', 'JBH', 'JCS', 'JRV', 'JLG', 'JIN', 'JMS', 'K2F',
          'KPO', 'KLL', 'KAR', 'KAS', 'KMD', 'KTD', 'KGL', 'KNL', 'KDR',
          'KIN', 'KSL', 'KIS', 'KRR', 'KCN', 'KRM', 'KSS', 'KNM', 'KNO',
          'KGN', 'KFE', 'KOR', 'KP2', 'KTA', 'KYK', 'LSF', 'LKE', 'LBL',
          'LAA', 'LAW', 'LBT', 'LER', 'LEX', 'LGD', 'LEG', 'LCK', 'LLC',
          'LPD', 'LSH', 'LIC', 'LAU', 'LNU', 'LNK', 'LTR', 'LNG', 'LIT',
          'LPI', 'LVH', 'LVT', 'LCT', 'LPE', 'LCM', 'LON', 'LOV', 'LOM',
          'LYC', 'MLD', 'M7T', 'MAH', 'MRP', 'MQG', 'MFG', 'MGG', 'MAU',
          'MNS', 'MGU', 'MGL', 'MAI', 'MEY', 'MMM', 'MYE', 'MCE', 'MAT',
          'MXR', 'MXI', 'MFD', 'MYX', 'MEA', 'MMS', 'MXT', 'MCP', 'MDR',
          'MPL', 'MVP', 'MDC', 'MML', 'MP1', 'MJC', 'MEM', 'MEZ', 'MSB',
          'MLX', 'MTS', 'MEL', 'MMI', 'MFF', 'MGC', 'MXC', 'MHJ', 'MX1',
          'MWY', 'MOY', 'MIL', 'MLT', 'MCR', 'MRC', 'MIN', 'MEP', 'MNW',
          'MIR', 'MGR', 'MSV', 'MRM', 'MNF', 'MBM', 'MOB', 'MOD', 'MOE',
          'MOH', 'MND', 'MA1', 'MVF', 'MNY', 'MOC', 'MTO', 'MGX', 'MPR',
          'MPW', 'MCA', 'MRG', 'MGV', 'MYL', 'MYR', 'MYQ', 'MYS', 'NAG',
          'NAN', 'NVU', 'NSC', 'NAB', 'NSR', 'NTD', 'NVL', 'NML', 'NGI',
          'NVT', 'NBI', 'NEA', 'NMT', 'NTC', 'NET', 'NWL', 'NEU', 'NCZ',
          'NXE', 'NEW', 'NHC', 'NCM', 'NWF', 'NWS', 'NXT', 'NXM', 'NHF',
          'NCK', 'NIC', 'NEC', 'NBL', 'N27', 'NTU', 'PFP', 'PIQ', 'PSZ',
          'PTB', 'PUA', 'PPH', 'PWH', 'QAN', 'QIP', 'QBE', 'QEM', 'QMS',
          'QTM', 'QUB', 'QHL', 'QVE', 'RAC', 'RZI', 'RMS', 'RHC', 'RAN',
          'REA', 'RLE', 'RCE', 'RFT', 'RED', 'RDM', 'RVR', 'RBL', 'RDC',
          'RFX', 'REH', 'RGS', 'REG', 'RRL', 'RWC', 'RNU', 'RNT', 'RNE',
          'RAP', 'RMC', 'RMD', 'RSG', 'RHT', 'RDG', 'RFG', 'RVS', 'REF',
          'RWD', 'RXM', 'RNO', 'RHP', 'RHY', 'RIC', 'RIO', 'RGL', 'RMY',
          'ROO', 'RGI', 'RUL', 'RTG', 'RTR', 'RFF', 'RHL', 'RXP', 'S2R',
          'SGC', 'SO4', 'SFR', 'STO', 'SAR', 'SCG', 'SDV', 'SCT', 'SDI',
          'SFG', 'SLK', 'SES', 'SMX', 'SEK', 'SHV', 'SWF', 'SEN', 'SXY',
          'SNS', 'SE1', 'SRV', 'SSM', 'SVW', 'SWM', 'SGF', 'SSG', 'SFX',
          'SBW', 'SHJ', 'SCP', 'SHM', 'SIG', 'SLX', 'SIV', 'SLR', 'SVL',
          'SIS', 'SGM', 'SIT', 'SKN', 'SAS', 'SKT', 'SKC', 'SKF', 'SM8',
          'SPZ', 'SIQ', 'SMP', 'SIL', 'SHL', 'S32', 'SXE', 'SXL', 'SVM',
          'SKI', 'SPK', 'STW', 'SEI', 'SPX', 'SP3', 'SDA', 'SEC', 'SRS',
          'ST1', 'SHO', 'SRG', 'SBM', 'SGQ', 'SMR', 'SPL', 'GAS', 'SVY',
          'SDF', 'SGI', 'SGP', 'STA', 'SXA', 'SOR', 'STX', 'SRK', 'SMN',
          'SLZ', 'SUN', 'SDG', 'STM', 'SUL', 'SUP', 'SLC', 'SWK', 'SW1',
          'SYD', 'SOP', 'SM1', 'SYR', 'TAH', 'TLG', 'TLM', 'TAM', 'TNO',
          'TAP', 'TFL', 'TAS', 'TGR', 'TMT', 'TNE', 'TLX', 'TLS', 'TPW',
          'TGG', 'TPP', 'TMR', 'TER', 'TNT', 'THC', 'A2M', 'TBH', 'CGL',
          'DXN', 'FOD', 'TRS', 'SGR', 'VMX', 'VAN', 'VLT', 'VEE', 'VMS',
          'VXR', 'VMC', 'VRM', 'VRS', 'VG1', 'VCX', 'VLW', 'VRL', 'VMY',
          'VEN', 'VAH', 'VRT', 'VTI', 'VTG', 'VEA', 'VVR', 'VIV', 'VMT',
          'VOC', 'VHT', 'VN8', 'VRX', 'WGN', 'WKT', 'WAM', 'WGB', 'WLE',
          'WMI', 'WAX', 'WGO', 'SOL', 'WHA', 'WEB', 'WBA', 'WBT', 'WLD',
          'WES', 'WAF', 'WSA', 'WGX', 'WBC', 'WEC', 'WHC', 'WHK', 'WEL',
          'WND', 'WNR', 'WTC', 'WWG', 'WZR', 'WPL', 'WOW', 'WML', 'WOR',
          'WPP', 'XAM', 'XIP', 'XRO', 'XF1', 'XRF', 'XTD', 'YBR', 'YOJ',
          'YOW', 'ZLD', 'ZNC', 'ZGL', 'Z1P', 'ZNO']
