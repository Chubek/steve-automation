from operator import add
from address import Address
from cluster import cluster
import pandas as pd
import ntpath
import os

class Parser:

    def __init__(self, file_path, sheetname, new):
        self.filepath = file_path
        self.df = pd.read_excel(file_path, sheet_name=sheetname)
        folder, filename = self.__path_leaf(self.filepath)
        format = "xlsx" if new else "xls"
        self.writer = pd.ExcelWriter(os.path.join(folder, f"{filename}_output.{format}"), mode='w')
        self.km = {}

    def __read_columns(self, route, columns, start, end):
        return self.df[self.df["Route"] == route].loc[start:end, columns]

    def __write_df(self, new_df, sheet_name, close=False):
        new_df.to_excel(self.writer, sheet_name=sheet_name)

        if close:
            self.writer.close()

    def __path_leaf(self, path):
        head, tail = ntpath.split(path)
        return head, tail.split(".")[-2]


    def operate(self, routes, address_field, city_field, province_field, zip_field, start, end):
        done = 0
        err = 0
       
        for i, route in enumerate(routes):
            
            columns = self.__read_columns(route, [address_field, city_field, province_field, zip_field], start, end)
            
            if columns.shape[0] < 1:
                err += 1
                continue

            addresses = [Address(columns.iloc[i, 0], columns.iloc[i, 1], columns.iloc[i, 2], columns.iloc[i, 3]).return_val() for i in range(columns.shape[0])]

            labels, self.km[route] = cluster(addresses)

            columns["Label"] = [f"L{label}" for label in labels]

            self.__write_df(columns, f"{route}_sheet", close=i + 1 == len(routes))

            done += 1
                

        return done, err

    def predict(self, route, address, city, province, zip):
        info = Address(address, city, province, zip).return_val()

        return self.km[route].predict(info)