from supabase import create_client, Client
from typing import Dict
from dotenv import load_dotenv
import os


class DataBase():
    def __init__(self):
        load_dotenv(".env")
        self.URL = os.getenv("SUPABASE_URL")
        self.API_KEY = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.URL, self.API_KEY)

    def fetch_eq(self, table: str = None,
                 col: str = '*',
                 key: str = None, val: str = '*'):
        if table is None:
            return
        return self.supabase\
            .table(table)\
            .select(col)\
            .eq(key, val)\
            .execute()

    def fetch(self, table: str = None,
              col: str = '*',
              ):
        if table is None:
            return
        return self.supabase\
            .table(table)\
            .select(f"{col}")\
            .execute()

    def insert(self, table: str = None, data: Dict = None):
        if table is None or data is None:
            return
        self.supabase\
            .table(table)\
            .insert(data)\
            .execute()

    def update(self, table: str = None,
               name: str = None,
               key: str = None,
               val: str | bool = None):
        if table is None or name is None or key is None or val is None:
            return
        self.supabase.table(table)\
            .update({
                key: val,
            })\
            .eq("task_name", name)\
            .execute()

    def delete(self, table: str = None, key: str = None, val: str = None):
        self.supabase\
            .table(table)\
            .delete()\
            .eq(key, val)\
            .execute()
