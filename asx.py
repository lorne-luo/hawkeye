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

codes1 = ['MOQ', '14D', 'TGP', 'TOT', '3PL', '5GN', '8CO', 'A2B', 'ABP',
          'AEG', 'AX1', 'ACQ', 'ACF', 'ACR', 'ADA', 'ADH', 'ABC', 'ADT',
          'ANO', 'AV1', 'AML', 'AEI', 'AIS', 'APT', 'AGL', 'AMN', 'AGR',
          'AGI', 'AIZ', 'AQG', 'LEP', 'AJX', 'ALK', 'AQZ', 'A40', 'A4N',
          'ALQ', 'ATC', 'AGH', 'ALU', 'AJM', 'AWC', 'AMA', 'AYS', 'AMH',
          'AMC', 'ABR', 'AMP', 'AS1', 'AB1', 'ANN', 'APL', 'APE', 'APA',
          'AHX', 'APD', 'AOP', 'ATL', 'APX', 'ARB', 'AR9', 'ARL', 'ALG',
          'ARF', 'ALI', 'ARG', 'ALL', 'ARQ', 'AHY', 'ASH', 'ASX', 'ALX',
          'ATU', 'AUB', 'AIA', 'AD8', 'AU8', 'AMI', 'AZJ', 'A3D', 'AC8',
          'ASL', 'AMG', 'AST', 'ASB', 'ANG', 'ANZ', 'AAC', 'ABX', 'AHF',
          'AEF', 'AFG', 'AFI', 'ALF', 'API', 'AOF', 'AVG', 'ATS', 'AHG',
          'ASG', 'AVA', 'AVN', 'AOG', 'AVH', 'AVJ', 'AZS', 'BBN', 'BTI',
          'BOQ', 'BAP', 'BSE', 'BRL', 'BBX', 'BCI', 'BPT', 'BLX', 'BCC',
          'BGA', 'BFG', 'BAL', 'BGL', 'BEN', 'BLT', 'BKY', 'BFC', 'BHP',
          'BID', 'BTH', 'BIN', 'BGT', 'BNO', 'BGS', 'BKI', 'BC8', 'BKT',
          'BKL', 'BLA', 'BAF', 'BSL', 'BLG', 'BDA', 'BOL', 'BLD', 'BOT',
          'BXB', 'BVS', 'BRB', 'BRG', 'BKW', 'BSA', 'BUB', 'BRU', 'BUX',
          'BWP', 'BWX', 'BYE', 'CDM', 'CTX', 'CAN', 'CP1', 'CAY', 'CAJ',
          'CAA', 'CWX', 'CDV', 'CDD', 'CVN', 'CAR', 'CCV', 'CYL', 'CAT',
          'CWP', 'CDY', 'CTP', 'CXM', 'CNI', 'CIP', 'CMA', 'CFO', 'CHN',
          'CGF', 'CIA', 'CQE', 'CHC', 'CLW', 'CQR', 'CNU', 'CIM', 'CCX',
          'CL1', 'CSS', 'CLQ', 'CWY', 'CVW', 'CPV', 'CAM', 'CUV', 'CLV',
          'CGR', 'COB', 'CCL', 'COH', 'CDA', 'COL', 'CLH', 'CKF', 'COI',
          'CBA', 'CMP', 'CPU', 'CIE', 'COE', 'C6C', 'CRN', 'CTD', 'CGC',
          'CYG', 'CRD', 'CCP', 'CPH', 'CMW', 'CWN', 'CSV', 'CSL', 'CSR',
          'CV1', 'CYB', 'CYP', 'DCN', 'DNK', 'DTL', 'DCG', 'DYL', 'DXS',
          'DGR', 'DDR', 'DUI', 'DJW', 'DCL', 'DHG', 'DMP', 'DOW', 'DTS',
          'DN8', 'DRO', 'DUB', 'DLX', 'D2O', 'DWS', 'E2M', 'EHH', 'EM2',
          'EAR', 'ECX', 'EGA', 'ENN', 'ELD', 'EOS', 'EXL', 'EAI', 'EGI',
          'ELX', 'ELS', 'EHL', 'EML', 'EPD', 'EMV', 'EAX', 'ERA', 'EGG',
          'EVS', 'EPW', 'EHE', 'EGH', 'EMN', 'EZL', 'EGD', 'EVT', 'EVN',
          'EVO', 'EXP', 'FZO', 'FRM', 'FTZ', 'FCT', 'FPH', 'FWD', 'FBU',
          'FXL', 'FLT', 'FLC', 'FOR', 'FMG', 'FNP', 'FLN', 'FDV', 'GMV',
          'GUD', 'GEM', 'GLN', 'GXY', 'GAP', 'G1A', 'GLL', 'GAL', 'GBT',
          'GDI', 'GSS', 'GNX', 'GMA', 'GSW', 'GC1', 'GEV', 'GVF', 'GOR',
          'GMG', 'GPT', 'GNG', 'GNC', 'GRR', 'GPX', 'GOZ', 'GTN', 'GWA',
          'HSN', 'HVN', 'HAS', 'HAV', 'HZR', 'HLS', 'HSO', 'HM1', 'HE8',
          'HLO', 'HMD', 'HRR', 'HXG', 'HFR', 'HIG', 'HIL', 'HZN', 'HPI',
          'HRL', 'HT1', 'HUB', 'HUO', 'HTA', 'ICQ', 'IEL', 'IDT', 'ILU',
          'IMA', 'IMD', 'IMF', 'IMC', 'IPD', 'IPL', 'IGO', 'IFN', 'IFM',
          'INA', 'ING', 'IAG', 'IDX', 'IGE', 'IRI', 'IRC', 'IVC', 'INR',
          'IFL', 'IPH', 'IRE', 'IBC', 'ISU', 'ISD', 'ISX', 'IGL', 'JHX',
          'JAL', 'JAN', 'JHG', 'JHC', 'JXT', 'JBH', 'JRV', 'JLG', 'JIN',
          'JMS', 'K2F', 'KLL', 'KAR', 'KMD', 'KTD', 'KGL', 'KNL', 'KDR',
          'KSL', 'KCN', 'KSS', 'KGN', 'LSF', 'LBL', 'LEX', 'LGD', 'LCK',
          'LLC', 'LIC', 'LAU', 'LNK', 'LNG', 'LPI', 'LVH', 'LVT', 'LPE',
          'LCM', 'LON', 'LOV', 'LOM', 'LYC', 'MLD', 'M7T', 'MAH', 'MQG',
          'MFG', 'MGG', 'MAU', 'MNS', 'MAI', 'MMM', 'MYE', 'MCE', 'MAT',
          'MXI', 'MFD', 'MYX', 'MEA', 'MMS', 'MXT', 'MCP', 'MPL', 'MVP',
          'MDC', 'MML', 'MP1', 'MEZ', 'MSB', 'MLX', 'MTS', 'MMI', 'MFF',
          'MGC', 'MHJ', 'MX1', 'MWY', 'MOY', 'MIL', 'MLT', 'MCR', 'MRC',
          'MIN', 'MIR', 'MGR', 'MRM', 'MNF', 'MOD', 'MOE', 'MND', 'MA1',
          'MVF', 'MNY', 'MOC', 'MTO', 'MGX', 'MPW', 'MCA', 'MYR', 'MYQ',
          'MYS', 'NAN', 'NSC', 'NAB', 'NSR', 'NTD', 'NVL', 'NGI', 'NVT',
          'NBI', 'NEA', 'NMT', 'NTC', 'NWL', 'NEU', 'NCZ', 'NEW', 'NHC',
          'NCM', 'NWF', 'NWS', 'NXT', 'NHF', 'NCK', 'NIC', 'NEC', 'NBL',
          'PFP', 'PIQ', 'PTB', 'PPH', 'PWH', 'QAN', 'QIP', 'QBE', 'QEM',
          'QMS', 'QUB', 'QVE', 'RZI', 'RMS', 'RHC', 'REA', 'RCE', 'RED',
          'RVR', 'RBL', 'RDC', 'REH', 'REG', 'RRL', 'RWC', 'RAP', 'RMC',
          'RMD', 'RSG', 'RHT', 'RFG', 'RVS', 'RNO', 'RHP', 'RHY', 'RIC',
          'RIO', 'RMY', 'RGI', 'RUL', 'RFF', 'RHL', 'RXP', 'SO4', 'SFR',
          'STO', 'SAR', 'SCG', 'SCT', 'SDI', 'SLK', 'SMX', 'SEK', 'SHV',
          'SWF', 'SXY', 'SNS', 'SE1', 'SRV', 'SSM', 'SVW', 'SWM', 'SGF',
          'SSG', 'SFX', 'SBW', 'SHJ', 'SCP', 'SHM', 'SIG', 'SLX', 'SIV',
          'SLR', 'SGM', 'SKT', 'SKC', 'SKF', 'SPZ', 'SIQ', 'SMP', 'SIL',
          'SHL', 'S32', 'SXE', 'SXL', 'SKI', 'SPK', 'STW', 'SP3', 'SDA',
          'SEC', 'ST1', 'SRG', 'SBM', 'SGQ', 'SMR', 'SPL', 'GAS', 'SVY',
          'SDF', 'SGP', 'STA', 'SMN', 'SUN', 'SDG', 'SUL', 'SLC', 'SWK',
          'SW1', 'SYD', 'SM1', 'SYR', 'TAH', 'TLG', 'TFL', 'TGR', 'TMT',
          'TNE', 'TLX', 'TLS', 'TPW', 'TGG', 'TMR', 'TER', 'THC', 'A2M',
          'CGL', 'TRS', 'SGR', 'VMX', 'VAN', 'VLT', 'VEE', 'VXR', 'VMC',
          'VG1', 'VCX', 'VLW', 'VRL', 'VEN', 'VAH', 'VRT', 'VTG', 'VEA',
          'VVR', 'VMT', 'VOC', 'VHT', 'VN8', 'WGN', 'WKT', 'WAM', 'WGB',
          'WLE', 'WMI', 'WAX', 'WGO', 'SOL', 'WHA', 'WEB', 'WBA', 'WBT',
          'WES', 'WAF', 'WSA', 'WGX', 'WBC', 'WHC', 'WHK', 'WND', 'WNR',
          'WTC', 'WWG', 'WZR', 'WPL', 'WOW', 'WOR', 'WPP', 'XIP', 'XRO',
          'XF1', 'XRF', 'YOJ', 'ZGL', 'Z1P', 'ZNO']

codes2 = codes1 + ['MEI', 'RDS', 'INP', 'MRP', 'CKA', 'IDZ', 'HSC', 'AVQ', '9SP', 'LBT', 'AVZ', 'CLI', 'AGS', 'ADR',
                   'BLZ', 'ALY', 'SHO', 'CFE', 'ICI', 'NXE', 'BSR', 'VRC', 'APC', 'SCU', 'AD1', 'NTI', 'BDC', 'SGI',
                   'AUZ', 'KSN', 'EN1', 'ACB', 'RAC', 'AAU', 'ENR', 'BXN', 'GSN', 'PSC', 'FUN', 'DOR', 'IVZ', 'BCK',
                   'RGL', 'CNJ', 'ASN', 'PUR', 'MEP', 'INF', 'JHL', 'IHR', 'CAP', 'LKE', 'SPX', 'CNW', 'SIS', 'ARV',
                   'STX', 'MGU', '1ST', 'DVL', 'RDM', 'TAS', 'ASP', 'GBG', 'AHQ', 'ARS', 'CAF', 'MTC', 'NVU', 'KAS',
                   'STM', 'ESR', 'IME', 'AQD', 'ACL', 'MSG', 'SIH', 'EMR', 'EUR', 'MAY', 'AAR', 'NNW', 'HNR', 'TLM',
                   'SRZ', 'FYI', 'AZM', 'BIQ', 'COG', 'DEV', 'GGG', 'DXN', 'BPP', 'SVM', 'FMS', 'MXR', 'AXT', 'AME',
                   'MEL', 'SES', 'CRB', 'AUR', 'RFT', 'SEN', 'FHS', 'AQI', 'DNA', 'SOP', 'VRS', 'AEV', 'EUC', 'IMU',
                   'SVL', 'ADO', 'CUL', 'BMG', 'TAM', 'MPR', 'IBX', 'AHN', 'MZI', 'EHX', 'SDV', 'FFG', 'BCT', 'LER',
                   'AJL', '1AG', 'CAE', 'RWD', 'EEG', 'HMX', '88E', 'TPP', 'PUA', 'KTA', 'ICN', 'ARD', 'CE1', 'CXX',
                   'QTM', 'AGY', 'DCC', 'XTD', 'HLX', 'BCB', 'EM1', 'SGC', 'LAW', 'AFR', 'G88', 'PM1', 'IVX', 'CAZ',
                   'CZR', 'CWL', 'AJQ', 'ATP', 'YBR', 'CUE', 'SVD', 'VTI', 'MYL', 'LNU', 'FSG', 'RXM', 'GOO', 'BRN',
                   'ARM', 'RGS', 'DRX', 'VRM', 'IP1', 'KYK', 'IHL', 'GTR', 'MSV', 'SRS', 'ECT', 'WML', 'GWR', 'QHL',
                   'NML', 'MRG', 'ZNC', 'IPB', 'FIN', 'B2Y', 'ESH', 'ANW', 'ERX', 'KNM', 'COO', 'RFX', 'EGL', 'KOR',
                   'SUP', 'ADY', 'KPO', 'ACW', 'ALC', 'ESE', 'ABT', 'GID', 'ARE', 'AIY', 'AQX', 'CZL', 'MEB', 'LCT',
                   'CRL', 'SBB', 'REF', 'RCP', 'AWY', 'ICT', 'EXR', 'S2R', 'LSH', 'ERM', 'IEC', 'RLE', 'ROO', 'TNT',
                   'TBH', 'AHZ', 'AKM', 'FEX', 'EWC', 'RBR', 'GMN', 'ESV', 'SYA', 'AL8', 'BMN', 'RTG', 'CHZ', 'BIT',
                   'RNE', 'GRB', 'CCG', 'PVD', 'DXB', 'WEL', 'KFE', 'GTG', 'CGN', 'GPR', 'CLA', 'JAT', 'DTI', 'EDE',
                   'TAP', 'VKA', 'MGV', 'FBR', 'BDG', 'MNW', 'SXA', 'IMM', 'GML', 'BPL', 'MBM', 'CMM', 'MEY', 'MXC',
                   'RNT', 'SFG', 'MOB', 'AZY', 'CVV', 'CZI', 'GIB', 'AON', 'BSX', 'RAN', 'MEM', 'ATH', 'PPL', 'MOH',
                   'CMC', 'KRR', 'MGL', 'INK', 'DSE', 'JCS', 'BRK', 'GBR', 'LIT', 'AVL', 'CXO', 'CCA', 'XPD', 'RTR',
                   'AXP', 'BAR', 'KMT', 'N27', 'BD1', 'ARU', 'BCN', 'SLZ', 'FDM', 'ANP', 'MLM', 'RDG', 'HGO', 'TNO',
                   'HAW', 'WNB', 'AUQ', '4DS', 'VMY', 'RNU', 'NXM', 'LEG', 'BEE', 'KNO', 'SRK', 'KRM', 'FEL', 'MJC',
                   'MEU', 'SVT', 'DMG', 'LTR', 'NTU', 'WMC', 'NWC', 'IOD', 'SGO', 'WLD', 'BEM', 'HCH', 'AUC', 'WEC',
                   'PSZ', 'MDR', 'TDO', 'IGN', 'XAM', 'VRX', 'KP2', 'DEG', 'ENA', 'BLU', 'EMU', 'GCY', 'LPD', 'SEI',
                   'CM8', 'AZV', 'AXE', 'ABV', 'LCD', 'ADJ', 'KIS', 'BOE', 'CAI', 'SAS', 'GMR', 'RMG', 'GMD', 'CI1',
                   'DTZ', 'BUD', 'HYD', 'FOD', 'RMP', 'SIT', 'NAG', 'NET', 'GED', 'BAT', 'LAA', 'HPR', 'SKN', 'VMS',
                   'YOW', 'KIN', 'IBG', 'VIV', 'FAR', 'SOR', 'CDX', 'ZLD', 'FRN', 'AMD', 'SM8']

codes3 = codes2 + ['LRS', 'ATX', 'RDF', 'BYI', 'STN', 'CIO', 'LHB', 'RTE', 'KZA', 'BAH', 'SEQ', 'CAQ', 'HOT', 'ZER', 'AJC',
                'RMX', 'VBS', 'YAL', 'ASW', 'NCC', 'AQS', 'DME', 'CGO', 'GTE', 'CVC', 'MCX', 'WIC', '4CE', 'LRM', 'AER',
                'CVS', 'BUG', 'AKP', 'FRI', 'RLC', 'HOR', 'CL8', 'GPP', 'DW8', 'KSC', 'DDD', 'RD1', 'ELT', 'XPL', 'LMW',
                'TWD', 'AVW', 'AWV', 'HGH', 'RDH', 'QGL', 'BRI', 'AQC', 'MDI', 'DAU', 'AQR', 'IVR', 'LIN', 'LYL', 'JRL',
                'DAF', 'TAO', 'ZEL', 'DFM', 'AOU', 'AIV', 'BEL', 'ETE', 'MAG', 'ANR', 'RNX', 'SCN', 'BAU', 'EMH', 'CY5',
                'WOA', 'STG', 'CAV', 'KAT', 'SFY', 'QFY', 'AGG', 'FGG', 'KAM', 'XPE', 'JJF', 'IKW', 'BOA', 'HCT', 'EGN',
                'GLH', 'LNY', 'EBG', 'COY', 'KPT', 'TMK', 'SND', 'AHK', 'TPD', 'HGM', 'KOV', 'AXI', 'SPT', 'MOT', 'EBO',
                'ABA', 'MZN', 'LI3', 'MVT', 'AMT', 'SRI', 'AYI', 'ONT', 'FSI', 'IVT', 'JAY', 'CYQ', 'EDC', 'KGM', 'SNZ',
                'E2E', 'RAG', 'FE8', 'SHK', 'DTM', 'GNE', 'CDP', 'ELO', 'IPC', 'EFE', 'NAE', 'EXO', 'ICG', 'BGP', 'T3D',
                'REV', 'AGJ', 'WHF', 'WBE', 'WLL', 'KWR', 'KPC', 'RDN', 'RYD', 'VML', 'ARN', 'KLA', 'SXX', 'SFC', 'NSE',
                'CMD', 'CCJ', 'LLO', 'CLZ', 'SYT', 'SUH', 'DLC', 'N1H', 'AEE', 'CLY', 'GLB', 'IVQ', 'GES', 'ARO', 'AIB',
                'FEI', 'AYZ', 'RCW', 'FSA', 'CHK', 'AKG', 'IAU', 'FAM', 'DDT', 'NZK', 'HLA', 'GGE', 'BSM', 'PSI', 'CTE',
                'AWN', 'MRL', 'SFL', 'MWR', 'AU1', 'WCN', 'RKN', 'AYM', 'CD2', 'MKG', 'PCH', 'MTB', 'VEC', 'KRX', 'SCI',
                'CZN', 'ABL', 'SPQ', 'EGY', 'AUL', 'MAX', 'MNC', 'ECL', 'DBF', 'BST', 'IRD', 'CNL', 'EOF', 'RNY', 'DHR',
                'WWI', 'WQG', 'AYK', 'CBY', 'NAC', 'TDL', 'MRR', 'DAV', 'HNG', 'NGE', 'KBC', 'IAB', 'KLO', 'CD3', 'GGX',
                'APZ', 'ALT', 'MAQ', 'AO1', 'SLF', 'GCI', 'MZZ', 'EX1', 'AUI', 'SAU', 'RHI', 'ROG', 'NCL', 'GMC', 'SHI',
                'RXH', 'SLM', 'SAN', '1AD', 'HWK', 'CIW', 'IBN', 'IKE', 'GDG', 'SUR', 'DGH', 'GTK', 'MGT', 'AMO', 'BNR',
                'CGM', 'SOM', 'ATM', 'LML', 'BLY', 'RRS', 'MQR', 'MMR', 'AAP', 'FPC', '8VI', 'DRE', 'MPH', 'GLE', 'GFL',
                'BLK', 'RND', 'FGO', 'SSL', 'FPL', 'CVL', 'ACS', 'CGA', 'SIO', 'ADN', 'CR1', 'TRL', 'MTH', 'SVS', '8IH',
                'CDT', 'EVE', 'FFI', 'MBK', 'EER', 'BBL', 'EMP', 'GCM', 'BGH', 'QPR', 'SF1', 'ANL', 'ATR', 'KEY', 'CBC',
                'MRZ', 'SKO', 'BIS', 'GO2', 'GBZ', 'GUL', 'MCM', 'DKM', 'NSB', 'GME', 'MSR', 'JYC', 'ERL', 'BDI', 'KKL',
                'VIC', 'AOA', 'BAS', 'ARC', 'VLS', 'EQT', 'MAR', 'IVO', 'VGL', 'SBR', 'MRN', 'MCT', 'GCR', 'JDR', 'BUY',
                'EMB', 'CUP', 'ADD', 'SL1', 'AX8', 'AAJ', 'AMS', 'IFT', 'IAM', 'MRQ', 'AYF', 'FIJ', 'CXU', 'KGD', 'CAD',
                'ADV', '8EC', 'REX', 'AYR', 'IMS', 'ERF', 'BPH', 'RXL', 'SPO', 'NTL', 'VII', 'MHI', 'CVF', 'CTM', 'SUD',
                'HRN', 'NME', 'GPS', 'SEA', 'GLV', 'SI6', 'SMC', 'CGS', 'PRO', 'WRM', 'LSX', 'E25', 'RCO', 'EPM', 'EVZ',
                'MEC', 'CML', 'PLX', 'CRS', 'RCL', 'ERG', 'BWR', 'FGR', 'BTC', 'GBE', 'HHY', 'GBP', 'LVE', 'CTO', 'MSI',
                'DTR', 'CRM', 'CXZ', 'AUT', 'RIM', 'SFM', 'MDX', 'DGO', 'CHR', 'XST', 'NC6', 'KME', 'GLA', 'EFF', 'FAU',
                'ESK', 'IPT', 'INV', 'VP7', 'SRN', 'KPE', 'BYH', 'HHM', '360', 'LCY', 'LSA', 'CII', 'KTE', 'HGL', 'RFN',
                'ZIM', 'FND', 'VAL', 'SST', 'LKO', 'PGR', 'TMX', 'SRY', 'EAS', 'FML', 'SGH', 'R3D', 'FRX', 'A1G', 'KPG',
                'LIO', 'NES', 'MPX', 'NAM', 'FGF', 'MSE', 'CUX', 'SRO', 'CRO', 'CEN', 'TZN', 'AGE', 'AIQ', 'FTC', 'AIR',
                'CSE', 'CAG', 'FPP', 'IDA', 'SMD', 'HT8', 'YRL', 'SDX', 'EME', 'SNC', 'ENE', 'FCC', 'FSF', 'S66', 'LRT',
                'AUH', 'CLB', 'SMI', 'ZMI', 'EQX', 'SER', 'EQE', 'FZR', 'GZL', 'EAF', 'YPB', 'IXU', 'ARX', 'ED1', 'CG1',
                'BHL', 'WAA', 'XTE', 'FID', 'BBC', 'DVN', 'BNL', 'HCO', 'MRD', 'MAM', 'CA8', 'BOC', 'RIE', 'MHC', 'ID8',
                'QTG', 'GSM', 'NXS', 'ADI', 'HIP', 'RDY', 'VIG', 'RFR', 'AHL', 'ICS', 'BWF', 'MPP', 'MLS', 'AKN', 'RCT',
                'GDF', 'TCN', 'PO3', 'SNL', 'CYC', 'AMB', 'AUP', 'QRI', 'CLF', 'TAR', 'LSR', 'APW', 'CLT', 'VMG', 'AZI',
                'IS3', 'FNT', 'LMG', 'FFC', 'VAR', 'CIN', 'DEM', 'APG', 'AFP', 'ICU', 'MMJ', 'ECG', 'ENX', 'ARA', 'POW',
                'SRH', 'CLX', 'SPB', 'CT1', 'JPR', 'MRV', 'SCL', 'EOL', 'CXL', 'ADX', 'FTT', 'AVC', 'KLH', 'KKT', 'AFA',
                'REY', 'EGF', 'BIR', 'GRV', 'GOW', 'AGM', 'HIT', 'MCY', 'ENT', 'AGD', 'WAT', 'AJJ', 'TBL', 'JCI', 'FGX',
                'LHM', 'NMS', 'A1C']
