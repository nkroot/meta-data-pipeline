

def get_existing_data(cursor:str,table_name:str,col_name:str):

    cursor.execute("""select distinct {col} from {table_name}""".format(col=col_name,table_name=table_name))
    
    return [r[0] for r in cursor.fetchall()]


def get_existing_hashed_data(cursor:str,table_name:str,col_name:str):

    cursor.execute("""select distinct {col} from {table_name}""".format(col=col_name,table_name=table_name))
    
    return [hash(tuple(str(record_val) for record_val in record)) for record in cursor.fetchall()]