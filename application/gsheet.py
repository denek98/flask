from oauth2client.service_account import ServiceAccountCredentials

import gspread
import gspread_dataframe as gd
import os
import pandas as pd

class Gsheet():
    def __init__(self):
        self.__path = os.path.abspath(os.getcwd())
        self.__readed_data_file_path = os.path.join(self.__path, 'data.csv')
        self.__creds_file_name = 'creds.json'
        self.__sheet_url = 'https://docs.google.com/spreadsheets/d/1twdIEXlFWhOZcpJBvPTg-Gl2kB1dkgvUk-mVFq2rmqY/edit#gid=0'
        self.__sheet_name = 'flask-app'
        self.__auth_gsheet = self.__class__.__auth_for_gsheet(self.__path,self.__sheet_url,self.__sheet_name,self.__creds_file_name)
        self.__raw_df_from_sheet = self.__read_data_from_sheet_to_dataframe(self.__auth_gsheet)
        try:
            self.__df_to_upload = pd.read_csv(os.path.join(self.__path, 'data-to-upload.csv'))
        except:
            pass
            
    def export_readed_data_to_csv(self):
        self.__raw_df_from_sheet.to_csv(self.__readed_data_file_path,index = False)

    def upload_new_data_to_sheet(self):
        united_df = pd.concat([self.__df_to_upload,self.__raw_df_from_sheet])
        gd.set_with_dataframe(self.__auth_gsheet, united_df,resize=False)
    
    @staticmethod
    def __auth_for_gsheet(path,sheet_url, sheet_name, creds_json):
        creds_json = os.path.join(path,creds_json)
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
        client = gspread.authorize(creds)
        wsh = client.open_by_url(sheet_url).worksheet(sheet_name)
        return wsh

    @classmethod
    def __read_data_from_sheet_to_dataframe(cls,auth_gsheet):
        gsheet_df = gd.get_as_dataframe(auth_gsheet)
        try:
            gsheet_df.dropna(inplace=True,how = 'all')
            gsheet_df.dropna(axis = 1,inplace=True,how = 'all')
            return gsheet_df
        except Exception as e:
            print('get_gsheet_data', e)
            return False

    @property
    def datafile(self):
        return self.__readed_data_file_path