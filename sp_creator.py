'''
IMPORTANT: To use this script, remember:
1. Copy and paste all columns and assign to (columns) in line (20).
2. The store procedure name must start with: sp_load_fact[table_name] to create every file correctly.
3. Remember that the tables are created from a template and datatypes must be set.

__author__ = "Juan Manuel Dávila Restrepo"
__status__ = "Develop"
'''
import codecs

def run():
    filename = input("What is the store procedure name?: ")

    tmp_table = filename.replace('sp_load_fact', 'tmp')

    schema = 'etl_kaggle'

    # PASTE HERE YOUR COLUMNS
    # columns = ['dimension1', 'dimension2', 'metrica1', 'metrica2', 'metrica3']
    columns = ['country_id', 'country', 'year', 'ama_exchange_rate',
               'imf_based_exchange_rate', 'population', 'currency', 'per_capita_gni',
               'agriculture,hunting,forestry,fishing(isic_a_b)',
               'changes_in_inventories', 'construction_(isic_f)',
               'exports_of_goods_and_services', 'final_consumption_expenditure',
               'general_government_final_consumption_expenditure',
               'gross_capital_formation', 'gross_fixed_capital_formation',
               'household_consumption_expenditure', 'imports_of_goods_and_services',
               'manufacturing_(isic_d)', 'mining,_manufacturing,_utilities(isic_c_e)',
               'other_activities_(isic_j_p)', 'total_value_added',
               'transport,storage_and_communication(isic_i)',
               'wholesale,retail_trade,restaurants_and_hotels(isic_g_h)',
               'gross_national_income(gni)_in_usd', 'gross_domestic_product_(gdp)']

    fact_table = tmp_table.replace('tmp', 'fact')

    print(filename, tmp_table, fact_table)
    # CREATE TMP TABLE
    f_tmp = codecs.open('./files/' + tmp_table + '.sql', 'w', 'utf-8')

    cols_define_tables = ''

    for i in range(len(columns)):
        if(i == len(columns) - 1):
            cols_define_tables = cols_define_tables + f'''"{columns[i]}" TEXT NULL\n'''
        else:
            cols_define_tables = cols_define_tables + f'''"{columns[i]}" TEXT NULL,\n'''

    text_create_table = f'''
    BEGIN;
    CREATE TABLE IF NOT EXISTS {schema}.{tmp_table} (
        {cols_define_tables}
    );
    COMMIT;
    '''

    f_tmp.write(text_create_table)
    f_tmp.close()

    # CREATE FACT TABLE
    f_fact = codecs.open('./files/' + fact_table + '.sql', 'w', 'utf-8')

    f_fact.write(f'''
    BEGIN;
    CREATE TABLE IF NOT EXISTS {schema}.{fact_table} (
        {cols_define_tables}
    );
    COMMIT;
    ''')

    f_fact.close()

    # CREATE STORE PROCEDURE
    f = codecs.open('./files/' + filename + '.sql', 'w', 'utf-8')

    cols_define = ''
    for i in range(len(columns)):
        if(i == len(columns)-1 ):
            cols_define = cols_define+f'''"{columns[i]}"\n'''
        else:
            cols_define = cols_define+f'''"{columns[i]}",\n'''

    cols_update_define = ''
    for i in range(len(columns)):
        if(i == len(columns)-1):
            cols_update_define = cols_update_define+f'''a."{columns[i]}" = b."{columns[i]}"\n'''
        else:
            cols_update_define = cols_update_define+f'''a."{columns[i]}" = b."{columns[i]}",\n'''

    cols_b_define = ''
    for i in range(len(columns)):
        if(i == len(columns)-1):
            cols_b_define = cols_b_define+f'''b."{columns[i]}"\n'''
        else:
            cols_b_define = cols_b_define+f'''b."{columns[i]}",\n'''

    f.write(f'''-- ================================================
    -- Template generated from Template Explorer using:
    -- Create Procedure (New Menu).SQL
    --
    -- Use the Specify Values for Template Parameters 
    -- command (Ctrl-Shift-M) to fill in the parameter 
    -- values below.
    --
    -- This block of comments will not be included in
    -- the definition of the procedure.
    -- ================================================

    CREATE OR REPLACE PROCEDURE {schema}.{filename}()
    LANGUAGE plpgsql
    AS $$
    BEGIN
        WITH b AS (
            SELECT
                {cols_define}
            FROM {schema}.{tmp_table}
        )
        INSERT INTO {schema}.{fact_table} (
            {cols_define}
        )
        SELECT 
        {cols_define}
        FROM b
        ON CONFLICT (
            date
            ) DO UPDATE
        SET 
        {cols_update_define}
        ;
    END;
    $$;
    ''')

    f.close()

if __name__ == "__main__":
    run()